function Format-FileLength {
    param([double]$len=0)

    if ($len -ge 1TB) {
        return "{0:N2} TB" -f ($len / 1TB)
    } elseif ($len -ge 1GB) {
        return "{0:N2} GB" -f ($len / 1GB)
    } elseif ($len -ge 1MB) {
        return "{0:N2} MB" -f ($len / 1MB)
    } elseif ($len -ge 1KB) {
        return "{0:N2} KB" -f ($len / 1KB)
    } else {
        return "$($len) bytes"
    }
}

function Show-FileLength([string]$name, [double]$len) {
    $color = "Black"
    $size = Format-FileLength($len)

    if ($len -ge 1TB) {
        $color = "DarkRed"
    } elseif ($len -ge 100GB) {
        $color = "Red"
    } elseif ($len -ge 10GB) {
        $color = "Green"
    } elseif ($len -ge 4GB) {
        $color = "White"
    } elseif ($len -ge 800MB) {
        $color = "Gray"
    } elseif ($len -ge 300MB) {
        $color = "DarkGray"
    }

    Write-Host -NoNewLine -ForegroundColor $color "$size `t"
    Write-Output $name
}

function List-Files {
    param([string]$path = "./", [double]$min=1GB)

    $cols = (Get-Host).UI.RawUI.MaxWindowSize.Width - 5
    $blank = " " * $cols
    $check_str = "Checking "
    $cols -= $check_str.length

    Get-ChildItem $path -Force -Recurse -ErrorAction SilentlyContinue | % {
        $name = $_.FullName

        if ($name.length -ge $cols) {
            $name = $name.substring(0, $cols - 3) + "..."
        }

        if ($_.Length -ge $min) {
            Write-Host -NoNewLine "`r" $blank "`r"
            Show-FileLength $_.FullName $_.length
        } else {
            Write-Host -NoNewLine "`r" $blank "`r"
            Write-Host -NoNewLine $check_str $name
        }
    }

    Write-Host -NoNewLine "`r" $blank "`r"
}


$path = './'
$min = 1MB

$a = $args

switch($a.length) {
    0 { Break; }
    1 { if($a[0] -is [string]) {
        $path = $a[0] 
    } else { 
        $min = $a[0] 
    }; break }
    default { $path = $a[0]; $min = $a[1] }
}

List-Files $path $min