#!/usr/bin/env python3
"""
WanderTrip Main Entry Point
Starts the Flask API server using the backend package
"""

from backend import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)