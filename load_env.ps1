# Read .env file and set environment variables
Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*$") { continue }  # Ignore empty lines
    $var = $_ -split '='
    if ($var.Length -eq 2) {
        [System.Environment]::SetEnvironmentVariable($var[0], $var[1])
    }
}