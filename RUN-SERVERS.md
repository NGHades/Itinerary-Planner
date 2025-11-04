# WanderTrip Development Commands

## Quick Start

```bash
# Option 1: Double-click the batch file (Windows)
start-servers.bat

# Option 2: Run the Python launcher
python start-app.py

# Option 3: Manual (original method)
# Terminal 1:
cd backend && python main.py

# Terminal 2:
cd frontend && python -m http.server 8000
```

## Development Servers

- **Backend (Flask)**: http://localhost:8080
- **Frontend (Static)**: http://localhost:8000

## Application Access

Once both servers are running, open: http://localhost:8000

## Environment Setup

Make sure you have a `.env` file in the project root with:

```
GEMINI_API_KEY=your_gemini_api_key_here
OPENTRIPMAP_API_KEY=your_opentripmap_api_key_here
```

## Stopping Servers

- **Batch Method**: Close the console windows that open
- **Python Method**: Press Enter or Ctrl+C in the launcher
- **Manual Method**: Press Ctrl+C in each terminal
