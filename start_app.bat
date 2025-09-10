@echo off
echo 🚀 Starting Intervista - AI-Powered Interview Platform
echo =================================================

REM Check if manage.py exists
if not exist "manage.py" (
    echo ❌ Error: manage.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Error: Virtual environment not found. Please create it first.
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend\package.json" (
    echo ❌ Error: Frontend directory not found.
    pause
    exit /b 1
)

echo ✅ Starting Django Backend Server...
start "Django Backend" cmd /k "venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo ✅ Starting React Frontend Server...
start "React Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo 🎉 Intervista is starting up!
echo =================================================
echo 📱 Frontend: http://localhost:5174
echo 🔧 Backend:  http://127.0.0.1:8000
echo ⚙️  Admin:    http://127.0.0.1:8000/admin
echo.
echo 💡 Tips:
echo    • Add job roles through the admin panel
echo    • Select a job role to start practicing
echo    • Close both terminal windows to stop the servers
echo.
pause

