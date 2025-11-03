"""
Data models for WanderTrip itinerary planning

Contains classes and structures for representing:
- Travel itineraries
- Activities and attractions
- Day plans and schedules
- Location data
"""

from .itinerary_models import Itinerary, Activity, DayPlan, Location

__all__ = [
    'Itinerary',
    'Activity', 
    'DayPlan',
    'Location'
]