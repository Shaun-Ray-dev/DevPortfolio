param (
    [Parameter(Mandatory=$true)]
    [string]$Url
)

$BaseDir = Resolve-Path "$PSScriptRoot\.."
$ScrapedDir = Join-Path $BaseDir "scraped_files"
New-Item -ItemType Directory -Force -Path $ScrapedDir | Out-Null

Write-Host "Scraping $Url"

$response = Invoke-WebRequest -Uri $Url -UseBasicParsing
$htmlName = ($Url -replace '[^a-zA-Z0-9]', '_') + ".html"
$htmlPath = Join-Path $ScrapedDir $htmlName
$response.Content | Out-File -Encoding utf8 $htmlPath
Write-Host "Saved HTML: $htmlName"

$Uri = [System.Uri]$Url
foreach ($img in $response.Images) {
    $imgUrl = $img.src
    if (-not $imgUrl) { continue }

    if ($imgUrl -notmatch "^http") {
        $imgUrl = "$($Uri.Scheme)://$($Uri.Host)/$($imgUrl.TrimStart('/'))"
    }

    $imgName = [System.IO.Path]::GetFileName($imgUrl)
    $outPath = Join-Path $ScrapedDir $imgName

    try {
        Invoke-WebRequest -Uri $imgUrl -OutFile $outPath -UseBasicParsing
        Write-Host "Saved image: $imgName"
    } catch {
        Write-Host "Failed image: $imgUrl"
    }
}


