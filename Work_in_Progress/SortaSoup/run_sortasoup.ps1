Set-Location $PSScriptRoot

Write-Host "=== SortaSoup Pipeline Starting ==="

$Url = Read-Host "Enter a URL to scrape"
if (-not $Url) {
    Write-Host "No URL provided. Exiting."
    exit 1
}

Write-Host "[1/3] Running PowerShell scraper..."
& ".\psh_util\web_scraper.ps1" -Url $Url

Write-Host "[2/3] Processing HTML with Bash..."
bash "./bsh_util/process_scraped_html.sh"

Write-Host "[3/3] Parsing and organizing with Python..."
python "./pys_util/parse_and_organize.py"

Write-Host "=== SortaSoup Pipeline Complete ==="
