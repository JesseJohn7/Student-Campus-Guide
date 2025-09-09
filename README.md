# MAU Yola Campus Guide

A web-based interactive map and navigation system for Modibbo Adama University (MAU), Yola. This project helps students, staff, and visitors find locations, get walking directions, and learn about campus facilities.

## Features

- **Interactive Map**: Visualize campus locations using OpenStreetMap and Leaflet.js.
- **Search**: Quickly find any building or facility by name.
- **Directions**: Get step-by-step walking directions between any two points on campus.
- **Location Markers**: See all major buildings, offices, and services on the map.
- **Admin Panel**: Add or update campus locations (secured by login).
- **Mobile Friendly**: Responsive design for use on phones and tablets.

## Demo Screenshots

![Campus Guide Main](Campus%20Guide.png)
![Route Example](route.png)
![Search Result Display](Search%20Resultt%20Display.png)

## Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/MAU-Campus-Guide.git
   cd MAU-Campus-Guide
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the app**
   ```sh
   python app.py
   ```
4. **Open in browser**
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure

- `app.py` — Main Flask backend
- `templates/index.html` — Main web UI
- `locations.json` — List of campus locations
- `credentials.json` — Admin login credentials
- `requirements.txt` — Python dependencies
- `route.png`, `Campus Guide.png`, `Search Resultt Display.png` — Demo images

## API Endpoints

- `/` — Main web interface
- `/locations` — Get all campus locations (JSON)
- `/directions?start=lat,lon&end=lat,lon` — Get walking directions (JSON)
- `/admin-login` — Admin login (POST)
- `/add-location` — Add or update a location (POST)

## Technologies Used
- Python, Flask
- HTML, CSS, JavaScript
- Leaflet.js, OpenStreetMap
- OpenRouteService API (for directions)

## Customization
- To add new locations, use the admin panel or edit `locations.json`.
- To change admin credentials, edit `credentials.json`.

## License
MIT License

---

**This project is student-built for MAU Yola. Contributions and suggestions are welcome!**
