# Intervista - One-Click Startup Script
# This script starts both Django backend and React frontend

Write-Host "🚀 Starting Intervista - AI-Powered Interview Platform" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found. Please run this script from the project root directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\activate")) {
    Write-Host "❌ Error: Virtual environment not found. Please create it first with: python -m venv venv" -ForegroundColor Red
    exit 1
}

# Check if frontend directory exists
if (-not (Test-Path "frontend\package.json")) {
    Write-Host "❌ Error: Frontend directory not found. Please ensure the frontend folder exists." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Starting Django Backend Server..." -ForegroundColor Yellow
# Start Django server in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; venv\Scripts\activate; Write-Host '🐍 Django Backend Starting...' -ForegroundColor Green; python manage.py runserver"

# Wait a moment for Django to start
Start-Sleep -Seconds 3

Write-Host "✅ Starting React Frontend Server..." -ForegroundColor Yellow
# Start React server in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host '⚛️ React Frontend Starting...' -ForegroundColor Blue; npm run dev"

# Wait a moment for React to start
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "🎉 Intervista is starting up!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "📱 Frontend: http://localhost:5174" -ForegroundColor White
Write-Host "🔧 Backend:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "⚙️  Admin:    http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   • Add job roles through the admin panel" -ForegroundColor Gray
Write-Host "   • Select a job role to start practicing" -ForegroundColor Gray
Write-Host "   • Close both terminal windows to stop the servers" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to exit this script (servers will continue running)..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

