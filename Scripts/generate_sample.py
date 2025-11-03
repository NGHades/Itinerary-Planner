#!/usr/bin/env python3
"""
Standalone script to generate sample itinerary data
Can be run independently to create test data for development
"""

import sys
import os
import json

# Add the project root to Python path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.itinerary_service import create_itinerary


def main():
    """Generate sample itinerary data"""
    # Default configuration
    destination = "Pasadena"
    days = 3
    pace = "moderate" 
    has_car = True
    month = "November"
    
    print(f"Generating {days}-day itinerary for {destination}...")
    
    try:
        # Generate itinerary
        itinerary_data = create_itinerary(
            destination=destination,
            days=days,
            pace=pace,
            has_car=has_car,
            month=month
        )
        
        # Pretty print the result
        print("\n=== Generated Itinerary (JSON) ===")
        print(json.dumps(itinerary_data, indent=2))
        
        # Save to frontend directory
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'frontend',
            'itinerary_data.json'
        )
        
        with open(output_path, 'w') as f:
            json.dump(itinerary_data, f, indent=2)
        
        print(f"\nItinerary saved to {output_path}")
        
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())