import json
import requests
from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__, template_folder='templates')

# File paths
LOCATIONS_FILE = 'locations.json'
CREDENTIALS_FILE = 'credentials.json'

# Initialize locations file if it doesn't exist
if not os.path.exists(LOCATIONS_FILE):
    with open(LOCATIONS_FILE, 'w') as f:
        json.dump([
            {"name": "MAU micro Finance Bank", "lat": 9.345492416940417, "lon": 12.50601813594931},
            {"name": "Admin Block", "lat": 9.344825471025517, "lon":  12.503250096228145},
            {"name": "SLS LT1 & 2", "lat": 9.351696011512175,  "lon": 12.48553678787726},
            {"name": "LT5 and 6", "lat": 9.348583641688878, "lon": 12.498153899074662},
            {"name": "Smith LT1", "lat": 9.347609697146915, "lon": 12.49801442422044},
            {"name": "CBT Center", "lat":9.348520123666368, "lon": 12.496211979759792},
            {"name": "Smith", "lat": 9.347165069381244, "lon":  12.497445795928263},
            {"name": "STSE", "lat": 9.352860496458316,   "lon": 12.489538643741357},
            {"name": "College of Medical Sciences", "lat": 9.351378424042613,  "lon": 12.494012568382297},
            {"name": "ICT Center", "lat": 9.346498126654113, "lon":   12.501125786668604  },
             {"name": "Multi Purpose Hall", "lat": 9.34828722412421, "lon":  12.500342581651598},
            {"name": "Ibrahim Babangida Library", "lat": 9.350023380856136, "lon":  12.492564175504123},
            {"name": "Department of Food Science", "lat": 9.347990806206194,    "lon": 12.494216416251593},
            {"name": "School of Agriculture", "lat": 9.347556765297265,   "lon":  12.495632622622693},
            { "name": "Library", "lat": 9.3339, "lon": 12.4968 },
            { "name": "School Clinic", "lat": 9.3352, "lon": 12.4959 },
            { "name": "Guidance & Counselling", "lat": 9.3341, "lon": 12.4961 },
            { "name": "Security Office", "lat": 9.3335, "lon": 12.4967 }
            
        ], f)

# Initialize credentials file if it doesn't exist
if not os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({"username": "admin", "password": "admin123"}, f)

# Load locations
def load_locations():
    try:
        with open(LOCATIONS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading locations: {e}")
        return []

# Save locations
def save_locations(locations):
    try:
        with open(LOCATIONS_FILE, 'w') as f:
            json.dump(locations, f)
    except Exception as e:
        print(f"Error saving locations: {e}")

# Load credentials
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return {"username": "admin", "password": "admin123"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/locations')
def get_locations():
    try:
        return jsonify(load_locations())
    except Exception as e:
        print(f"Error loading locations: {e}")
        return jsonify({'error': 'Failed to load locations'}), 500

@app.route('/directions')
def get_directions():
    try:
        start = request.args.get('start').split(',')
        end = request.args.get('end').split(',')
        start = [float(start[0]), float(start[1])]
        end = [float(end[0]), float(end[1])]

        # Relaxed validation for MAU Yola area (expanded bounds)
        if not (9.29 <= start[0] <= 9.36 and 12.44 <= start[1] <= 12.56):
            print(f"Invalid start coordinates for MAU Yola area: {start}")
            return jsonify({'error': 'Start coordinates outside campus area'}), 400
        if not (9.29 <= end[0] <= 9.36 and 12.44 <= end[1] <= 12.56):
            print(f"Invalid end coordinates for MAU Yola area: {end}")
            return jsonify({'error': 'Destination coordinates outside campus area'}), 400

        # Use OpenRouteService for routing
        api_key = "5b3ce3597851110001cf624871868e31e7194277a6b2d22ad48346d2"
        url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        body = {
            "coordinates": [[start[1], start[0]], [end[1], end[0]]],  # ORS expects [lon, lat]
            "instructions": True
        }
        print(f"Requesting ORS route: {url} with body: {body}")
        response = requests.post(url, json=body, headers=headers, timeout=10)
        data = response.json()
        print(f"ORS response: {data}")

        if response.status_code == 200 and 'features' in data:
            route = data['features'][0]['geometry']['coordinates']
            route = [[coord[1], coord[0]] for coord in route]  # Swap lon, lat to lat, lon for Leaflet
            distance = data['features'][0]['properties']['summary']['distance'] / 1000  # Convert to km
            steps = [instr.get('instruction', 'No instruction') for instr in data['features'][0]['properties']['segments'][0]['steps']]
            return jsonify({'route': route, 'steps': steps, 'distance': distance})
        else:
            print(f"ORS error: {data.get('error', 'No error message provided')}")
            return jsonify({'error': data.get('error', 'Unable to calculate route')}), 400
    except ValueError as e:
        print(f"ValueError in directions: {e}")
        return jsonify({'error': 'Invalid coordinate format'}), 400
    except requests.RequestException as e:
        print(f"Request error in directions: {e}")
        return jsonify({'error': 'Failed to connect to routing service'}), 503
    except Exception as e:
        print(f"Unexpected error in directions: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        credentials = load_credentials()
        if data['username'] == credentials['username'] and data['password'] == credentials['password']:
            return jsonify({'success': True})
        return jsonify({'success': False})
    except Exception as e:
        print(f"Error in admin login: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/add-location', methods=['POST'])
def add_location():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'lat', 'lon']):
            print("Missing required fields in add-location")
            return jsonify({'error': 'Missing required fields'}), 400
        lat = float(data['lat'])
        lon = float(data['lon'])
        # Validate coordinates for MAU Yola area
               # Validate coordinates for MAU Yola area
        if not (9.28 <= lat <= 9.37 and 12.44 <= lon <= 12.57):
            print(f"Invalid coordinates in add-location: lat={lat}, lon={lon}")
            return jsonify({'error': 'Coordinates outside campus area'}), 400

        locations = load_locations()
        for loc in locations:
            if loc['name'] == data['name']:
                loc['lat'] = lat
                loc['lon'] = lon
                save_locations(locations)
                return jsonify({'message': 'Location updated'})
        locations.append({'name': data['name'], 'lat': lat, 'lon': lon})
        save_locations(locations)
        return jsonify({'message': 'Location added'})
    except Exception as e:
        print(f"Error in add-location: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)