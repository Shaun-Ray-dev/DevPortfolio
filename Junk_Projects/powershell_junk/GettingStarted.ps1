# write-output 'testing'


write-output "Today's date is $(Get-Date)"

$user = read-host -Prompt "Enter your name"
write-output "Today is the day $user began a PowerShell programming journey."