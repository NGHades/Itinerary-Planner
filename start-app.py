#!/usr/bin/env python3
"""
WanderTrip Application Launcher
Starts both backend and frontend servers simultaneously
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("          🌍 WanderTrip Application Launcher 🌍")
    print("=" * 60)
    print()

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Backend Server (Flask on port 8080)...")
    backend_path = Path("backend")
    
    if not backend_path.exists():
        print("❌ Backend directory not found!")
        return None
    
    try:
        # Start backend server
        backend_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=backend_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("✅ Backend server started")
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend HTTP server"""
    print("🚀 Starting Frontend Server (HTTP on port 8000)...")
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        return None
    
    try:
        # Start frontend server
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000"],
            cwd=frontend_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("✅ Frontend server started")
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    print_banner()
    
    # Start backend server
    backend_process = start_backend()
    if not backend_process:
        input("Press Enter to exit...")
        return
    
    # Wait a moment for backend to initialize
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend server
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend, terminating backend...")
        backend_process.terminate()
        input("Press Enter to exit...")
        return
    
    print()
    print("🎉 Both servers are running!")
    print("📍 Backend:  http://localhost:8080")
    print("📍 Frontend: http://localhost:8000")
    print()
    
    # Open browser after a short delay
    print("🌐 Opening application in browser...")
    time.sleep(2)
    webbrowser.open("http://localhost:8000")
    
    print()
    print("ℹ️  To stop the servers:")
    print("   - Close the console windows that opened")
    print("   - Or press Ctrl+C in this window")
    print()
    
    try:
        input("Press Enter to stop all servers...")
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
    
    # Clean up processes
    try:
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")
    except:
        print("⚠️  Some processes may still be running")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")