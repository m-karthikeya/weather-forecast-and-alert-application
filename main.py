#main
import streamlit as st
import pandas as pd
from src.api_handler import get_weather_data
from src.logic_engine import check_alerts, get_daily_forecast
from src.report_generator import save_to_csv, create_forecast_chart

st.set_page_config(page_title="Weather Forecast & Alert App", page_icon="🌤️", layout="wide")

st.title("🌤️ Weather Forecast & Alert Application")
st.markdown("A real-time meteorological monitoring tool with predictive warnings.")
st.markdown("---")

# Sidebar for Input
with st.sidebar:
    st.header("📍 Location Settings")
    city = st.text_input("Enter City Name", "Anantapur")
    run_btn = st.button("Analyze Weather Data", type="primary")
    st.markdown("---")
    st.caption("Data provided by Open-Meteo API")

if run_btn:
    with st.spinner(f'Fetching live satellite data for {city}...'):
        data = get_weather_data(city)
        
        if data:
            report = check_alerts(data)
            forecast = get_daily_forecast(data)
            
            st.subheader(f"Current Conditions in {report['City']}, {report['Full_Loc']}")
            
            # --- THE ALERT SECTION ---
            st.markdown("### 🚨 Active Alerts")
            if report['Alerts']:
                for alert in report['Alerts']:
                    if "HEAT" in alert:
                        st.error(alert)
                    elif "RAIN" in alert:
                        st.warning(alert)
                    else:
                        st.info(alert)
            else:
                st.success("✅ No Active Alerts. Conditions are safe.")
            
            st.markdown("---")
            
            # --- THE CURRENT WEATHER SECTION ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{report['Temp_C']} \u00B0C")
            col2.metric("Humidity", f"{report['Humidity']}%")
            col3.metric("Condition", report['Condition'])
            
            st.markdown("---")
            
            # --- THE FORECAST SECTION ---
            st.subheader("📅 3-Day Forecast Summary")
            
            # Create a simple "Grid" for the forecast
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.info(f"**{forecast[0]['Day']}**\n\nHigh: {forecast[0]['High']}\u00B0C\n\nRain Prob: {forecast[0]['Rain_Prob']}")
            with f_col2:
                st.info(f"**{forecast[1]['Day']}**\n\nHigh: {forecast[1]['High']}\u00B0C\n\nRain Prob: {forecast[1]['Rain_Prob']}")
            with f_col3:
                st.info(f"**{forecast[2]['Day']}**\n\nHigh: {forecast[2]['High']}\u00B0C\n\nRain Prob: {forecast[2]['Rain_Prob']}")

            st.markdown("---")

            # --- THE VISUALIZATION SECTION ---
            st.subheader("📈 48-Hour Temperature Trend")
            chart_path = create_forecast_chart(data['hourly'], city)
            
            st.image(chart_path, use_container_width=True)

            # --- DATA LOGGING ---
            save_to_csv(report)
            
        else:
            st.error(f"Failed to retrieve data for '{city}'. Please check the spelling.")

st.markdown("---")