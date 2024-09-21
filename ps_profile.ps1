# Functions

function ll {
	return Get-ChildItem -Force @args
}


function lsl ($p='./') { 
	return ll $p `
		| Get-Item -stream * -ErrorAction SilentlyContinue `
		| ForEach-Object { if($_.stream -ne ':$DATA') {$_.PSChildName} }
}


# ls | Get-Item -ErrorAction SilentlyContinue -stream * | ? { $_.stream -ne ':$DATA' }
function lslcat($p) {
	return lsl $p | ForEach-Object {
		write-host -nonewline "### " $_ " ###`n"; Get-Content $_; Write-Output "###" "" 
	}
}


# find-duplicates ./, .\a\ | tee -Var dupes
function find-duplicates {
	Param(
		[Array] $paths = './',
		[switch] $r=$False
	)

	return ll -File -Recurse:$r -Path $paths `
		| Group-Object -Property Length `
		| Where-Object { $_.Count -gt 1 } `
		| ForEach-Object { $_.Group } `
		| Get-FileHash `
		| Group-Object -Property Hash `
		| Where-Object { $_.Count -gt 1 } `
		| Select-Object -ExpandProperty Group `
		| Sort-Object -Property Hash -Unique `
		| Select-Object -Property Path
}


function find-file {
	Param([
		Parameter(Mandatory)]
		[String] $pattern,
		[String] $path
	)

	return ll -Path $path -Filter $pattern -Recurse -ErrorAction SilentlyContinue | 
		Format-Wide FullName -Column 1
}


function search {
	Param([
		Parameter(Mandatory)]
		[String] $pattern,
		[String] $path,
		[switch] $f=$False
	)

	if ($f) {
		# echo "woop"
		return find-file $pattern $path
	}

	return ll -Path $path -Recurse -ErrorAction SilentlyContinue |
		Select-String $pattern -List -ErrorAction SilentlyContinue | 
		ForEach-Object { return $_.Path + ":" + $_.LineNumber }
}


function path2filename() {
	Param(
        [String] $inputString,
        [String] $joinString = '-'
    )

    return $inputString.Split([IO.Path]::GetInvalidFileNameChars()) -join $joinString
}


function datestamp() {
	return Get-Date -Format yyyy-MM-dd
}


function datefile() {
	# Returns a given filename prepended with the current date.
	# Example:
	# nvim $(datefile foo.txt) # Opens a file named 2023-03-09-foo.txt
	Param([String] $filename)

	return "$(Get-Date -Format yyyy-MM-dd)-$filename"
}


function ReExtension() {
	# Usage: rextension old_extension new_extension
	# Rename one extension to another for each file in the current working directory
	#
	# Example: rextension txt rtf
	# Changes all text files to rich text files in the current working directory.
	Param([String] $SrcExt, [String] $DstExt)

	return ll "*.$SrcExt" `
		| Rename-Item -NewName { $_.Name -Replace ".$SrcExt", ".$DstExt" }
}


function GetPath {
	return Split-Path -Leaf -Path (Get-Location)
}


#Set Window Title
function SetTitle {
	Param($T=(GetPath))
	$Host.UI.RawUI.WindowTitle = $T
}


function Which ($Command) {
	$out = (($full = Get-Command -Name $Command -ErrorAction SilentlyContinue) |
		Select-Object -ExpandProperty Path -ErrorAction SilentlyContinue)

	return $out ? $out : $full
}


function cdwhich ($cmd) {
	return Set-Location (ll (Get-Command $cmd).path).directory
}


function Fdiff ($a, $b) {
	return Compare-Object (Get-Content $a) (Get-Content $b)
}


# Aliases
Set-Alias -Name ls -Value ll -Force
Set-Alias -Name grep -Value Select-String
