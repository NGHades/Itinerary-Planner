"""
Points of Interest (POI) discovery service
Uses OpenTripMap API to find tourist attractions and landmarks
Includes fallback static data for common destinations
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

# Fallback POI data for common destinations
FALLBACK_POIS = {
    "paris": [
        {"name": "Eiffel Tower", "type": "monuments"},
        {"name": "Louvre Museum", "type": "museums"},
        {"name": "Notre-Dame Cathedral", "type": "churches"},
        {"name": "Arc de Triomphe", "type": "monuments"},
        {"name": "Champs-Élysées", "type": "interesting_places"},
        {"name": "Sacré-Cœur", "type": "churches"},
        {"name": "Seine River Cruise", "type": "water"},
        {"name": "Montmartre District", "type": "interesting_places"},
        {"name": "Versailles Palace", "type": "museums"},
        {"name": "Latin Quarter", "type": "interesting_places"}
    ],
    "london": [
        {"name": "Big Ben", "type": "monuments"},
        {"name": "Tower of London", "type": "museums"},
        {"name": "British Museum", "type": "museums"},
        {"name": "London Eye", "type": "attractions"},
        {"name": "Westminster Abbey", "type": "churches"},
        {"name": "Buckingham Palace", "type": "monuments"},
        {"name": "Tower Bridge", "type": "bridges"},
        {"name": "Hyde Park", "type": "parks"},
        {"name": "Covent Garden", "type": "interesting_places"},
        {"name": "Tate Modern", "type": "museums"}
    ],
    "rome": [
        {"name": "Colosseum", "type": "monuments"},
        {"name": "Vatican Museums", "type": "museums"},
        {"name": "Trevi Fountain", "type": "monuments"},
        {"name": "Roman Forum", "type": "archaeological_sites"},
        {"name": "Pantheon", "type": "churches"},
        {"name": "Spanish Steps", "type": "monuments"},
        {"name": "St. Peter's Basilica", "type": "churches"},
        {"name": "Castel Sant'Angelo", "type": "museums"},
        {"name": "Villa Borghese", "type": "parks"},
        {"name": "Trastevere", "type": "interesting_places"}
    ],
    "tokyo": [
        {"name": "Senso-ji Temple", "type": "temples"},
        {"name": "Tokyo Skytree", "type": "towers"},
        {"name": "Shibuya Crossing", "type": "interesting_places"},
        {"name": "Meiji Shrine", "type": "temples"},
        {"name": "Imperial Palace", "type": "monuments"},
        {"name": "Tsukiji Outer Market", "type": "food_markets"},
        {"name": "Ueno Park", "type": "parks"},
        {"name": "Ginza District", "type": "interesting_places"},
        {"name": "Tokyo National Museum", "type": "museums"},
        {"name": "Harajuku", "type": "interesting_places"}
    ],
    "new york": [
        {"name": "Statue of Liberty", "type": "monuments"},
        {"name": "Central Park", "type": "parks"},
        {"name": "Empire State Building", "type": "skyscrapers"},
        {"name": "Times Square", "type": "interesting_places"},
        {"name": "Brooklyn Bridge", "type": "bridges"},
        {"name": "Metropolitan Museum", "type": "museums"},
        {"name": "9/11 Memorial", "type": "monuments"},
        {"name": "High Line Park", "type": "parks"},
        {"name": "Broadway Theater District", "type": "theatres"},
        {"name": "Wall Street", "type": "interesting_places"}
    ]
}


def get_fallback_pois(destination):
    """
    Get fallback POI data for common destinations
    
    Args:
        destination (str): Destination city name
    
    Returns:
        list: List of POI dictionaries
    """
    dest_key = destination.lower().strip()
    
    # Try exact match first
    if dest_key in FALLBACK_POIS:
        return FALLBACK_POIS[dest_key]
    
    # Try partial matching for cities with country names
    for key in FALLBACK_POIS.keys():
        if key in dest_key or dest_key in key:
            return FALLBACK_POIS[key]
    
    # Return generic POIs for unknown destinations
    return [
        {"name": "City Center", "type": "interesting_places"},
        {"name": "Local Museum", "type": "museums"},
        {"name": "Main Square", "type": "interesting_places"},
        {"name": "Historic District", "type": "interesting_places"},
        {"name": "Local Market", "type": "food_markets"},
        {"name": "Waterfront Area", "type": "interesting_places"},
        {"name": "Cultural Center", "type": "museums"},
        {"name": "Public Park", "type": "parks"}
    ]


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
    print(f"🔍 [POI_SERVICE] Searching for POIs at coordinates: {lat}, {lon}")
    
    # Try OpenTripMap API first
    if OPENTRIPMAP_API_KEY:
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
            print(f"🔍 [POI_SERVICE] Making API request to OpenTripMap...")
            resp = requests.get(url, params=params)
            data = resp.json()
            
            print(f"🔍 [POI_SERVICE] API Response status: {resp.status_code}")
            
            if resp.status_code == 200 and data and "features" in data:
                pois = []
                for place in data.get("features", []):
                    name = place["properties"]["name"]
                    kinds = place["properties"].get("kinds", "")
                    if name:  # Only include POIs with names
                        pois.append({"name": name, "type": kinds})
                
                if pois:
                    print(f"🔍 [POI_SERVICE] ✅ Found {len(pois)} POIs from API")
                    return pois[:limit]
                else:
                    print(f"🔍 [POI_SERVICE] ⚠️ API returned no POIs, using fallback data")
            else:
                print(f"🔍 [POI_SERVICE] ⚠️ API returned empty response, using fallback data")
            
        except Exception as e:
            print(f"🔍 [POI_SERVICE] ⚠️ API error: {e}, using fallback data")
    else:
        print(f"🔍 [POI_SERVICE] ⚠️ No API key, using fallback data")
    
    # Use fallback data based on coordinates
    fallback_pois = get_fallback_pois_by_coordinates(lat, lon)
    print(f"🔍 [POI_SERVICE] ✅ Using {len(fallback_pois)} fallback POIs")
    return fallback_pois[:limit]


def get_fallback_pois_by_coordinates(lat, lon):
    """
    Get fallback POIs based on approximate coordinates
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
    
    Returns:
        list: List of POI dictionaries
    """
    # Approximate coordinate ranges for major cities
    city_coords = {
        "paris": (48.8566, 2.3522),
        "london": (51.5074, -0.1278),
        "rome": (41.9028, 12.4964),
        "tokyo": (35.6762, 139.6503),
        "new york": (40.7128, -74.0060)
    }
    
    # Find closest city based on coordinates (simple distance)
    min_distance = float('inf')
    closest_city = None
    
    for city, (city_lat, city_lon) in city_coords.items():
        distance = abs(lat - city_lat) + abs(lon - city_lon)  # Manhattan distance
        if distance < min_distance:
            min_distance = distance
            closest_city = city
    
    # If coordinates are close to a known city (within ~1 degree), use that city's POIs
    if min_distance < 1.0 and closest_city:
        return FALLBACK_POIS[closest_city]
    
    # Otherwise return generic POIs
    return get_fallback_pois("unknown")


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