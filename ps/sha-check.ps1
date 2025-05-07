#! /opt/microsoft/powershell/7/pwsh

<#
.DESCRIPTION
    Match the SHA256 checksum of a file and a string.
#>

param (
        [Parameter(Mandatory, HelpMessage="Path")]
        [string] $Path,

        [Parameter(Mandatory, HelpMessage="Checksum String")]
        [string] $Sum,

        [Parameter(HelpMessage="Use SHA1 instead of SHA256")]
        [switch] $S1
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
    $a = If ($S1) {"SHA1"} Else {"SHA256"}

    if (Test-Path $Sum) {
        $p = $Sum
        $s = $Path
    } elseif (!(Test-Path $Path)) {
        echo("Error! Invalid path: $Path");
        exit
    }

    $h = (Get-FileHash -Algorithm $a -Path $p).hash

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
