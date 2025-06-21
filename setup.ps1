# COVID-19 Analysis Project - PowerShell Auto Setup
# This script automatically sets up the virtual environment and runs the project

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  COVID-19 Analysis Project - Auto Setup" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check if Python is installed
if (-not (Test-Command "python")) {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[SETUP] Python found - checking version..." -ForegroundColor Green
python --version

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[SETUP] Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[SETUP] Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "[SETUP] Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "If you get execution policy errors, run:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install/upgrade dependencies
Write-Host "[SETUP] Installing dependencies..." -ForegroundColor Green
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! Running the project..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Run the project
python run.py all

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Project execution completed!" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now run individual activities using:" -ForegroundColor Green
Write-Host "  python run.py activity1" -ForegroundColor Yellow
Write-Host "  python run.py activity2" -ForegroundColor Yellow
Write-Host "  etc." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit" 