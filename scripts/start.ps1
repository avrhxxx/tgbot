$repoUrl = "https://github.com/avrhxxx/tgbot.git"
$branch = "bot"
$repoPath = Join-Path $PSScriptRoot "..\repo"

Write-Host "=== START ===" -ForegroundColor Yellow

# --------------------
# GIT CLONE / UPDATE
# --------------------
if (!(Test-Path $repoPath)) {
    Write-Host "Cloning repo..."
    git clone -b $branch $repoUrl $repoPath
} else {
    Write-Host "Updating repo..."
    Set-Location $repoPath
    git checkout $branch
    git pull
    Set-Location $PSScriptRoot
}

Write-Host "Repo ready"

# --------------------
# BUILD
# --------------------
& "$PSScriptRoot\build.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed" -ForegroundColor Red
    exit 1
}

# --------------------
# DEPLOY
# --------------------
& "$PSScriptRoot\deploy.ps1"