#! /opt/microsoft/powershell/7/pwsh

<#
.DESCRIPTION
    Hash files recursively
#>

param (
    [Parameter(HelpMessage = "Path")]
    [string] $Path = "./"
)

function main() {
    $fails = @()
    $files = @{}
    $dupes = @{}
    $waste = 0

    $start = Get-Date
    $lastUpdate = Get-Date

    $p = Convert-Path $Path

    Write-Output "($start) Searching for file duplicates in $p"

    Get-ChildItem -Recurse -Attributes !Directory $p | ForEach-Object {
        $hash = (Get-FileHash -LiteralPath $_.FullName).hash

        if (-not $hash) {
            Write-Output "Could not hash $($_.FullName)"
            $fails += $_.FullName
            return
        }

        $shash = $hash[0..7] -join ''
        $copies = 0
        $fwaste = 0

        $info = @{
            Name     = $_.Name;
            FullName = $_.FullName;
            Path     = $_.DirectoryName;
            Length   = $_.Length;
        }

        if ($files[$hash]) {
            $files[$hash] += $info

            $copies = $files[$hash].length - 1
            $fwaste = $_.Length * $copies
            $waste += $_.Length

            $dupes[$hash] = @{ Copies = $copies; Waste = $fwaste }

            $lastUpdate = Get-Date
        } else {
            $files[$hash] = @($info)

            $now = Get-Date
            $deltam = ((Get-Date) - $lastUpdate).TotalMinutes

            if ($deltam -ge 1) { $lastUpdate = $now } else { return }
        }

        Write-Output "$shash $($_.FullName) $fwaste ($($_.Length) x $copies) / $waste"
    }

    $output = [ordered]@{
        Fails = $fails;
        Files = $files;
        Dupes = $dupes;
        Waste = $waste; 
    }

    $filename = "$((pwd).Path)\.$(Get-Date -Format yyyy-MM-dd-HHmmss).filehash.json"

    ConvertTo-Json -Depth 4 $output > $filename

    Write-Output "Results took $((get-date) - $start), and written to: $filename"
    Write-Output "$($dupes.count) unique duplicates found. Total excess size: $waste"
}

main