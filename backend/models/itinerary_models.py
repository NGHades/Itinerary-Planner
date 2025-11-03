"""
Data models for WanderTrip itinerary planning
Defines structured classes for travel data
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Location:
    """Represents a geographic location"""
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    region: Optional[str] = None


@dataclass 
class Activity:
    """Represents a single travel activity"""
    id: str
    name: str
    description: str
    time: str
    duration: Optional[str] = None
    activity_type: str = "general"
    location: Optional[Location] = None
    
    def to_dict(self) -> dict:
        """Convert activity to dictionary format"""
        return {
            "id": self.id,
            "activity": self.name,
            "description": self.description,
            "time": self.time,
            "duration": self.duration,
            "type": self.activity_type
        }


@dataclass
class DayPlan:
    """Represents activities for a single day"""
    day_number: int
    date: str
    morning: List[Activity]
    afternoon: List[Activity] 
    evening: List[Activity]
    
    def to_dict(self) -> dict:
        """Convert day plan to dictionary format"""
        return {
            "dayNumber": self.day_number,
            "date": self.date,
            "periods": {
                "morning": [activity.to_dict() for activity in self.morning],
                "afternoon": [activity.to_dict() for activity in self.afternoon],
                "evening": [activity.to_dict() for activity in self.evening]
            }
        }
    
    def get_all_activities(self) -> List[Activity]:
        """Get all activities for this day"""
        return self.morning + self.afternoon + self.evening


@dataclass
class Itinerary:
    """Represents a complete travel itinerary"""
    destination: str
    start_date: str
    days: List[DayPlan]
    additional_activities: List[Activity]
    
    def to_dict(self) -> dict:
        """Convert itinerary to dictionary format for JSON serialization"""
        return {
            "destination": self.destination,
            "startDate": self.start_date,
            "days": [day.to_dict() for day in self.days],
            "additionalActivities": [activity.to_dict() for activity in self.additional_activities]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Itinerary':
        """Create Itinerary instance from dictionary data"""
        days = []
        for day_data in data.get("days", []):
            morning = [Activity(**act) for act in day_data["periods"].get("morning", [])]
            afternoon = [Activity(**act) for act in day_data["periods"].get("afternoon", [])]
            evening = [Activity(**act) for act in day_data["periods"].get("evening", [])]
            
            day_plan = DayPlan(
                day_number=day_data["dayNumber"],
                date=day_data["date"],
                morning=morning,
                afternoon=afternoon,
                evening=evening
            )
            days.append(day_plan)
        
        additional_activities = [
            Activity(**act) for act in data.get("additionalActivities", [])
        ]
        
        return cls(
            destination=data["destination"],
            start_date=data["startDate"], 
            days=days,
            additional_activities=additional_activities
        )
    
    def get_total_activities(self) -> int:
        """Get total number of scheduled activities"""
        return sum(len(day.get_all_activities()) for day in self.days)
    
    def get_duration_days(self) -> int:
        """Get number of days in itinerary"""
        return len(self.days)