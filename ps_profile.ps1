# & { param($t, $p) ls -r -ea ig -pa $p -fi $t } *jackson*
# & { param($t, $p) return (ls -r -ea ig -pa $p -fi $t).fullname } de*
function find-file {
	param([
		Parameter(Mandatory)]
		[String] $pattern,
		[String] $path
	)

	return Get-ChildItem -Path $path -Filter $pattern -Recurse -ErrorAction SilentlyContinue -Force | 
		Format-Wide FullName -Column 1
}

# & { param($t) ls -r | sls $t -List -ea si | %{ return $_.Path + ":" + $_.LineNumber } } "Hello"
function search {
	param([
		Parameter(Mandatory)]
		[String] $pattern,
		[String] $path,
		[switch] $f=$False
	)

	if ($f) {
		# echo "woop"
		return find-file $pattern $path
	}

	return Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue |
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
	Get-ChildItem "*.$SrcExt" | Rename-Item -NewName { $_.Name -Replace ".$SrcExt", ".$DstExt" }
}

function GetPath {
	Split-Path -leaf -path (Get-Location)
}

# Add Appx
# & { $ProgressPreference = 'Ignore'; Import-Module -UseWindowsPowerShell Appx 3>$null }
#$PSDefaultParameterValues['Import-Module:UseWindowsPowerShell'] = { 
#	if ((Get-PSCallStack)[1].Position.Text -match '\bAppX\b') {
#		$true
#	} 
#} 

#Set Window Title
function SetTitle {
	Param($T=(GetPath))
	#Param($T=(Split-Path -leaf -path (Get-Location)))
	$Host.UI.RawUI.WindowTitle = $T
}

function Which ($Command) {
	$out = (($full = Get-Command -Name $Command -ErrorAction SilentlyContinue) |
		Select-Object -ExpandProperty Path -ErrorAction SilentlyContinue)

	return $out ? $out : $full
}

function cdwhich ($cmd) {
	cd (ls (gcm $cmd).path).directory
}


function Fdiff ($a, $b) {
	Compare-Object (Get-Content $a) (Get-Content $b)
}

# Alias functions
function lsal { return Get-ChildItem -Force @args }

# function lsl($p='./') { 
# 	(lsal $p | get-item -stream * -ErrorAction SilentlyContinue | 
# 		? { $_.stream -ne ':$DATA'} | % { "$($_.Filename):$($_.Stream)" }) 2>$null
# }

function lsl($p='./') { 
	# % { Write-Output "$($_.Filename):$($_.Stream)" 
	return lsal $p | get-item $_.FullName -stream * -ErrorAction SilentlyContinue | % { if($_.stream -ne ':$DATA') {$_.PSChildName} }
}


# ls | get-item -ErrorAction SilentlyContinue -stream * | ? { $_.stream -ne ':$DATA' }
function lslcat($p) {
	lsl $p | % { write-host -nonewline "### " $_ " ###`n"; cat $_; echo "###" "" }
}

# Aliases
set-alias -Name ls -Value lsal -force
Set-Alias -Name grep -Value Select-String
