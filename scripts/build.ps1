$repoPath = Join-Path $PSScriptRoot "..\repo"
Set-Location $repoPath

Write-Host "=== BUILD ===" -ForegroundColor Yellow

# --------------------
# VENV
# --------------------
if (!(Test-Path ".venv")) {
    Write-Host "Creating venv..."
    python -m venv .venv
}

# activate venv
& ".venv\Scripts\Activate.ps1"

# --------------------
# INSTALL DEPS
# --------------------
Write-Host "Installing requirements..."
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "pip install failed" -ForegroundColor Red
    exit 1
}

# --------------------
# PREFLIGHT (TWÓJ CI CHECK)
# --------------------
Write-Host "Running preflight..."

python scripts/preflight.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Preflight FAILED" -ForegroundColor Red
    exit 1
}

Write-Host "BUILD OK" -ForegroundColor Green