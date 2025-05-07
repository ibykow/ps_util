param($path = "./")
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

function Show-DirLength([string]$name, [double]$len) {

    $color = "Black"
    $size = Format-FileLength($len)

    if ($len -ge 1TB) {
        $color = "White"
    } elseif ($len -ge 100GB) {
        $color = "Gray"
    } elseif ($len -ge 10GB) {
        $color = "Green"
    } elseif ($len -ge 4GB) {
        $color = "DarkRed"
    } elseif ($len -ge 800MB) {
        $color = "Red"
    } elseif ($len -ge 300MB) {
        $color = "DarkGray"
    }

    Write-Host -NoNewLine -ForegroundColor $color "$size `t"
    Write-Host $name
}

function Get-DirLength {
    param($path = "./")

    return (Get-ChildItem $path -Force -Recurse -ErrorAction SilentlyContinue | 
        Measure-Object -Property Length -Sum -ErrorAction Stop).Sum
}

function Get-DirSizes {
    param($path = "./")

    $total = 0

    $ret = @()

    Get-ChildItem $path -Force -Directory | ForEach-Object {
        $name = $_.FullName
        $len = Get-DirLength($name)

        Show-DirLength $name $len
        
        $total += $len

        $ret += @{
            Path = $_
            Length = $len
        }
    }

    Write-Host "" "Total:"
    Show-DirLength $path $total

    return $ret
}

Get-DirSizes $path
