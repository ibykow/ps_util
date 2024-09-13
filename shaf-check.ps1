#! /opt/microsoft/powershell/7/pwsh

<#
.DESCRIPTION
    Compare the SHA256 checksum of two files.
#>

param (
        [Parameter(Mandatory, HelpMessage="Path A")]
        [string] $PathA,

        [Parameter(Mandatory, HelpMessage="Path B")]
        [string] $PathB
)

function test_path($p) {
    if (!(Test-Path $p)) {
        echo("Error! Invalid path: $p");
        exit
    }
}

function main() {
    test_path($PathA) && test_path($PathB)

    $hA = (Get-FileHash -Algorithm SHA256 -Path $PathA).hash
    $hB = (Get-FileHash -Algorithm SHA256 -Path $PathB).hash

    $diff = diff $hA $hB

    if ($diff.count) {
        echo("NO MATCH!")
        echo("$hA - $PathA")
        echo("$hB - $PathB")
    } else {
        echo("Match: $hA")
    }sha
}

main
