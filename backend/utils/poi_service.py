"""
Points of Interest (POI) discovery service
Uses OpenTripMap API to find tourist attractions and landmarks
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")


def get_pois(lat, lon, radius=5000, limit=10):
    """
    Get points of interest within a radius of given coordinates
    
    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        radius (int): Search radius in meters (default: 5000)
        limit (int): Maximum number of POIs to return (default: 10)
    
    Returns:
        list: List of POI dictionaries with 'name' and 'type' keys
    """
    url = f"https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "radius": radius,
        "lon": lon,
        "lat": lat,
        "rate": 3,       # 1=low, 3=popular
        "limit": limit,
        "apikey": OPENTRIPMAP_API_KEY,
    }
    
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        
        pois = []
        for place in data.get("features", []):
            name = place["properties"]["name"]
            kinds = place["properties"].get("kinds", "")
            if name:  # Only include POIs with names
                pois.append({"name": name, "type": kinds})
        
        return pois
        
    except Exception as e:
        print(f"Error fetching POIs: {e}")
        return []


def get_poi_details(poi_id):
    """
    Get detailed information about a specific POI
    
    Args:
        poi_id (str): OpenTripMap POI identifier
    
    Returns:
        dict: Detailed POI information including description, image URLs, etc.
    """
    url = f"https://api.opentripmap.com/0.1/en/places/xid/{poi_id}"
    params = {"apikey": OPENTRIPMAP_API_KEY}
    
    try:
        resp = requests.get(url, params=params)
        return resp.json()
    except Exception as e:
        print(f"Error fetching POI details: {e}")
        return {}