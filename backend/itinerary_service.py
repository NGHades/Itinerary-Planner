"""
WanderTrip Itinerary Service
Core business logic for AI-powered travel itinerary generation
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from .utils import geocode_city, get_pois

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def build_prompt(destination, days, pace, has_car, pois, month="November"):
    """
    Build a comprehensive prompt for AI itinerary generation
    
    Args:
        destination (str): Travel destination city
        days (int): Number of days for the trip
        pace (str): Travel pace - 'slow', 'moderate', or 'fast'
        has_car (bool): Whether traveler has a car available
        pois (list): List of points of interest from OpenTripMap
        month (str): Month of travel
    
    Returns:
        str: Formatted prompt for AI model
    """
    poi_list = ", ".join([poi["name"] for poi in pois if poi["name"]])
    
    return f"""
    Create a {days}-day travel itinerary for {destination} in {month}.
    Traveler pace: {pace}.
    Transportation: {"car" if has_car else "no car, public transit/walking"}.
    Suggested POIs include: {poi_list}.
    
    IMPORTANT: Return your response as a valid JSON object with the following structure:
    
    {{
        "destination": "{destination}",
        "startDate": "Feb 7, 2025",
        "days": [
            {{
                "dayNumber": 1,
                "date": "Feb 7, 2025",
                "periods": {{
                    "morning": [
                        {{
                            "time": "08:00",
                            "activity": "Breakfast and get ready",
                            "description": "Start the day with a hearty breakfast",
                            "id": "day1_morning_0"
                        }},
                        {{
                            "time": "10:00",
                            "activity": "Visit Museum",
                            "description": "Explore local history and culture",
                            "id": "day1_morning_1"
                        }}
                    ],
                    "afternoon": [
                        {{
                            "time": "14:00",
                            "activity": "Lunch and get ready for the next destination",
                            "description": "Enjoy local cuisine",
                            "id": "day1_afternoon_0"
                        }}
                    ],
                    "evening": [
                        {{
                            "time": "19:00",
                            "activity": "Stroll along the famous avenue",
                            "description": "Enjoy the evening atmosphere",
                            "id": "day1_evening_0"
                        }}
                    ]
                }}
            }}
        ],
        "additionalActivities": [
            {{
                "id": "extra_activity_0",
                "activity": "Shopping at Local Market",
                "description": "Browse local crafts and souvenirs",
                "duration": "1-2 hours",
                "type": "additional"
            }}
        ]
    }}
    
    Generate realistic activities with specific times, engaging descriptions, and include 10-15 additional activities that users can drag and drop into their schedule. Make sure the JSON is valid and properly formatted.
    """


def generate_itinerary(prompt) -> dict:
    """
    Generate travel itinerary using Google's Gemini AI
    
    Args:
        prompt (str): Formatted prompt for AI model
    
    Returns:
        dict: Structured itinerary data or error fallback
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"You are a travel itinerary planner. {prompt}")
        
        # Clean the response text to extract JSON
        response_text = response.text.strip()
        
        # Remove markdown formatting if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        return json.loads(response_text.strip())
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response.text}")
        # Return a fallback structure if JSON parsing fails
        return {
            "destination": "Unknown",
            "startDate": datetime.now().strftime("%b %d, %Y"),
            "days": [],
            "additionalActivities": [],
            "error": "Failed to parse JSON response from AI"
        }
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return {
            "destination": "Unknown",
            "startDate": datetime.now().strftime("%b %d, %Y"),
            "days": [],
            "additionalActivities": [],
            "error": f"Error generating itinerary: {str(e)}"
        }


def create_itinerary(destination, days=3, pace="moderate", has_car=True, month="November"):
    """
    High-level function to create a complete itinerary
    
    Args:
        destination (str): Travel destination
        days (int): Number of days
        pace (str): Travel pace
        has_car (bool): Transportation availability
        month (str): Month of travel
    
    Returns:
        dict: Complete itinerary data
    """
    # Get location data
    lat, lon = geocode_city(destination)
    
    # Get points of interest
    pois = get_pois(lat, lon)
    
    # Build prompt and generate itinerary
    prompt = build_prompt(destination, days, pace, has_car, pois, month)
    itinerary_data = generate_itinerary(prompt)
    
    return itinerary_data