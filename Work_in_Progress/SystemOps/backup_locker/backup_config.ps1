$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackupFolder = Join-Path $ScriptRoot "..\backup_locker\backups"


If (!(Test-Path $BackupFolder)) { 
    New-Item -ItemType Directory -Path $BackupFolder | Out-Null
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$BackupPath = "$BackupFolder\config_$Timestamp.txt"

"New backup created on $Timestamp" | Out-File -FilePath $BackupPath

Write-Output "Backup saved to $BackupPath"
