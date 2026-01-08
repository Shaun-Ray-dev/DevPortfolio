# param(
#     $Path
# )
# New-Item $Path
# Write-Host "File $Path was created"

# Param(
#     $Path
# )
# If (-Not $Path -eq '') {
#     New-Item $Path
#     Write-Host "File created at $Path"
# } Else {
#     Write-Error "Path cannot be empty"
# }

# Param (
#     [Parameter(Mandatory)]
#     $Path
# )
# New-Item $Path
# Write-Host "File created at path $Path"

# Param (
#     [Parameter(Mandatory, HelpMessage = "Please provide a valid path")]
#     $Path
# )
# New-Item $Path
# Write-Host "File created at path $Path"

Param (
    [Parameter(Mandatory, HelpMessage = "Please provide a valid path")]
    [string]$Path
)
New-Item $Path
Write-Host "File created at path $Path"