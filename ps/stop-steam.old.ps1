# "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile "C:\Users\z\code\int\ps\stop-steam.ps1"
# "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -c "& {Stop-Process -name steam*}"
Stop-Process -Name steam* -Force