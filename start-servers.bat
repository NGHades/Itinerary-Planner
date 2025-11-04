@echo off
echo Starting WanderTrip Application...
echo.

echo Starting Backend Server (Flask on port 8080)...
start "Backend Server" cmd /k "cd /d backend && python main.py"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server (HTTP on port 8000)...
start "Frontend Server" cmd /k "cd /d frontend && python -m http.server 8000"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8080
echo Frontend: http://localhost:8000
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:8000

echo.
echo Application is now running!
echo Close the terminal windows to stop the servers.
pause