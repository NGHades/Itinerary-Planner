"""
Geographic location services for WanderTrip
Handles city geocoding using OpenTripMap API
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")


def geocode_city(city_name):
    """
    Get latitude and longitude coordinates for a city
    
    Args:
        city_name (str): Name of the city to geocode
    
    Returns:
        tuple: (latitude, longitude) as floats
    """
    url = f"https://api.opentripmap.com/0.1/en/places/geoname"
    params = {"name": city_name, "apikey": OPENTRIPMAP_API_KEY}
    
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        
        if resp.status_code == 200 and "lat" in data and "lon" in data:
            return data["lat"], data["lon"]
        else:
            # Fallback: Use hardcoded coordinates for Pasadena, CA
            print(f"Geocoding failed for {city_name}, using default coordinates for Pasadena, CA")
            return 34.1478, -118.1445
            
    except Exception as e:
        print(f"Geocoding error: {e}, using default coordinates")
        return 34.1478, -118.1445