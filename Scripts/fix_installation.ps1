# AI Fitness Trainer - Installation Fix Script
Write-Host "🏋️ AI Fitness Trainer - Installation Fix" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Yellow

# Check Python
Write-Host "`nChecking Python installation..." -ForegroundColor Cyan
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Cyan
$packages = @(
    "opencv-python",
    "mediapipe", 
    "numpy",
    "streamlit"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Gray
    pip install $package
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $package installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install $package" -ForegroundColor Red
    }
}

# Test imports
Write-Host "`nTesting imports..." -ForegroundColor Cyan
python -c "
try:
    import cv2
    print('✅ OpenCV imported')
    import mediapipe
    print('✅ MediaPipe imported') 
    import numpy
    print('✅ NumPy imported')
    import streamlit
    print('✅ Streamlit imported')
    print('`n🎉 All dependencies working!')
except ImportError as e:
    print(f'❌ Import error: {e}')
"

Write-Host "`n🚀 Starting AI Fitness Trainer (Desktop Version)..." -ForegroundColor Green
python .\run_fitness_trainer.py