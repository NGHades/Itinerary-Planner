import os
import requests
import google.generativeai as genai

# --- CONFIG ---
OPENTRIPMAP_API_KEY = os.getenv("5ae2e3f221c38a28845f05b60f8887eacd3727cd6a9fd80fed39f192")
OPENAI_API_KEY = os.getenv("AIzaSyCdkF2khECub_ELYEk3m1htISTcp6gQ6ik")

genai.configure(api_key="AIzaSyCdkF2khECub_ELYEk3m1htISTcp6gQ6ik")

# --- 1. USER INPUTS (hardcoded for now) ---
destination = "Pasadena"
days = 3
pace = "moderate"
has_car = True
month = "November"


# --- 2. GEOCODE DESTINATION ---
def geocode_city(city_name):
    url = f"https://api.opentripmap.com/0.1/en/places/geoname"
    params = {"name": city_name, "apikey": "5ae2e3f221c38a28845f05b60f8887eacd3727cd6a9fd80fed39f192"}
    resp = requests.get(url, params=params).json()
    return resp["lat"], resp["lon"]


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
        "apikey": "5ae2e3f221c38a28845f05b60f8887eacd3727cd6a9fd80fed39f192",
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


# --- 5. CALL OPENAI ---
def generate_itinerary(prompt) ->str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(
        f"You are a travel itinerary planner.\n{prompt}"
    )
    return resp.text


itinerary = generate_itinerary(prompt)

print("=== Generated Itinerary ===")
print(itinerary)
