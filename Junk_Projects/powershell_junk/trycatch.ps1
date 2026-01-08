
# Try {
#    # Statement. For example, call a command.
#    # Another statement. For example, assign a variable.
# }


# try {
#     # do something with a file
# } Catch [System.IO.IOException] {
#     Write-Host "Something went wrong"
# } Catch {
#     # Catch all. Not an IOException but something else
# }


# Try {
#    # Do something with a file.
# } Catch [System.IO.IOException] {
#    Write-Host "Something went wrong"
# }  Catch {
#    # Catch all. It's not an IOException but something else.
# } Finally {
#    # Clean up resources.
# }

# Try {
#     # Do something with code
# } Catch [System.IO.IOException] {
#     Write-Host "Something IO went wrong: $($_.exception.message)"
# } Catch {
#     Write-Host "Something else went wrong: $($_.exception.message)"
# }


# Try {
#     Get-Content './file.txt' -ErrorAction Stop
# } Catch {
#     Write-Error "File can't be found"
# }


# Try {
#     If ($Path -eq './forbidden')
#     {
#         Throw "Path not allowed"
#     }
#     # Carry on.

# } Catch {
#     Write-Error "$($_.exception.message)" # Path not allowed
# }