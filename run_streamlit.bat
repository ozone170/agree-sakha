@echo off
echo 🌱 Starting Smart Soil Streamlit Application...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Install requirements if needed
echo 📦 Installing requirements...
pip install -r requirements_streamlit.txt

REM Start Streamlit app
echo 🚀 Starting Streamlit application...
echo.
echo Your app will open in your default web browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application.
echo.

streamlit run streamlit_app.py

pause
