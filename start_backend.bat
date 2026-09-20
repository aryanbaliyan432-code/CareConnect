@echo off
title CareConnect — Backend Server
color 0B

echo ============================================
echo   CareConnect Backend
echo ============================================
echo.

:: Check MongoDB
echo [1/3] Checking MongoDB...
sc query MongoDB >nul 2>&1
if %errorlevel% == 0 (
    net start MongoDB >nul 2>&1
    echo       MongoDB service started.
) else (
    echo       MongoDB service not found.
    echo       Trying to start mongod directly...
    start /min "" "C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe" --dbpath "%USERPROFILE%\data\db" 2>nul
    start /min "" "C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe" --dbpath "%USERPROFILE%\data\db" 2>nul
    start /min "" "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "%USERPROFILE%\data\db" 2>nul
    start /min "" "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath "%USERPROFILE%\data\db" 2>nul
    start /min "" "C:\Program Files\MongoDB\Server\5.0\bin\mongod.exe" --dbpath "%USERPROFILE%\data\db" 2>nul
    timeout /t 2 /nobreak >nul
    echo       If MongoDB is not installed, get it from:
    echo       https://www.mongodb.com/try/download/community
    echo.
)

:: Create MongoDB data directory if needed
if not exist "%USERPROFILE%\data\db" mkdir "%USERPROFILE%\data\db"

echo [2/3] Installing/checking Python packages...
python -m pip install -r backend\requirements.txt -q --no-warn-script-location

echo [3/3] Starting FastAPI server on http://localhost:8000
echo.
echo  API Docs: http://localhost:8000/docs
echo  Press Ctrl+C to stop
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir backend

pause
