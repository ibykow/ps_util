# Functions

function ll {
	return Get-ChildItem -Force @args
}


function ls-streams($p = './') { 
	ll $p `
	| Get-Item -stream * -ErrorAction SilentlyContinue `
	| where stream -ne ':$DATA'
	| select stream, pschildname, length, filename
}


# ls | Get-Item -ErrorAction SilentlyContinue -stream * | ? { $_.stream -ne ':$DATA' }
function cat-streams($p) {
	ll $p `
	| Get-Item -stream * -ErrorAction SilentlyContinue `
	| where stream -ne ':$DATA'
	| select pspath
	| convert-path
	| % { 
		echo $_
		gc $_ 
		echo ''
	}
}

function find-size-duplicates {
	Param(
		[Array] $paths = './',
		[switch] $r = $False
	)

	Get-ChildItem -Force -File -Recurse:$r -Path $paths `
	| Group-Object -Property Length `
	| Where-Object { $_.Count -gt 1 } `
	| Select-Object -ExpandProperty Group
}


# find-duplicates ./, .\a\ | tee -Var dupes
function find-duplicates {
	Param(
		[Array] $paths = './',
		[switch] $r = $False,
		[switch] $n = $False
	)

	if ($n) {
		return find-size-duplicates $paths $r | Select-Object -Property Length, FullName
	}
	
	# find-size-duplicates $paths $r
	find-size-duplicates $paths $r | Get-FileHash `
	| Group-Object -Property Hash `
	| Where-Object { $_.Count -gt 1 } `
	| Select-Object -ExpandProperty Group
	# | ForEach-Object { $_.Group.Path[0] }
}


function find-file {
	Param([
		Parameter(Mandatory)]
		[String] $pattern,
		[String] $path
	)

	Get-ChildItem -Force -Path $path -exclude .git -Filter $pattern -Recurse -ErrorAction SilentlyContinue | 
	Format-Wide FullName -Column 1
}


function search {
	Param([
		Parameter(Mandatory)]
		[String] $pattern,
		[String] $path,
		[switch] $f = $False
	)

	if ($f) {
		# echo "woop"
		return find-file $pattern $path
	}

	Get-ChildItem -Force -Path $path -Recurse -ErrorAction SilentlyContinue |
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
	Param($T = (GetPath))
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

function mkcd {
	Param([
		Parameter(Mandatory)]
		[String] $path
	)
	cd (mkdir -force $path)
}



# Aliases
# Set-Alias -Name ls -Value ll -Force
Set-Alias -Name grep -Value Select-String


# $PSDefaultParameterValues = @{‘Get-ChildItem:Force’ = $True}

SetTitle
