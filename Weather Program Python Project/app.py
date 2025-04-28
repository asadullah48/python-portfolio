#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
🌦️ Weather Magic - Advanced Weather Forecast App
Featuring Lottie animations, dynamic backgrounds, premium UI/UX, 5-day forecast,
air quality data, and unit conversion.
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import pytz
import os
from typing import Optional, Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    st.error("OpenWeather API key not found. Please set it in the .env file.")
    API_KEY = "da1537f4faec6d6b4b6d1c09b1701e37"  # Fallback API key (limited usage)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
AIR_QUALITY_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
TIMEZONE = "UTC"
REFRESH_INTERVAL = 300  # 5 minutes in seconds

# Constants for the app

# Air Quality Index descriptions
AQI_DESCRIPTIONS = {
    1: {"level": "Good", "description": "Air quality is satisfactory, and air pollution poses little or no risk.", "color": "#4CAF50"},
    2: {"level": "Fair", "description": "Air quality is acceptable. However, there may be a risk for some people.", "color": "#8BC34A"},
    3: {"level": "Moderate", "description": "Members of sensitive groups may experience health effects.", "color": "#FFC107"},
    4: {"level": "Poor", "description": "Everyone may begin to experience health effects.", "color": "#FF9800"},
    5: {"level": "Very Poor", "description": "Health warnings of emergency conditions. The entire population is likely to be affected.", "color": "#F44336"}
}

# Temperature unit conversion
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

# CSS for animated background and UI enhancements
def load_css():
    st.markdown(f"""
    <style>
    /* Animated gradient background */
    @keyframes gradientBackground {{
        0% {{background-position: 0% 50%;}}
        50% {{background-position: 100% 50%;}}
        100% {{background-position: 0% 50%;}}
    }}

    /* Dark mode and light mode variables */
    :root {{
        --bg-gradient-dark: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a40);
        --bg-gradient-light: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        --card-bg-dark: rgba(0, 0, 0, 0.5);
        --card-bg-light: rgba(255, 255, 255, 0.25);
        --text-color-dark: #f0f0f0;
        --text-color-light: #1a1a2e;
        --border-color-dark: rgba(255, 255, 255, 0.18);
        --border-color-light: rgba(0, 0, 0, 0.1);
        --shadow-color-dark: rgba(0, 0, 0, 0.5);
        --shadow-color-light: rgba(31, 38, 135, 0.2);
        --link-color-dark: #9ff0ff;
        --link-color-light: #0066cc;
    }}

    body {{
        background: var(--bg-gradient-dark);
        background-size: 400% 400%;
        animation: gradientBackground 15s ease infinite;
        transition: all 0.5s ease;
    }}

    body.light-mode {{
        background: var(--bg-gradient-light);
    }}

    /* Glass morphism effect with improved text contrast */
    .glass-card {{
        background: var(--card-bg-dark);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid var(--border-color-dark);
        padding: 22px;
        margin-bottom: 22px;
        box-shadow: 0 8px 32px 0 var(--shadow-color-dark);
        transition: all 0.3s ease;
        color: var(--text-color-dark);
    }}

    .light-mode .glass-card {{
        background: var(--card-bg-light);
        border: 1px solid var(--border-color-light);
        color: var(--text-color-light);
        box-shadow: 0 8px 32px 0 var(--shadow-color-light);
    }}

    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }}

    /* Adding text shadow to all text for better readability */
    h1, h2, h3, p, .stMarkdown, .stExpander, .stCaption {{
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        color: var(--text-color-dark);
        transition: color 0.3s ease;
    }}

    .light-mode h1, .light-mode h2, .light-mode h3, .light-mode p,
    .light-mode .stMarkdown, .light-mode .stExpander, .light-mode .stCaption {{
        text-shadow: none;
        color: var(--text-color-light);
    }}

    /* Weather animation container */
    .animation-container {{
        height: 220px;
        margin: 20px 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    /* Input field styling */
    .stTextInput>div>div>input {{
        background: rgba(0, 0, 0, 0.3) !important;
        color: var(--text-color-dark) !important;
        border-radius: 24px !important;
        border: 1px solid var(--border-color-dark) !important;
        padding: 12px 18px !important;
        transition: all 0.3s ease !important;
    }}

    .light-mode .stTextInput>div>div>input {{
        background: rgba(255, 255, 255, 0.7) !important;
        color: var(--text-color-light) !important;
        border: 1px solid var(--border-color-light) !important;
    }}

    .stTextInput>div>div>input::placeholder {{
        color: rgba(255,255,255,0.7) !important;
    }}

    .light-mode .stTextInput>div>div>input::placeholder {{
        color: rgba(0,0,0,0.5) !important;
    }}

    .stTextInput>div>div>input:focus {{
        box-shadow: 0 0 0 2px rgba(128, 128, 255, 0.5) !important;
        border-color: rgba(128, 128, 255, 0.8) !important;
    }}

    /* Button styling */
    .stButton>button {{
        background: rgba(0, 0, 0, 0.3) !important;
        color: var(--text-color-dark) !important;
        border-radius: 24px !important;
        border: 1px solid var(--border-color-dark) !important;
        transition: all 0.3s ease !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
    }}

    .light-mode .stButton>button {{
        background: rgba(255, 255, 255, 0.7) !important;
        color: var(--text-color-light) !important;
        border: 1px solid var(--border-color-light) !important;
    }}

    .stButton>button:hover {{
        background: rgba(0, 0, 0, 0.5) !important;
        transform: scale(1.05);
    }}

    .light-mode .stButton>button:hover {{
        background: rgba(255, 255, 255, 0.9) !important;
    }}

    /* Toggle switch for dark/light mode */
    .toggle-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px 0;
    }}

    .toggle-switch {{
        position: relative;
        display: inline-block;
        width: 60px;
        height: 30px;
    }}

    .toggle-switch input {{
        opacity: 0;
        width: 0;
        height: 0;
    }}

    .toggle-slider {{
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        transition: .4s;
        border-radius: 34px;
    }}

    .toggle-slider:before {{
        position: absolute;
        content: "";
        height: 22px;
        width: 22px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
        border-radius: 50%;
    }}

    input:checked + .toggle-slider {{
        background-color: rgba(255, 255, 255, 0.8);
    }}

    input:checked + .toggle-slider:before {{
        transform: translateX(30px);
        background-color: #1a1a2e;
    }}

    /* Links with better contrast */
    a {{
        color: var(--link-color-dark) !important;
        text-decoration: none !important;
        transition: all 0.3s ease;
    }}

    .light-mode a {{
        color: var(--link-color-light) !important;
    }}

    a:hover {{
        text-decoration: underline !important;
        opacity: 0.9;
    }}

    /* Forecast cards */
    .forecast-container {{
        display: flex;
        overflow-x: auto;
        padding: 10px 0;
        margin: 20px 0;
        scroll-snap-type: x mandatory;
    }}

    .forecast-card {{
        min-width: 150px;
        scroll-snap-align: start;
        margin-right: 15px;
        text-align: center;
    }}

    /* Air quality indicator */
    .aqi-indicator {{
        width: 100%;
        height: 10px;
        border-radius: 5px;
        margin: 10px 0;
        background: linear-gradient(to right, #4CAF50, #8BC34A, #FFC107, #FF9800, #F44336);
    }}

    .aqi-marker {{
        width: 15px;
        height: 15px;
        background-color: white;
        border-radius: 50%;
        position: relative;
        top: -12px;
        border: 2px solid #333;
        transition: left 0.5s ease;
    }}

    /* Mobile responsiveness */
    @media only screen and (max-width: 768px) {{
        .glass-card {{
            padding: 18px;
            margin-bottom: 18px;
        }}

        .stTextInput>div>div>input {{
            padding: 10px 15px !important;
        }}

        .stButton>button {{
            padding: 10px 20px !important;
            font-size: 14px !important;
        }}

        .animation-container {{
            height: 180px;
        }}

        .forecast-card {{
            min-width: 120px;
        }}
    }}

    @media only screen and (max-width: 480px) {{
        .glass-card {{
            padding: 15px;
            margin-bottom: 15px;
        }}

        .animation-container {{
            height: 150px;
        }}

        .forecast-card {{
            min-width: 100px;
            margin-right: 10px;
        }}
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.2);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255,255,255,0.3);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255,255,255,0.5);
    }}

    .light-mode ::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.1);
    }}
    .light-mode ::-webkit-scrollbar-thumb {{
        background: rgba(0,0,0,0.2);
    }}
    .light-mode ::-webkit-scrollbar-thumb:hover {{
        background: rgba(0,0,0,0.3);
    }}

    /* Loading animation */
    .loading-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }}
    </style>
    """, unsafe_allow_html=True)
def configure_page():
    """Set up Streamlit page configuration"""
    st.set_page_config(
        page_title="Weather Magic",
        page_icon="🌤️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    load_css()

    # Initialize session state for theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'

    # Add theme toggle in header
    col1, col2 = st.columns([4, 1])
    with col2:
        st.markdown("""
            <div class="toggle-container">
                <span style="margin-right: 10px;">🌙</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="theme-toggle" onchange="toggleTheme()">
                    <span class="toggle-slider"></span>
                </label>
                <span style="margin-left: 10px;">☀️</span>
            </div>
            <script>
                function toggleTheme() {
                    const body = document.querySelector('body');
                    body.classList.toggle('light-mode');

                    // Store theme preference
                    const isLightMode = body.classList.contains('light-mode');
                    localStorage.setItem('theme', isLightMode ? 'light' : 'dark');

                    // Send theme to Streamlit
                    const data = {
                        theme: isLightMode ? 'light' : 'dark'
                    };
                    window.parent.postMessage({
                        type: "streamlit:setComponentValue",
                        value: data
                    }, "*");
                }

                // Apply saved theme on load
                document.addEventListener('DOMContentLoaded', () => {
                    const savedTheme = localStorage.getItem('theme');
                    if (savedTheme === 'light') {
                        document.querySelector('body').classList.add('light-mode');
                        document.getElementById('theme-toggle').checked = true;
                    }
                });
            </script>
        """, unsafe_allow_html=True)

    # App header
    with col1:
        st.markdown("""
            <h1 style="text-align: center;
                    font-weight: 700;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                    margin-bottom: 0;">
                Weather Magic 🌈
            </h1>
            <p style="text-align: center; opacity: 0.8;">
                Real-time weather with beautiful animations
            </p>
        """, unsafe_allow_html=True)

def get_weather_data(city: str, units: str = "metric") -> Optional[Dict[str, Any]]:
    """Fetch current weather data from OpenWeatherMap API"""
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Network error occurred: {str(e)}")
        return None
    except ValueError as e:
        st.error(f"Error parsing weather data: {str(e)}")
        return None

def get_forecast_data(city: str, units: str = "metric") -> Optional[Dict[str, Any]]:
    """Fetch 5-day forecast data from OpenWeatherMap API"""
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units,
            "cnt": 40  # 5 days, 3-hour intervals
        }
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Network error occurred: {str(e)}")
        return None
    except ValueError as e:
        st.error(f"Error parsing forecast data: {str(e)}")
        return None

def get_air_quality_data(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch air quality data from OpenWeatherMap API"""
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }
        response = requests.get(AIR_QUALITY_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Network error occurred: {str(e)}")
        return None
    except ValueError as e:
        st.error(f"Error parsing air quality data: {str(e)}")
        return None

def get_city_coordinates(city: str) -> Optional[Tuple[float, float]]:
    """Get latitude and longitude for a city using OpenWeatherMap Geocoding API"""
    try:
        params = {
            "q": city,
            "limit": 1,
            "appid": API_KEY
        }
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return data[0]["lat"], data[0]["lon"]
        return None
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        st.error(f"Error getting city coordinates: {str(e)}")
        return None

def get_weather_emoji(weather_condition: str) -> str:
    """Return appropriate emoji based on weather condition"""
    weather_condition = weather_condition.lower()

    if "rain" in weather_condition:
        return "🌧️"
    elif "cloud" in weather_condition:
        return "☁️"
    elif "sun" in weather_condition or "clear" in weather_condition:
        return "☀️"
    elif "snow" in weather_condition:
        return "❄️"
    elif "thunder" in weather_condition or "storm" in weather_condition:
        return "⚡"
    elif "wind" in weather_condition:
        return "💨"
    elif "mist" in weather_condition or "fog" in weather_condition or "haze" in weather_condition:
        return "🌫️"
    else:
        return "🌤️"

def get_weather_color(weather_condition: str) -> str:
    """Return appropriate background color based on weather condition"""
    weather_condition = weather_condition.lower()

    if "rain" in weather_condition:
        return "#4287f5"  # Blue
    elif "cloud" in weather_condition:
        return "#b3b3b3"  # Gray
    elif "sun" in weather_condition or "clear" in weather_condition:
        return "#ffd700"  # Gold
    elif "snow" in weather_condition:
        return "#e6f2ff"  # Light blue
    elif "thunder" in weather_condition or "storm" in weather_condition:
        return "#666699"  # Dark purple
    elif "wind" in weather_condition:
        return "#b3d9ff"  # Light blue
    elif "mist" in weather_condition or "fog" in weather_condition or "haze" in weather_condition:
        return "#cccccc"  # Light gray
    else:
        return "#87ceeb"  # Sky blue

def is_daytime(sunrise: int, sunset: int, current: int) -> bool:
    """Check if it's daytime based on sunrise and sunset times"""
    return sunrise <= current <= sunset

def display_weather_info(weather_data: Dict[str, Any], units: str = "metric", forecast_data: Optional[Dict[str, Any]] = None, air_quality_data: Optional[Dict[str, Any]] = None):
    """Display weather information with animations and additional features"""
    if not weather_data or weather_data.get("cod") != 200:
        st.error("Invalid weather data received")
        return

    try:
        # Extract weather information
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        description = weather_data["weather"][0]["description"]
        city_name = weather_data.get("name", "Unknown City")
        country = weather_data.get("sys", {}).get("country", "")

        # Get sunrise/sunset times
        sunrise = weather_data.get("sys", {}).get("sunrise", 0)
        sunset = weather_data.get("sys", {}).get("sunset", 0)

        # Temperature unit display
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"

        # Display city name and animation
        st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="margin: 0;">{city_name}, {country if country else ''}</h2>
                <p style="margin: 5px 0 15px 0; text-transform: capitalize; font-size: 1.2rem;">
                    {description}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Display weather icon (using HTML instead of Lottie animation)
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin: 20px 0;">
                <div style="width: 150px; height: 150px; background-color: {get_weather_color(description)};
                     border-radius: 50%; display: flex; justify-content: center; align-items: center;">
                    <span style="font-size: 50px;">{get_weather_emoji(description)}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Create columns for metrics
        col1, col2, col3 = st.columns(3)

        # Temperature card
        with col1:
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Temperature</p>
                    <h2 style="margin: 0;">{temp:.1f}{temp_unit}</h2>
                </div>
            """, unsafe_allow_html=True)

        # Humidity card
        with col2:
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Humidity</p>
                    <h2 style="margin: 0;">{humidity}%</h2>
                </div>
            """, unsafe_allow_html=True)

        # Wind speed card
        with col3:
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Wind Speed</p>
                    <h2 style="margin: 0;">{wind_speed} {speed_unit}</h2>
                </div>
            """, unsafe_allow_html=True)

        # Sunrise and Sunset times
        st.markdown("<h3>Sunrise & Sunset</h3>", unsafe_allow_html=True)
        col_sun1, col_sun2 = st.columns(2)

        with col_sun1:
            sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M')
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Sunrise</p>
                    <div style="display: flex; align-items: center; justify-content: center;">
                        <h3 style="margin: 0;">{sunrise_time}</h3>
                        <div style="width: 40px; height: 40px; margin-left: 10px;">
                            <img src="https://img.icons8.com/fluency/48/000000/sunrise.png" width="40" height="40"/>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col_sun2:
            sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M')
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Sunset</p>
                    <div style="display: flex; align-items: center; justify-content: center;">
                        <h3 style="margin: 0;">{sunset_time}</h3>
                        <div style="width: 40px; height: 40px; margin-left: 10px;">
                            <img src="https://img.icons8.com/fluency/48/000000/sunset.png" width="40" height="40"/>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Air Quality Information (if available)
        if air_quality_data and 'list' in air_quality_data and len(air_quality_data['list']) > 0:
            aqi = air_quality_data['list'][0]['main']['aqi']
            aqi_info = AQI_DESCRIPTIONS.get(aqi, {"level": "Unknown", "description": "No data available", "color": "#999"})

            st.markdown("<h3>Air Quality</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="glass-card">
                    <p style="margin: 0; font-size: 1.1rem; color: {aqi_info['color']}; font-weight: bold;">
                        {aqi_info['level']}
                    </p>
                    <p style="margin: 5px 0;">
                        {aqi_info['description']}
                    </p>
                    <div class="aqi-indicator">
                        <div class="aqi-marker" style="left: {(aqi-1) * 25}%;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Additional weather details
        with st.expander("More Details", expanded=False):
            col4, col5, col6 = st.columns(3)
            with col4:
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Feels Like</p>
                        <h3 style="margin: 0;">{weather_data["main"]["feels_like"]:.1f}{temp_unit}</h3>
                    </div>
                """, unsafe_allow_html=True)

            with col5:
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Pressure</p>
                        <h3 style="margin: 0;">{weather_data["main"]["pressure"]} hPa</h3>
                    </div>
                """, unsafe_allow_html=True)

            with col6:
                visibility = weather_data.get("visibility", 0) / 1000  # Convert to km
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Visibility</p>
                        <h3 style="margin: 0;">{visibility:.1f} km</h3>
                    </div>
                """, unsafe_allow_html=True)

        # Display 5-day forecast if available
        if forecast_data and 'list' in forecast_data:
            display_forecast(forecast_data, units)

        # Last updated time
        tz = pytz.timezone(TIMEZONE)
        current_time_str = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        st.caption(f"Last updated: {current_time_str}")

    except KeyError as e:
        st.error(f"Missing expected data in weather response: {str(e)}")

def display_forecast(forecast_data: Dict[str, Any], units: str = "metric"):
    """Display 5-day weather forecast"""
    if not forecast_data or 'list' not in forecast_data:
        return

    st.markdown("<h3>5-Day Forecast</h3>", unsafe_allow_html=True)

    # Get daily forecasts (one per day)
    daily_forecasts = []
    current_date = ""

    for item in forecast_data['list']:
        forecast_date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')

        # Only take one forecast per day (at noon if possible)
        forecast_hour = datetime.fromtimestamp(item['dt']).hour
        if forecast_date != current_date:
            daily_forecasts.append(item)
            current_date = forecast_date
        elif len(daily_forecasts) > 0 and abs(forecast_hour - 12) < abs(datetime.fromtimestamp(daily_forecasts[-1]['dt']).hour - 12) and forecast_date == current_date:
            # Replace with a time closer to noon
            daily_forecasts[-1] = item

    # Limit to 5 days
    daily_forecasts = daily_forecasts[:5]

    # Temperature unit
    temp_unit = "°C" if units == "metric" else "°F"

    # Create forecast cards
    st.markdown("""
        <div class="forecast-container">
    """, unsafe_allow_html=True)

    for forecast in daily_forecasts:
        date = datetime.fromtimestamp(forecast['dt']).strftime('%a, %b %d')
        temp = forecast['main']['temp']
        description = forecast['weather'][0]['description']
        icon_url = f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"

        st.markdown(f"""
            <div class="glass-card forecast-card">
                <p style="margin: 0; font-weight: bold;">{date}</p>
                <img src="{icon_url}" width="50" height="50" style="margin: 5px 0;">
                <h3 style="margin: 0;">{temp:.1f}{temp_unit}</h3>
                <p style="margin: 5px 0; font-size: 0.8rem; text-transform: capitalize;">{description}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        </div>
    """, unsafe_allow_html=True)

    # Display temperature chart
    temps = [item['main']['temp'] for item in forecast_data['list'][:8]]
    times = [datetime.fromtimestamp(item['dt']).strftime('%H:%M') for item in forecast_data['list'][:8]]

    st.markdown("<h4>24-Hour Temperature Trend</h4>", unsafe_allow_html=True)

    # Create a simple chart using HTML/CSS
    chart_height = 150
    max_temp = max(temps)
    min_temp = min(temps)
    temp_range = max_temp - min_temp if max_temp != min_temp else 1

    st.markdown(f"""
        <div class="glass-card" style="padding: 15px;">
            <div style="display: flex; height: {chart_height}px; align-items: flex-end; justify-content: space-between;">
    """, unsafe_allow_html=True)

    for i, temp in enumerate(temps):
        height_percent = ((temp - min_temp) / temp_range) * 70 + 20  # At least 20% height

        st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                <div style="margin-bottom: 5px;">{temp:.1f}{temp_unit}</div>
                <div style="background: linear-gradient(to top, rgba(0,123,255,0.7), rgba(0,123,255,0.3));
                            width: 80%; height: {height_percent}%; border-radius: 5px;"></div>
                <div style="margin-top: 5px; font-size: 0.8rem;">{times[i]}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create the sidebar with settings and contact information"""
    with st.sidebar:
        # Weather icon
        st.markdown("""
            <div style="display: flex; justify-content: center; margin: 20px 0;">
                <div style="width: 100px; height: 100px; background-color: #87ceeb;
                     border-radius: 50%; display: flex; justify-content: center; align-items: center;">
                    <span style="font-size: 40px;">🌤️</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="glass-card">
                <h3 style="margin-top: 0;">Weather Magic</h3>
                <p style="opacity: 0.8;">Real-time weather with beautiful animations</p>
            </div>
        """, unsafe_allow_html=True)

        # City input in sidebar with autocomplete
        st.markdown("<h3>📍 Location</h3>", unsafe_allow_html=True)
        st.text_input("Enter City Name", "London", key="sidebar_city",
                     placeholder="Type a city name...")

        # Temperature unit selection
        st.markdown("<h3>🔧 Settings</h3>", unsafe_allow_html=True)

        # Initialize temperature unit in session state if not present
        if 'temp_unit' not in st.session_state:
            st.session_state.temp_unit = "metric"

        # Unit selection
        unit_col1, unit_col2 = st.columns(2)
        with unit_col1:
            metric_selected = st.button("°C (Metric)",
                                      key="metric_unit",
                                      use_container_width=True,
                                      disabled=st.session_state.temp_unit == "metric")
            if metric_selected:
                st.session_state.temp_unit = "metric"
                st.session_state.force_refresh = True
                st.rerun()

        with unit_col2:
            imperial_selected = st.button("°F (Imperial)",
                                        key="imperial_unit",
                                        use_container_width=True,
                                        disabled=st.session_state.temp_unit == "imperial")
            if imperial_selected:
                st.session_state.temp_unit = "imperial"
                st.session_state.force_refresh = True
                st.rerun()

        # Refresh button
        if st.button("🔄 Refresh Weather", key="sidebar_refresh", use_container_width=True):
            st.session_state.force_refresh = True
            st.rerun()

        # Auto-refresh toggle
        auto_refresh = st.toggle("Auto-refresh (5 min)", value=True, key="auto_refresh")
        if not auto_refresh and 'auto_refresh_enabled' in st.session_state:
            st.session_state.auto_refresh_enabled = False
        elif auto_refresh and 'auto_refresh_enabled' not in st.session_state:
            st.session_state.auto_refresh_enabled = True

        st.markdown("---")

        # Contact section
        st.markdown("### 📬 Contact Info")
        st.markdown("""
            <div class="glass-card">
                <p>📧 <a href="mailto:asadullahshafique@hotmail.com">Email</a></p>
                <p>🔗 <a href="https://www.linkedin.com/in/asadullah-shafique-a00679325/">LinkedIn</a></p>
                <p>💬 <a href="https://wa.me/923213771445">WhatsApp</a></p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
            <p style="text-align: center; opacity: 0.7;">
                Built with ❤️ by Asadullah Shafique
            </p>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    configure_page()
    create_sidebar()

    # Get city from sidebar
    city = st.session_state.get("sidebar_city", "London")

    # Get temperature unit from session state
    units = st.session_state.get("temp_unit", "metric")

    # Auto-refresh logic
    if 'last_refresh' not in st.session_state or st.session_state.get("force_refresh", False):
        with st.spinner("🌤️ Fetching weather data..."):

            # Get current weather data
            weather_data = get_weather_data(city, units)

            if weather_data and weather_data.get("cod") == 200:
                # Get coordinates for air quality and forecast
                lat = weather_data.get("coord", {}).get("lat")
                lon = weather_data.get("coord", {}).get("lon")

                # Get forecast data
                forecast_data = get_forecast_data(city, units)

                # Get air quality data if coordinates are available
                air_quality_data = None
                if lat is not None and lon is not None:
                    air_quality_data = get_air_quality_data(lat, lon)

                # Display all weather information
                display_weather_info(weather_data, units, forecast_data, air_quality_data)
            else:
                error_msg = weather_data.get("message", "City not found") if weather_data else "Failed to fetch weather data"
                st.error(f"Error: {error_msg}")

                # Show a search suggestion
                st.markdown("""
                    <div class="glass-card" style="text-align: center;">
                        <p>Please check the city name and try again.</p>
                        <p>Examples: "London", "New York", "Tokyo", "Paris"</p>
                    </div>
                """, unsafe_allow_html=True)

        st.session_state.last_refresh = time.time()
        st.session_state.force_refresh = False

    # Auto-refresh every 5 minutes if enabled
    if 'last_refresh' in st.session_state and st.session_state.get("auto_refresh_enabled", True):
        if time.time() - st.session_state.last_refresh >= REFRESH_INTERVAL:
            st.session_state.force_refresh = True
            st.rerun()

    # Footer with data attribution
    st.markdown("""
        <div style="text-align: center; margin-top: 50px;">
            <p style="opacity: 0.7;">Data provided by <a href="https://openweathermap.org/">OpenWeatherMap</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()