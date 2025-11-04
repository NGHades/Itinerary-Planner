"""
WanderTrip Flask Application
Main API server for travel itinerary planning
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from itinerary_service import generate_itinerary, build_prompt
from utils.geocoding import geocode_city
from utils.poi_service import get_pois


def create_app():
    """Application factory pattern for Flask app"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend requests
    
    @app.route('/')
    def index():
        return jsonify({
            "message": "WanderTrip API is running!",
            "version": "1.0.0",
            "endpoints": [
                "/api/itinerary",
                "/api/generate", 
                "/api/save"
            ]
        })

    @app.route('/api/itinerary', methods=['GET'])
    def get_itinerary():
        """Serve the current itinerary data"""
        try:
            # Use relative path from backend directory
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'itinerary_data.json')
            with open(data_path, 'r') as f:
                data = json.load(f)
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({"error": "No itinerary data found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/generate', methods=['POST'])
    def generate_new_itinerary():
        """Generate a new itinerary based on user inputs"""
        print("🚀 [API_GENERATE] Endpoint called!")
        try:
            data = request.json
            print(f"🚀 [API_GENERATE] Received data: {data}")
            
            destination = data.get('destination', 'Pasadena')
            days = data.get('days', 3)
            
            print(f"🚀 [API_GENERATE] Destination: {destination}, Days: {days}")
            
            # Extract guest information
            guests = data.get('guests', {})
            adults = guests.get('adults', 2)
            
            # Extract date information
            start_date = data.get('startDate')
            end_date = data.get('endDate')
            
            print(f"🚀 [API_GENERATE] Guests: {adults} adults, Dates: {start_date} to {end_date}")
            
            # Set reasonable defaults for missing form fields
            pace = 'moderate'  # Default pace since not collected from form
            has_car = True     # Default assumption since not collected from form
            
            # Determine month from start date if provided
            if start_date:
                from datetime import datetime
                try:
                    date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                    month = date_obj.strftime('%B')
                    print(f"🚀 [API_GENERATE] Derived month: {month}")
                except ValueError:
                    month = 'November'  # Fallback
                    print(f"🚀 [API_GENERATE] Date parse failed, using fallback month: {month}")
            else:
                month = 'November'  # Default fallback
                print(f"🚀 [API_GENERATE] No date provided, using default month: {month}")
            
            print(f"🚀 [API_GENERATE] Getting coordinates and POIs...")
            # Get POIs for the destination
            lat, lon = geocode_city(destination)
            pois = get_pois(lat, lon)
            
            print(f"🚀 [API_GENERATE] Coordinates: {lat}, {lon}")
            print(f"🚀 [API_GENERATE] POIs found: {len(pois) if pois else 0}")
            
            # Build prompt and generate itinerary (using month derived from actual dates)
            print(f"🚀 [API_GENERATE] Building prompt and generating itinerary...")
            prompt = build_prompt(destination, days, pace, has_car, pois, month)
            itinerary_json = generate_itinerary(prompt)
            
            print(f"🚀 [API_GENERATE] ✅ Itinerary generated!")
            print(f"🚀 [API_GENERATE] Generated destination: {itinerary_json.get('destination', 'Unknown')}")
            print(f"🚀 [API_GENERATE] Generated days: {len(itinerary_json.get('days', []))}")
            
            # Add the actual user input data to the response
            itinerary_json['userInputs'] = {
                'destination': destination,
                'days': days,
                'adults': adults,
                'startDate': start_date,
                'endDate': end_date
            }
            
            print(f"🚀 [API_GENERATE] 💾 Saving to itinerary_data.json...")
            # Save the new itinerary
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'itinerary_data.json')
            with open(data_path, 'w') as f:
                json.dump(itinerary_json, f, indent=2)
            
            print(f"🚀 [API_GENERATE] ✅ File saved successfully!")
            print(f"🚀 [API_GENERATE] 📤 Returning response to client...")
            
            return jsonify(itinerary_json)
            
        except Exception as e:
            print(f"❌ [API_GENERATE] Error occurred: {e}")
            print(f"❌ [API_GENERATE] Error type: {type(e).__name__}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/save', methods=['POST'])
    def save_itinerary():
        """Save modified itinerary data"""
        print("💾 [API_SAVE] Endpoint called!")
        try:
            data = request.json
            print(f"💾 [API_SAVE] Received data keys: {list(data.keys()) if data else 'None'}")
            print(f"💾 [API_SAVE] Data destination: {data.get('destination', 'Unknown') if data else 'None'}")
            
            print(f"💾 [API_SAVE] Writing to itinerary_data.json...")
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'itinerary_data.json')
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"💾 [API_SAVE] ✅ File saved successfully!")
            return jsonify({"success": True, "message": "Itinerary saved successfully"})
        except Exception as e:
            print(f"❌ [API_SAVE] Error occurred: {e}")
            return jsonify({"error": str(e)}), 500
    
    return app


def run_server():
    """Run the Flask development server"""
    app = create_app()
    app.run(debug=True, port=8080)


if __name__ == '__main__':
    run_server()