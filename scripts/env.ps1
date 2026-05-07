$repoPath = Join-Path $PSScriptRoot "..\repo"
Set-Location $repoPath

$envFile = ".env.local"

if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.+)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }

    Write-Host "ENV loaded"
} else {
    Write-Host "No .env.local found"
}