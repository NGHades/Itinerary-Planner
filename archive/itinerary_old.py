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


prompt = build_prompt(destination, days, pace, has_car, pois)


# --- 5. CALL GEMINI ---
def generate_itinerary(prompt) -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(f"You are a travel itinerary planner.\n{prompt}")
    return response.text


# --- 6. PARSE ITINERARY TO JSON ---
def parse_itinerary_to_json(itinerary_text, destination, start_date="Feb 7, 2025"):
    """Parse the generated itinerary text into structured JSON format"""
    try:
        # Parse start date
        start = datetime.strptime(start_date, "%b %d, %Y")
        
        # Initialize the JSON structure
        itinerary_json = {
            "destination": destination,
            "startDate": start_date,
            "days": []
        }
        
        # Split by days
        day_sections = re.split(r'Day \d+', itinerary_text)
        day_matches = re.findall(r'Day (\d+)', itinerary_text)
        
        for i, day_match in enumerate(day_matches):
            if i + 1 < len(day_sections):
                day_content = day_sections[i + 1]
                day_number = int(day_match)
                current_date = start + timedelta(days=day_number - 1)
                
                day_data = {
                    "dayNumber": day_number,
                    "date": current_date.strftime("%b %d, %Y"),
                    "periods": {
                        "morning": [],
                        "afternoon": [],
                        "evening": []
                    }
                }
                
                # Parse activities by time period
                current_period = None
                lines = day_content.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line.lower().startswith('morning'):
                        current_period = 'morning'
                    elif line.lower().startswith('afternoon'):
                        current_period = 'afternoon'
                    elif line.lower().startswith('evening'):
                        current_period = 'evening'
                    elif line.startswith('-') and current_period:
                        # Parse activity line: "- 08:00 - Activity Name - Description"
                        activity_match = re.match(r'-\s*(\d{2}:\d{2})\s*-\s*([^-]+)(?:-\s*(.+))?', line)
                        if activity_match:
                            time = activity_match.group(1)
                            activity = activity_match.group(2).strip()
                            description = activity_match.group(3).strip() if activity_match.group(3) else ""
                            
                            activity_data = {
                                "time": time,
                                "activity": activity,
                                "description": description,
                                "id": f"day{day_number}_{current_period}_{len(day_data['periods'][current_period])}"
                            }
                            
                            day_data["periods"][current_period].append(activity_data)
                
                itinerary_json["days"].append(day_data)
        
        return itinerary_json
        
    except Exception as e:
        print(f"Error parsing itinerary: {e}")
        # Return a fallback structure
        return {
            "destination": destination,
            "startDate": start_date,
            "days": [],
            "error": str(e)
        }


# --- 7. GENERATE ADDITIONAL ACTIVITIES FOR SIDEBAR ---
def generate_additional_activities(destination, pois):
    """Generate additional activities that users can drag and drop"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    poi_list = ", ".join([poi["name"] for poi in pois if poi["name"]])
    
    prompt = f"""
    Generate 15-20 additional travel activities for {destination} that could be added to an itinerary.
    Include POIs like: {poi_list}
    
    Format each activity as:
    Activity Name - Brief description - Estimated duration
    
    Mix different types of activities: museums, restaurants, outdoor activities, shopping, cultural sites, etc.
    Keep descriptions concise (10-15 words max).
    """
    
    response = model.generate_content(prompt)
    activities = []
    
    lines = response.text.strip().split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line and not line.startswith('#'):
            # Remove bullet points or numbers
            line = re.sub(r'^[-•*\d+\.]\s*', '', line)
            
            # Parse activity format
            parts = line.split(' - ')
            if len(parts) >= 2:
                activity = {
                    "id": f"extra_activity_{i}",
                    "activity": parts[0].strip(),
                    "description": parts[1].strip() if len(parts) > 1 else "",
                    "duration": parts[2].strip() if len(parts) > 2 else "1-2 hours",
                    "type": "additional"
                }
                activities.append(activity)
    
    return activities


# --- 5. CALL GEMINI ---
def generate_itinerary(prompt) -> dict:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(f"You are a travel itinerary planner. {prompt}")
    
    try:
        # Try to parse the response as JSON
        import json
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


prompt = build_prompt(destination, days, pace, has_car, pois)
itinerary_json = generate_itinerary(prompt)

print("=== Generated Itinerary (JSON) ===")
print(json.dumps(itinerary_json, indent=2))

# Save to a file for the frontend to use
with open('itinerary_data.json', 'w') as f:
    json.dump(itinerary_json, f, indent=2)
