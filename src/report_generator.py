#report_generator
import pandas as pd
import matplotlib.pyplot as plt
import os

def save_to_csv(report_entry):
    """Appends weather data to a persistent CSV log."""
    os.makedirs('reports', exist_ok=True)
    file_path = "reports/weather_history.csv"
    
    # report_entry might contain a list for 'Alerts'. Convert it to a string for CSV.
    if 'Alerts' in report_entry and isinstance(report_entry['Alerts'], list):
        report_entry['Alert'] = " | ".join(report_entry['Alerts']) if report_entry['Alerts'] else "None"
        # We don't want the raw list in the CSV, so we delete it from the copy we save
        entry_to_save = report_entry.copy()
        del entry_to_save['Alerts']
    else:
        entry_to_save = report_entry

    df = pd.DataFrame([entry_to_save])
    df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))

def create_forecast_chart(hourly_data, city_name):
    """Creates a professional 48-hour temperature trend line chart."""
    os.makedirs('outputs', exist_ok=True)
    
    # Take the next 48 hours for a clean chart
    temps = hourly_data['temperature_2m'][:48]
    times = pd.to_datetime(hourly_data['time'][:48])
    
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5))
    plt.plot(times, temps, color='#00d4ff', linewidth=3, marker='o', markersize=4)
    
    plt.fill_between(times, temps, color='#00d4ff', alpha=0.1)
    plt.title(f"48-Hour Temperature Forecast: {city_name}", fontsize=14, pad=20)
    plt.ylabel("Temperature (\u00B0C)")
    
    # Format the x-axis to be more readable
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.2)
    
    save_path = f"outputs/{city_name}_forecast.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path