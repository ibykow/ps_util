#! /opt/microsoft/powershell/7/pwsh

<#
.DESCRIPTION
    Match the SHA256 checksum of a file and a string.
#>

param (
        [Parameter(Mandatory, HelpMessage="Path")]
        [string] $Path,

        [Parameter(Mandatory, HelpMessage="Checksum String")]
        [string] $Sum
)

function test_path($p) {
    if (!(Test-Path $p)) {
        echo("Error! Invalid path: $p");
        exit
    }
}

function main() {
    $p = $Path
    $s = $Sum

    if (Test-Path $Sum) {
        $p = $Sum
        $s = $Path
    } elseif (!(Test-Path $Path)) {
        echo("Error! Invalid path: $Path");
        exit
    }

    $h = (Get-FileHash -Algorithm SHA256 -Path $p).hash

    $diff = diff $h $s

    if ($diff.count) {
        echo("NO MATCH!")
        echo("$h - $p")
        echo("$s - Provided Checksum")
    } else {
        echo("Match: $h")
    }
}

main
