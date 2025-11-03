"""
WanderTrip Backend Package
AI-powered travel itinerary planning service

This package provides core functionality for:
- AI-generated travel itineraries using Gemini
- Points of interest discovery via OpenTripMap
- Flask REST API for frontend integration
- Geographic location services
"""

__version__ = "1.0.0"
__author__ = "WanderTrip Team"

# Import key functions to make them available at package level
from .itinerary_service import generate_itinerary, build_prompt
from .main import create_app

# Define public API
__all__ = [
    'generate_itinerary',
    'build_prompt', 
    'create_app',
    '__version__',
    '__author__'
]