# WanderTrip Application Launcher (PowerShell)
# Starts both backend and frontend servers simultaneously

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "          🌍 WanderTrip Application Launcher 🌍" -ForegroundColor Cyan  
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Error: Please run this script from the WanderTrip project root directory" -ForegroundColor Red
    Write-Host "   Make sure both 'backend' and 'frontend' folders exist" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start backend server
Write-Host "🚀 Starting Backend Server (Flask on port 8080)..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location backend
    python main.py
}

# Wait for backend to initialize
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend server  
Write-Host "🚀 Starting Frontend Server (HTTP on port 8000)..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD  
    Set-Location frontend
    python -m http.server 8000
}

# Wait a moment for servers to start
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "🎉 Both servers are running!" -ForegroundColor Green
Write-Host "📍 Backend:  http://localhost:8080" -ForegroundColor Cyan
Write-Host "📍 Frontend: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

# Open browser
Write-Host "🌐 Opening application in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "ℹ️  Server Information:" -ForegroundColor Blue
Write-Host "   Backend Job ID: $($backendJob.Id)" -ForegroundColor Gray
Write-Host "   Frontend Job ID: $($frontendJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop the servers, press Enter or Ctrl+C" -ForegroundColor Yellow

try {
    Read-Host "Press Enter to stop all servers"
} catch {
    Write-Host "`n🛑 Stopping servers..." -ForegroundColor Red
}

# Clean up jobs
Write-Host "🛑 Stopping servers..." -ForegroundColor Red
Stop-Job $backendJob -ErrorAction SilentlyContinue
Stop-Job $frontendJob -ErrorAction SilentlyContinue
Remove-Job $backendJob -ErrorAction SilentlyContinue  
Remove-Job $frontendJob -ErrorAction SilentlyContinue

Write-Host "✅ Servers stopped" -ForegroundColor Green