from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from itinerary import generate_itinerary, build_prompt, get_pois, geocode_city

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/')
def index():
    return "Travel Itinerary API is running!"

@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    """Serve the current itinerary data"""
    try:
        with open('frontend/itinerary_data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "No itinerary data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_new_itinerary():
    """Generate a new itinerary based on user inputs"""
    try:
        data = request.json
        destination = data.get('destination', 'Pasadena')
        days = data.get('days', 3)
        pace = data.get('pace', 'moderate')
        has_car = data.get('has_car', True)
        month = data.get('month', 'November')
        
        # Get POIs for the destination
        lat, lon = geocode_city(destination)
        pois = get_pois(lat, lon)
        
        # Build prompt and generate itinerary
        prompt = build_prompt(destination, days, pace, has_car, pois)
        itinerary_json = generate_itinerary(prompt)
        
        # Save the new itinerary
        with open('frontend/itinerary_data.json', 'w') as f:
            json.dump(itinerary_json, f, indent=2)
        
        return jsonify(itinerary_json)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_itinerary():
    """Save modified itinerary data"""
    try:
        data = request.json
        with open('frontend/itinerary_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({"success": True, "message": "Itinerary saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)