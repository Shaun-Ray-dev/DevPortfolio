$targetFolder = ".\scraped_files"

if (-not (Test-Path $targetFolder)) {
    New-Item -Path $targetFolder -ItemType Directory
}

Write-Host "Enter URLs to download files from. Type 'done' when finished.`n"

$urls = @()
while ($true) {
    $inputUrl = Read-Host "Enter a URL"
    if ($inputUrl -eq "done") { break }
    if (![string]::IsNullOrWhiteSpace($inputUrl)) { $urls += $inputUrl }
}

if ($urls.Count -eq 0) {
    Write-Host "No URLs entered. Exiting."
    exit
}

foreach ($url in $urls) {
    try {
        $fileName = Split-Path $url -Leaf
        if ([string]::IsNullOrEmpty($fileName)) {
            $fileName = ($url -replace "[^a-zA-Z0-9]", "_")
        }

        $filePath = Join-Path $targetFolder $fileName
        Invoke-WebRequest -Uri $url -OutFile $filePath -UseBasicParsing
        Write-Host "Downloaded $fileName"
    } catch {
        Write-Host "Failed to download $url"
    }
}

Write-Host "`nAll files downloaded to $targetFolder"
