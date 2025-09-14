# Smart Soil Streamlit Launcher
Write-Host "🌱 Starting Smart Soil Streamlit Application..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check if Python is installed
try {
    python --version | Out-Null
    Write-Host "✅ Python is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install requirements
Write-Host "`n📦 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements_streamlit.txt

# Start Streamlit app
Write-Host "`n🚀 Starting Streamlit application..." -ForegroundColor Green
Write-Host "Your app will open in your default web browser." -ForegroundColor Cyan
Write-Host "If it doesn't open automatically, go to: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the application." -ForegroundColor Yellow
Write-Host ""

streamlit run streamlit_app.py
