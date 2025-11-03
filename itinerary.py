import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv


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
    Please structure the answer day by day.
    """


prompt = build_prompt(destination, days, pace, has_car, pois)


# --- 5. CALL GEMINI ---
def generate_itinerary(prompt) -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(f"You are a travel itinerary planner.\n{prompt}")
    return response.text


itinerary = generate_itinerary(prompt)

print("=== Generated Itinerary ===")
print(itinerary)
