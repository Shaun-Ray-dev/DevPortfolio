# ======= USER CONFIG =======
$TargetEmail = "test@outlook.com"
$KeywordsFile = Join-Path $PSScriptRoot "keywords.json"
$RejFolderName = "REJEX"
$DryRun = $true
# ============================

if (-not (Test-Path $KeywordsFile)) {
    Write-Error "keywords.json not found!"
    exit
}
$Json = Get-Content $KeywordsFile -Raw | ConvertFrom-Json
$Keywords = $Json.keywords

try {
    $Outlook = New-Object -ComObject Outlook.Application
    $Namespace = $Outlook.GetNamespace("MAPI")
    $Account = $Namespace.Folders.Item($TargetEmail)
    $Inbox = $Account.Folders.Item("Inbox")
} catch {
    Write-Error "Could not connect to Outlook or find account. Make sure Outlook is open and signed in."
    exit
}

$RejFolder = $Inbox.Folders | Where-Object { $_.Name -eq $RejFolderName }
if (-not $RejFolder) {
    $RejFolder = $Inbox.Folders.Add($RejFolderName)
    Write-Host "Created folder '$RejFolderName'"
}

$Inbox.Items | Sort-Object ReceivedTime -Descending | ForEach-Object {
    $Mail = $_
    if ($Mail.MessageClass -eq "IPM.Note") {
        foreach ($Kw in $Keywords) {
            if ($Mail.Subject -match [regex]::Escape($Kw) -or $Mail.Body -match [regex]::Escape($Kw)) {
                if ($DryRun) {
                    Write-Host "[DRY-RUN] Would move email: $($Mail.Subject)"
                } else {
                    Write-Host "Moving email: $($Mail.Subject)"
                    $Mail.Move($RejFolder)
                }
                break
            }
        }
    }
}
