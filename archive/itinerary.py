import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re
from datetime import datetime, timedelta


# --- CONFIG ---
load_dotenv()
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# --- 1. USER INPUTS (hardcoded for now) ---
destination = "Pasadena"
days = 3
pace = "moderate"
has_car = True
month = "November"


# --- 2. GEOCODE DESTINATION ---
def geocode_city(city_name):
    # Try OpenTripMap first, then fallback to a simpler approach
    url = f"https://api.opentripmap.com/0.1/en/places/geoname"
    params = {"name": city_name, "apikey": OPENTRIPMAP_API_KEY}
    
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        
        if resp.status_code == 200 and "lat" in data and "lon" in data:
            return data["lat"], data["lon"]
        else:
            # Fallback: Use a basic geocoding service or hardcoded coordinates
            print(f"Geocoding failed for {city_name}, using default coordinates for Pasadena, CA")
            # Pasadena, CA coordinates as fallback
            return 34.1478, -118.1445
            
    except Exception as e:
        print(f"Geocoding error: {e}, using default coordinates")
        return 34.1478, -118.1445


lat, lon = geocode_city(destination)


# --- 3. GET TOP POIs ---
def get_pois(lat, lon, radius=5000, limit=10):
    url = f"https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "radius": radius,
        "lon": lon,
        "lat": lat,
        "rate": 3,       # 1=low, 3=popular
        "limit": limit,
        "apikey": OPENTRIPMAP_API_KEY,
    }
    resp = requests.get(url, params=params).json()
    pois = []
    for place in resp.get("features", []):
        name = place["properties"]["name"]
        kinds = place["properties"].get("kinds", "")
        pois.append({"name": name, "type": kinds})
    return pois

pois = get_pois(lat, lon)


# --- 4. BUILD PROMPT ---
def build_prompt(destination, days, pace, has_car, pois):
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


# --- 5. CALL GEMINI ---
def generate_itinerary(prompt) -> dict:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(f"You are a travel itinerary planner. {prompt}")
    
    try:
        # Try to parse the response as JSON
        # Clean the response text to extract JSON
        response_text = response.text.strip()
        
        # Sometimes the model includes markdown formatting, so let's clean it
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
            "destination": destination,
            "startDate": "Feb 7, 2025",
            "days": [],
            "additionalActivities": [],
            "error": "Failed to parse JSON response from AI"
        }


# --- MAIN EXECUTION ---
prompt = build_prompt(destination, days, pace, has_car, pois)
itinerary_json = generate_itinerary(prompt)

print("=== Generated Itinerary (JSON) ===")
print(json.dumps(itinerary_json, indent=2))

# Save to a file for the frontend to use
with open('frontend/itinerary_data.json', 'w') as f:
    json.dump(itinerary_json, f, indent=2)

print(f"\nItinerary saved to frontend/itinerary_data.json")