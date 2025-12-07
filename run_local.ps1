# Quick Setup and Run Script for Windows
# This script automates the setup and running of the application

Write-Host "🚀 Setting up Coding Questions Finder Application" -ForegroundColor Cyan
Write-Host "=" * 60

# Check if Python is installed
Write-Host "`n[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists
Write-Host "`n[2/6] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Could not activate virtual environment. Trying to continue..." -ForegroundColor Yellow
}

# Install dependencies
Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Setup database
Write-Host "`n[5/6] Setting up database..." -ForegroundColor Yellow
python setup_sqlite.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Database setup had issues, but continuing..." -ForegroundColor Yellow
} else {
    Write-Host "✅ Database ready" -ForegroundColor Green
}

# Check for .env file
Write-Host "`n[6/6] Checking environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    $apiKey = Read-Host "Enter your GOOGLE_API_KEY (or press Enter to skip)"
    if ($apiKey) {
        $env:GOOGLE_API_KEY = $apiKey
        Write-Host "✅ API key set for this session" -ForegroundColor Green
        Write-Host "💡 Tip: Create a .env file to save your API key permanently" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  No API key set. AI features will not work." -ForegroundColor Yellow
        Write-Host "   You can set it later with: `$env:GOOGLE_API_KEY = 'your_key'" -ForegroundColor Cyan
    }
}

# Check if GOOGLE_API_KEY is set
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "`n⚠️  WARNING: GOOGLE_API_KEY is not set!" -ForegroundColor Yellow
    Write-Host "   The application will run, but AI search features will not work." -ForegroundColor Yellow
    Write-Host "   Set it with: `$env:GOOGLE_API_KEY = 'your_key'" -ForegroundColor Cyan
}

# Start the application
Write-Host "`n" + "=" * 60
Write-Host "🎉 Setup complete! Starting application..." -ForegroundColor Green
Write-Host "=" * 60
Write-Host "`n📝 The application will be available at:" -ForegroundColor Cyan
Write-Host "   http://localhost:8080" -ForegroundColor White
Write-Host "`n💡 Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Run the application
python app.py

