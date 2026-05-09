#logic_engine
from datetime import datetime

def check_alerts(data):
    current = data['current_weather']
    temp = current['temperature']
    cond_code = current['weathercode']
    
    # Get humidity from hourly
    humidity = data['hourly']['relative_humidity_2m'][0]
    
    # ALERT LOGIC: Check next 12 hours for rain
    rain_probs = data['hourly']['precipitation_probability'][:12]
    incoming_rain = any(prob > 50 for prob in rain_probs)
    
    alert_list = []
    if temp >= 35: 
        alert_list.append("🔥 HEAT ADVISORY: Temperatures exceeding 35°C.")
    if incoming_rain: 
        alert_list.append("🌧️ RAIN ALERT: High probability of precipitation in the next 12 hours.")
    if humidity > 85: 
        alert_list.append("💧 HUMIDITY WARNING: Uncomfortable humidity levels detected.")

    condition_text = "Clear" if cond_code <= 3 else "Cloudy/Precipitation"

    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "City": data['city_name'],
        "Full_Loc": data['address'].split(',')[-1].strip(),
        "Temp_C": temp,
        "Humidity": humidity,
        "Condition": condition_text,
        "Alerts": alert_list # Returning a list of alerts now
    }

def get_daily_forecast(data):
    """Extracts a simple 3-day forecast summary."""
    # We grab data at index 24 (Day 1), 48 (Day 2), 72 (Day 3) roughly
    # In a real app, you'd use the daily endpoint, but we'll extract it from hourly here
    # to keep the API call simple.
    forecast = []
    
    try:
        # Day 1 (Tomorrow)
        d1_temp = max(data['hourly']['temperature_2m'][24:48])
        d1_prob = max(data['hourly']['precipitation_probability'][24:48])
        forecast.append({"Day": "Tomorrow", "High": d1_temp, "Rain_Prob": f"{d1_prob}%"})
        
        # Day 2
        d2_temp = max(data['hourly']['temperature_2m'][48:72])
        d2_prob = max(data['hourly']['precipitation_probability'][48:72])
        forecast.append({"Day": "Day 2", "High": d2_temp, "Rain_Prob": f"{d2_prob}%"})
        
        # Day 3
        d3_temp = max(data['hourly']['temperature_2m'][72:96])
        d3_prob = max(data['hourly']['precipitation_probability'][72:96])
        forecast.append({"Day": "Day 3", "High": d3_temp, "Rain_Prob": f"{d3_prob}%"})
    except Exception:
         forecast = [{"Day": "N/A", "High": "N/A", "Rain_Prob": "N/A"}]
         
    return forecast