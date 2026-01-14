@echo off
echo 🏋️ AI Fitness Trainer - Installation and Setup
echo ==============================================

echo Installing dependencies...
pip install opencv-python mediapipe numpy streamlit

echo.
echo ✅ Dependencies installed successfully!
echo.
echo Choose an option:
echo 1. Run Desktop Version (OpenCV)
echo 2. Run Web Version (Streamlit)
echo 3. Run Both
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Desktop Version...
    python run_fitness_trainer.py
) else if "%choice%"=="2" (
    echo Starting Web Version...
    streamlit run web_interface.py
) else if "%choice%"=="3" (
    echo Starting both versions...
    start cmd /k "python run_fitness_trainer.py"
    timeout /t 3
    streamlit run web_interface.py
) else (
    echo Invalid choice. Please run again.
    pause
)