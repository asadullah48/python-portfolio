#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
🌦️ Ultimate Weather Forecast App with Advanced Animations
Featuring Lottie animations, dynamic backgrounds, and premium UI/UX
"""

import streamlit as st
import requests
from datetime import datetime
import time
import pytz
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from streamlit_lottie import st_lottie

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("OPENWEATHER_API_KEY", "da1537f4faec6d6b4b6d1c09b1701e37")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
TIMEZONE = "UTC"
REFRESH_INTERVAL = 300  # 5 minutes in seconds

# Lottie animation URLs (can be replaced with local files)
LOTTIE_URLS = {
    "sunny": "https://assets1.lottiefiles.com/packages/lf20_wnql3h.json",
    "rainy": "https://assets1.lottiefiles.com/packages/lf20_kcsr6fcp.json",
    "cloudy": "https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json",
    "snow": "https://assets1.lottiefiles.com/packages/lf20_2cz3cUM1Ix.json",
    "thunder": "https://assets1.lottiefiles.com/packages/lf20_6cHiEK.json",
    "wind": "https://assets1.lottiefiles.com/packages/lf20_gl9xxn3z.json",
    "default": "https://assets1.lottiefiles.com/packages/lf20_pwohahvd.json"
}

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

    body {{
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBackground 15s ease infinite;
    }}

    /* Glass morphism effect with improved text contrast */
    .glass-card {{
        background: rgba(0, 0, 0, 0.4); /* Darker background for better contrast */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        color: #f0f0f0; /* Light gray text instead of pure white */
    }}

    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }}

    /* Adding text shadow to all text for better readability */
    h1, h2, h3, p, .stMarkdown, .stExpander, .stCaption {{
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        color: #f0f0f0;
    }}

    /* Weather animation container */
    .animation-container {{
        height: 200px;
        margin: 20px 0;
    }}

    /* Input field styling */
    .stTextInput>div>div>input {{
        background: rgba(0, 0, 0, 0.3) !important; /* Darker input background */
        color: #f0f0f0 !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        padding: 10px 15px !important;
    }}

    .stTextInput>div>div>input::placeholder {{
        color: rgba(255,255,255,0.7) !important;
    }}

    /* Button styling */
    .stButton>button {{
        background: rgba(0, 0, 0, 0.3) !important; /* Darker button background */
        color: #f0f0f0 !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        transition: all 0.3s ease !important;
        padding: 10px 24px !important;
    }}

    .stButton>button:hover {{
        background: rgba(0, 0, 0, 0.5) !important;
        transform: scale(1.05);
    }}

    /* Links with better contrast */
    a {{
        color: #9ff0ff !important; /* Light blue for links */
        text-decoration: none !important;
    }}

    a:hover {{
        text-decoration: underline !important;
    }}

    /* Mobile responsiveness */
    @media only screen and (max-width: 600px) {{
        .glass-card {{
            padding: 15px;
            margin-bottom: 15px;
        }}
        
        .stTextInput>div>div>input {{
            padding: 8px 12px !important;
        }}
        
        .stButton>button {{
            padding: 8px 16px !important;
            font-size: 14px !important;
        }}
        
        .animation-container {{
            height: 150px;
        }}
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.2);
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255,255,255,0.3);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255,255,255,0.5);
    }}
    </style>
    """, unsafe_allow_html=True)
def configure_page():
    """Set up Streamlit page configuration"""
    st.set_page_config(
        page_title="Weather Magic",
        page_icon="🌤️",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    load_css()
    
    # App header
    st.markdown("""
        <h1 style="text-align: center; 
                   color: white;
                   font-weight: 700;
                   text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                   margin-bottom: 0;">
            Weather Magic 🌈
        </h1>
        <p style="text-align: center; color: white; opacity: 0.8;">
            Real-time weather with beautiful animations
        </p>
    """, unsafe_allow_html=True)

def get_weather_data(city: str) -> Optional[Dict[str, Any]]:
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
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

def get_weather_animation(weather_condition: str) -> str:
    """Return appropriate Lottie animation based on weather condition"""
    weather_condition = weather_condition.lower()
    if "rain" in weather_condition:
        return LOTTIE_URLS["rainy"]
    elif "cloud" in weather_condition:
        return LOTTIE_URLS["cloudy"]
    elif "sun" in weather_condition or "clear" in weather_condition:
        return LOTTIE_URLS["sunny"]
    elif "snow" in weather_condition:
        return LOTTIE_URLS["snow"]
    elif "thunder" in weather_condition or "storm" in weather_condition:
        return LOTTIE_URLS["thunder"]
    elif "wind" in weather_condition:
        return LOTTIE_URLS["wind"]
    else:
        return LOTTIE_URLS["default"]

def display_weather_info(weather_data: Dict[str, Any]):
    """Display weather information with animations"""
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
        
        # Get appropriate animation
        animation_url = get_weather_animation(description)
        
        # Display city name and animation
        st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="margin: 0; color: white;">{city_name}, {country if country else ''}</h2>
                <p style="margin: 5px 0 15px 0; color: white; text-transform: capitalize; font-size: 1.2rem;">
                    {description}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display Lottie animation
        st_lottie(animation_url, height=200, key="weather-animation")
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        # Temperature card
        with col1:
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Temperature</p>
                    <h2 style="margin: 0;">{temp:.1f}°C</h2>
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
                    <h2 style="margin: 0;">{wind_speed} m/s</h2>
                </div>
            """, unsafe_allow_html=True)
        
        # Additional weather details
        with st.expander("More Details", expanded=False):
            col4, col5 = st.columns(2)
            with col4:
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Feels Like</p>
                        <h3 style="margin: 0;">{weather_data["main"]["feels_like"]:.1f}°C</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Pressure</p>
                        <h3 style="margin: 0;">{weather_data["main"]["pressure"]} hPa</h3>
                    </div>
                """, unsafe_allow_html=True)
        
        # Last updated time
        tz = pytz.timezone(TIMEZONE)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        st.caption(f"Last updated: {current_time}")
        
    except KeyError as e:
        st.error(f"Missing expected data in weather response: {str(e)}")

def create_sidebar():
    """Create the sidebar with contact information"""
    with st.sidebar:
        # Animated weather icon
        st_lottie(LOTTIE_URLS["default"], height=150, key="sidebar-animation")
        
        st.markdown("""
            <div class="glass-card">
                <h3 style="color: white; margin-top: 0;">Weather Magic</h3>
                <p style="color: white; opacity: 0.8;">Real-time weather with beautiful animations</p>
            </div>
        """, unsafe_allow_html=True)
        
        # City input in sidebar
        city = st.text_input("Enter City Name", "London", key="sidebar_city")
        
        # Refresh button
        if st.button("🔄 Refresh Weather", key="sidebar_refresh"):
            st.session_state.force_refresh = True
            st.experimental_rerun()
        
        st.markdown("---")
        
        # Contact section
        st.markdown("### 📬 Contact Info")
        st.markdown("""
            <div class="glass-card">
                <p>📧 <a href="mailto:asadullahshafique@hotmail.com" style="color: white;">Email</a></p>
                <p>🔗 <a href="https://www.linkedin.com/in/asadullah-shafique-a00679325/" style="color: white;">LinkedIn</a></p>
                <p>💬 <a href="https://wa.me/923213771445" style="color: white;">WhatsApp</a></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
            <p style="text-align: center; color: white; opacity: 0.7;">
                Built with ❤️ by Asadullah Shafique
            </p>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    configure_page()
    create_sidebar()
    
    # Get city from sidebar or main input
    city = st.session_state.get("sidebar_city", "London")
    
    # Auto-refresh logic
    if 'last_refresh' not in st.session_state or st.session_state.get("force_refresh", False):
        with st.spinner("🌤️ Fetching weather data..."):
            weather_data = get_weather_data(city)
            if weather_data:
                if weather_data.get("cod") == 200:
                    display_weather_info(weather_data)
                else:
                    st.error(f"Error: {weather_data.get('message', 'City not found')}")
        st.session_state.last_refresh = time.time()
        st.session_state.force_refresh = False
    
    # Auto-refresh every 5 minutes
    if 'last_refresh' in st.session_state:
        if time.time() - st.session_state.last_refresh >= REFRESH_INTERVAL:
            st.session_state.force_refresh = True
            st.experimental_rerun()
    
    # Footer with data attribution
    st.markdown("""
        <div style="text-align: center; margin-top: 50px;">
            <p style="color: white; opacity: 0.7;">Data provided by <a href="https://openweathermap.org/" style="color: white;">OpenWeatherMap</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()