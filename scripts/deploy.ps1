$repoPath = Join-Path $PSScriptRoot "..\repo"
Set-Location $repoPath

Write-Host "=== DEPLOY ===" -ForegroundColor Yellow

& ".venv\Scripts\Activate.ps1"

# 🚀 START BOT
Write-Host "Starting bot..."

python -m src.bootstrap.bot