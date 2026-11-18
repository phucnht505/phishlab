$ErrorActionPreference = "Stop"

$ProjectRoot = $PSScriptRoot
$Python = (Get-Command py -ErrorAction Stop).Source

# Start server only if port 5500 is not being used
$Listener = Get-NetTCPConnection `
    -LocalPort 5500 `
    -State Listen `
    -ErrorAction SilentlyContinue

if (-not $Listener) {
    Start-Process `
        -FilePath $Python `
        -ArgumentList "-V:3.14 -m http.server 5500 --bind 127.0.0.1" `
        -WorkingDirectory $ProjectRoot `
        -WindowStyle Minimized
}

Write-Host "PhishLab HTTP Server started." -ForegroundColor Green
Write-Host "http://127.0.0.1:5500"