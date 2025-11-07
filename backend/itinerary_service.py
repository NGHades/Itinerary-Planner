"""
WanderTrip Itinerary Service
Core business logic for AI-powered travel itinerary generation
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.geocoding import geocode_city
from utils.poi_service import get_pois

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("🔧 [ITINERARY_SERVICE] Module loaded")
print(f"🔧 [ITINERARY_SERVICE] GEMINI_API_KEY loaded: {'Yes' if GEMINI_API_KEY else 'No'}")

if not GEMINI_API_KEY:
    print("❌ [ITINERARY_SERVICE] CRITICAL: GEMINI_API_KEY environment variable is not set!")
    print("❌ [ITINERARY_SERVICE] Please check your .env file")

# Configure Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("🔧 [ITINERARY_SERVICE] Gemini API configured successfully")
except Exception as e:
    print(f"❌ [ITINERARY_SERVICE] Failed to configure Gemini API: {e}")


def build_prompt(destination, startDate, endDate, guestCount, pois):
    """
    Build a comprehensive prompt for AI itinerary generation
    
    Args:
        destination (str): Travel destination city
        startDate (str): Trip start date in YYYY-MM-DD format
        endDate (str): Trip end date in YYYY-MM-DD format  
        guestCount (int): Number of guests/travelers
        pois (list): List of points of interest from OpenTripMap
    
    Returns:
        str: Formatted prompt for AI model
    """
    # Calculate number of days from dates
    from datetime import datetime
    try:
        start_dt = datetime.strptime(startDate, '%Y-%m-%d')
        end_dt = datetime.strptime(endDate, '%Y-%m-%d')
        days = (end_dt - start_dt).days
        month = start_dt.strftime('%B')
        formatted_start_date = start_dt.strftime('%b %d, %Y')
    except ValueError:
        # Fallback if date parsing fails
        days = 3
        month = 'November'
        formatted_start_date = 'Feb 7, 2025'
    
    print(f"🎯 [BUILD_PROMPT] Called with: {destination}, {startDate} to {endDate} ({days} days), {guestCount} guests, month: {month}")
    print(f"🎯 [BUILD_PROMPT] POIs count: {len(pois) if pois else 0}")
    
    poi_list = ", ".join([poi["name"] for poi in pois if poi["name"]])
    print(f"🎯 [BUILD_PROMPT] POI list: {poi_list[:100]}...")
    
    # Set reasonable defaults for pace and transportation
    pace = 'moderate'  # Default since not collected from form
    has_car = True     # Default assumption
    
    prompt = f"""
    Create a {days}-day travel itinerary for {destination} in {month}.
    Traveler count: {guestCount} {'person' if guestCount == 1 else 'people'}.
    Traveler pace: {pace}.
    Transportation: {"car" if has_car else "no car, public transit/walking"}.
    Suggested POIs include: {poi_list}.
    
    IMPORTANT: Return your response as a valid JSON object with the following structure:
    
    {{
        "destination": "{destination}",
        "startDate": "{formatted_start_date}",
        "days": [
            {{
                "dayNumber": 1,
                "date": "{formatted_start_date}",
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
    
    print(f"🎯 [BUILD_PROMPT] Prompt created (length: {len(prompt)} chars)")
    return prompt


def generate_itinerary(prompt) -> dict:
    """
    Generate travel itinerary using Google's Gemini AI
    
    Args:
        prompt (str): Formatted prompt for AI model
    
    Returns:
        dict: Structured itinerary data or error fallback
    """
    print(f"🤖 [GENERATE_ITINERARY] Starting AI generation...")
    print(f"🤖 [GENERATE_ITINERARY] Prompt length: {len(prompt)} chars")
    
    try:
        print(f"🤖 [GENERATE_ITINERARY] Creating Gemini model...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print(f"🤖 [GENERATE_ITINERARY] Sending request to AI...")
        response = model.generate_content(f"You are a travel itinerary planner. {prompt}")
        
        print(f"🤖 [GENERATE_ITINERARY] AI response received")
        print(f"🤖 [GENERATE_ITINERARY] Raw response length: {len(response.text)} chars")
        print(f"🤖 [GENERATE_ITINERARY] Response preview: {response.text[:200]}...")
        
        # Clean the response text to extract JSON
        response_text = response.text.strip()
        print(f"🤖 [GENERATE_ITINERARY] Cleaning response text...")
        
        # Remove markdown formatting if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
            print(f"🤖 [GENERATE_ITINERARY] Removed ```json prefix")
        if response_text.startswith('```'):
            response_text = response_text[3:]
            print(f"🤖 [GENERATE_ITINERARY] Removed ``` prefix")
        if response_text.endswith('```'):
            response_text = response_text[:-3]
            print(f"🤖 [GENERATE_ITINERARY] Removed ``` suffix")
        
        print(f"🤖 [GENERATE_ITINERARY] Parsing JSON...")
        result = json.loads(response_text.strip())
        print(f"🤖 [GENERATE_ITINERARY] ✅ JSON parsed successfully!")
        print(f"🤖 [GENERATE_ITINERARY] Destination: {result.get('destination', 'Unknown')}")
        print(f"🤖 [GENERATE_ITINERARY] Days count: {len(result.get('days', []))}")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ [GENERATE_ITINERARY] JSON parsing error: {e}")
        print(f"❌ [GENERATE_ITINERARY] Raw response text:")
        print(f"❌ [GENERATE_ITINERARY] {response.text}")
        print(f"❌ [GENERATE_ITINERARY] Cleaned response text:")
        print(f"❌ [GENERATE_ITINERARY] {response_text}")
        # Return a fallback structure if JSON parsing fails
        return {
            "destination": "Unknown",
            "startDate": datetime.now().strftime("%b %d, %Y"),
            "days": [],
            "additionalActivities": [],
            "error": "Failed to parse JSON response from AI"
        }
    except Exception as e:
        print(f"❌ [GENERATE_ITINERARY] Error generating itinerary: {e}")
        print(f"❌ [GENERATE_ITINERARY] Error type: {type(e).__name__}")
        print(f"❌ [GENERATE_ITINERARY] Error details: {str(e)}")
        return {
            "destination": "Unknown",
            "startDate": datetime.now().strftime("%b %d, %Y"),
            "days": [],
            "additionalActivities": [],
            "error": f"Error generating itinerary: {str(e)}"
        }


def create_itinerary(destination, startDate, endDate, guestCount):
    """
    High-level function to create a complete itinerary
    
    Args:
        destination (str): Travel destination
        startDate (str): Trip start date in YYYY-MM-DD format
        endDate (str): Trip end date in YYYY-MM-DD format
        guestCount (int): Number of guests/travelers
    
    Returns:
        dict: Complete itinerary data
    """
    print(f"🏁 [CREATE_ITINERARY] Starting creation for {destination}")
    print(f"🏁 [CREATE_ITINERARY] Parameters: {startDate} to {endDate}, {guestCount} guests")
    
    # Get location data
    print(f"🏁 [CREATE_ITINERARY] Getting coordinates...")
    lat, lon = geocode_city(destination)
    print(f"🏁 [CREATE_ITINERARY] Coordinates: {lat}, {lon}")
    
    # Get points of interest
    print(f"🏁 [CREATE_ITINERARY] Getting POIs...")
    pois = get_pois(lat, lon)
    print(f"🏁 [CREATE_ITINERARY] Found {len(pois) if pois else 0} POIs")
    
    # Build prompt and generate itinerary
    print(f"🏁 [CREATE_ITINERARY] Building prompt...")
    prompt = build_prompt(destination, startDate, endDate, guestCount, pois)
    
    print(f"🏁 [CREATE_ITINERARY] Generating itinerary...")
    itinerary_data = generate_itinerary(prompt)
    
    print(f"🏁 [CREATE_ITINERARY] ✅ Itinerary creation complete!")
    return itinerary_data