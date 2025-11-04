"""
Geographic location services for WanderTrip
Handles city geocoding using OpenTripMap API with fallback coordinates
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

# Fallback coordinates for major cities
CITY_COORDINATES = {
    "paris": (48.8566, 2.3522),
    "london": (51.5074, -0.1278),
    "rome": (41.9028, 12.4964),
    "tokyo": (35.6762, 139.6503),
    "new york": (40.7128, -74.0060),
    "new york city": (40.7128, -74.0060),
    "nyc": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "san francisco": (37.7749, -122.4194),
    "berlin": (52.5200, 13.4050),
    "madrid": (40.4168, -3.7038),
    "barcelona": (41.3851, 2.1734),
    "amsterdam": (52.3676, 4.9041),
    "vienna": (48.2082, 16.3738),
    "prague": (50.0755, 14.4378),
    "budapest": (47.4979, 19.0402),
    "moscow": (55.7558, 37.6176),
    "istanbul": (41.0082, 28.9784),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "hong kong": (22.3193, 114.1694),
    "sydney": (-33.8688, 151.2093),
    "melbourne": (-37.8136, 144.9631),
    "toronto": (43.6532, -79.3832),
    "vancouver": (49.2827, -123.1207),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.7041, 77.1025),
    "bangkok": (13.7563, 100.5018),
    "seoul": (37.5665, 126.9780),
    "beijing": (39.9042, 116.4074),
    "shanghai": (31.2304, 121.4737),
    "cairo": (30.0444, 31.2357),
    "cape town": (-33.9249, 18.4241),
    "rio de janeiro": (-22.9068, -43.1729),
    "buenos aires": (-34.6118, -58.3960),
    "mexico city": (19.4326, -99.1332),
    "lima": (-12.0464, -77.0428),
    "miami": (25.7617, -80.1918),
    "las vegas": (36.1699, -115.1398),
    "chicago": (41.8781, -87.6298),
    "boston": (42.3601, -71.0589),
    "seattle": (47.6062, -122.3321),
    "montreal": (45.5017, -73.5673),
    "lisbon": (38.7223, -9.1393),
    "athens": (37.9838, 23.7275),
    "florence": (43.7696, 11.2558),
    "venice": (45.4408, 12.3155),
    "milan": (45.4642, 9.1900),
    "zurich": (47.3769, 8.5417),
    "copenhagen": (55.6761, 12.5683),
    "stockholm": (59.3293, 18.0686),
    "oslo": (59.9139, 10.7522),
    "helsinki": (60.1699, 24.9384),
    "dublin": (53.3498, -6.2603)
}


def get_city_coordinates(city_name):
    """
    Get coordinates from fallback data
    
    Args:
        city_name (str): Name of the city
    
    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    city_key = city_name.lower().strip()
    
    # Try exact match first
    if city_key in CITY_COORDINATES:
        return CITY_COORDINATES[city_key]
    
    # Try partial matching
    for key in CITY_COORDINATES.keys():
        if key in city_key or city_key in key:
            return CITY_COORDINATES[key]
    
    return None


def geocode_city(city_name):
    """
    Get latitude and longitude coordinates for a city
    
    Args:
        city_name (str): Name of the city to geocode
    
    Returns:
        tuple: (latitude, longitude) as floats
    """
    print(f"🌍 [GEOCODING] Looking up coordinates for: {city_name}")
    
    # Try OpenTripMap API first
    if OPENTRIPMAP_API_KEY:
        url = f"https://api.opentripmap.com/0.1/en/places/geoname"
        params = {"name": city_name, "apikey": OPENTRIPMAP_API_KEY}
        
        try:
            print(f"🌍 [GEOCODING] Trying OpenTripMap API...")
            resp = requests.get(url, params=params)
            data = resp.json()
            
            if resp.status_code == 200 and "lat" in data and "lon" in data:
                print(f"🌍 [GEOCODING] ✅ API found coordinates: {data['lat']}, {data['lon']}")
                return data["lat"], data["lon"]
            else:
                print(f"🌍 [GEOCODING] ⚠️ API response: {data}")
                
        except Exception as e:
            print(f"🌍 [GEOCODING] ⚠️ API error: {e}")
    
    # Use fallback coordinates
    coords = get_city_coordinates(city_name)
    if coords:
        print(f"🌍 [GEOCODING] ✅ Using fallback coordinates: {coords[0]}, {coords[1]}")
        return coords
    
    # Final fallback: Use Paris coordinates
    print(f"🌍 [GEOCODING] ⚠️ City '{city_name}' not found, using Paris as default")
    return 48.8566, 2.3522