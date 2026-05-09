#api_handler
import requests
from geopy.geocoders import Nominatim

def get_weather_data(city):
    """
    Fetches real-time data from Open-Meteo (No API Key required).
    1. Converts City to Lat/Long.
    2. Fetches current and hourly forecast.
    """
    try:
        # Step 1: Get Coordinates
        geolocator = Nominatim(user_agent="weather_forecast_dashboard")
        location = geolocator.geocode(city)
        
        if not location:
            print(f"[Error] Could not find coordinates for {city}")
            return None

        lat, lon = location.latitude, location.longitude

        # Step 2: Fetch Weather Data
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability",
            "timezone": "auto"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Adding city/country info back into the dictionary for logic_engine
            data['city_name'] = city.capitalize()
            data['address'] = location.address
            return data
        else:
            return None

    except Exception as e:
        print(f"[System Error] {e}")
        return None