param(
    [string]$ProcessName = "notepad"
)

$proc = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue

if ($proc) {
    Write-Output "$ProcessName is running."
} else {
    Write-Output "$ProcessName is NOT running!"
    [System.Windows.Forms.MessageBox]::Show("$ProcessName is not running!", "Process Monitor Alert")
}