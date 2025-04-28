import streamlit as st
import time
import datetime
import json
import os
from pathlib import Path
import base64

class StreamlitCountdownTimer:
    """A Streamlit-based countdown timer with multiple display modes and controls."""
    
    def __init__(self):
        """Initialize the Streamlit app structure and state."""
        self._initialize_session_state()
        self._setup_app_layout()
        
    def _initialize_session_state(self):
        """Initialize all session state variables."""
        if 'remaining' not in st.session_state:
            st.session_state.remaining = 0
        if 'running' not in st.session_state:
            st.session_state.running = False
        if 'paused' not in st.session_state:
            st.session_state.paused = False
        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0
        if 'end_time' not in st.session_state:
            st.session_state.end_time = 0
        if 'duration' not in st.session_state:
            st.session_state.duration = 0
        if 'theme' not in st.session_state:
            st.session_state.theme = "default"
        if 'presets' not in st.session_state:
            st.session_state.presets = self._load_presets()
        if 'completion_time' not in st.session_state:
            st.session_state.completion_time = None
        if 'timer_name' not in st.session_state:
            st.session_state.timer_name = "Countdown Timer"
        if 'show_finished' not in st.session_state:
            st.session_state.show_finished = False
            
    def _load_presets(self):
        """Load saved timer presets."""
        default_presets = {
            "Quick Break": 300, 
            "Pomodoro": 1500, 
            "Meeting": 1800
        }
        
        # Create presets directory if it doesn't exist
        os.makedirs('presets', exist_ok=True)
        
        preset_path = Path('presets/timer_presets.json')
        if preset_path.exists():
            try:
                with open(preset_path, "r") as f:
                    return json.load(f)
            except Exception:
                return default_presets
        else:
            # Save default presets
            with open(preset_path, "w") as f:
                json.dump(default_presets, f)
            return default_presets
            
    def _save_presets(self):
        """Save current presets to file."""
        preset_path = Path('presets/timer_presets.json')
        try:
            with open(preset_path, "w") as f:
                json.dump(st.session_state.presets, f)
            return True
        except Exception:
            return False
            
    def _format_time(self, seconds):
        """Format time for display with different units based on duration."""
        if seconds < 0:
            seconds = 0
            
        if seconds >= 3600:  # 1 hour or more
            hours, remainder = divmod(seconds, 3600)
            mins, secs = divmod(remainder, 60)
            return f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
        else:
            mins, secs = divmod(seconds, 60)
            return f"{int(mins):02d}:{int(secs):02d}"
            
    def _start_timer(self):
        """Start the countdown timer."""
        duration = st.session_state.duration
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.start_time = time.time()
        st.session_state.end_time = st.session_state.start_time + duration
        st.session_state.remaining = duration
        st.session_state.completion_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        st.session_state.show_finished = False
        
    def _pause_timer(self):
        """Pause the countdown timer."""
        st.session_state.paused = True
        
    def _resume_timer(self):
        """Resume the countdown timer."""
        st.session_state.paused = False
        st.session_state.end_time = time.time() + st.session_state.remaining
        
    def _stop_timer(self):
        """Stop the countdown timer."""
        st.session_state.running = False
        st.session_state.show_finished = False
        
    def _add_time(self, seconds):
        """Add time to the current countdown."""
        if st.session_state.running:
            st.session_state.end_time += seconds
            st.session_state.remaining += seconds
            if st.session_state.completion_time:
                st.session_state.completion_time += datetime.timedelta(seconds=seconds)
            
    def _update_timer(self):
        """Update the timer remaining time."""
        if st.session_state.running and not st.session_state.paused:
            current_time = time.time()
            st.session_state.remaining = max(0, st.session_state.end_time - current_time)
            
            # Check if timer has ended
            if st.session_state.remaining <= 0 and not st.session_state.show_finished:
                st.session_state.running = False
                st.session_state.show_finished = True
                
    def _create_preset(self, name, seconds):
        """Create a new timer preset."""
        if name and seconds > 0:
            st.session_state.presets[name] = seconds
            self._save_presets()
            return True
        return False
        
    def _delete_preset(self, name):
        """Delete an existing timer preset."""
        if name in st.session_state.presets:
            del st.session_state.presets[name]
            self._save_presets()
            return True
        return False
        
    def _get_theme_colors(self):
        """Get color scheme based on selected theme."""
        themes = {
            "default": {
                "progress_color": "blue",
                "bg_color": "#f0f2f6",
                "text_color": "black",
                "bg_image": "linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%)"
            },
            "dark": {
                "progress_color": "green",
                "bg_color": "#262730",
                "text_color": "white",
                "bg_image": "linear-gradient(to right, #434343 0%, black 100%)"
            },
            "ocean": {
                "progress_color": "#0083B8",
                "bg_color": "#E1F2F7",
                "text_color": "#00557A",
                "bg_image": "linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%)"
            },
            "sunset": {
                "progress_color": "#FF5F1F",
                "bg_color": "#FFF3E0",
                "text_color": "#A63F03",
                "bg_image": "linear-gradient(to right, #ff8177 0%, #ff867a 0%, #ff8c7f 21%, #f99185 52%, #cf556c 78%, #b12a5b 100%)"
            }
        }
        return themes.get(st.session_state.theme, themes["default"])
        
    def _get_css(self):
        """Generate custom CSS based on theme."""
        colors = self._get_theme_colors()
        
        return f"""
        <style>
            .stApp {{
                background: {colors['bg_image']};
            }}
            .timer-container {{
                background-color: {colors['bg_color']};
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px 0;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
            }}
            .timer-display {{
                font-size: 72px;
                font-weight: bold;
                color: {colors['text_color']};
                font-family: 'Courier New', monospace;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }}
            .timer-finished {{
                animation: pulse 1.5s infinite;
                color: #FF5252;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            .completion-time {{
                font-size: 14px;
                color: {colors['text_color']};
                opacity: 0.8;
                margin-top: 5px;
            }}
            .stButton button {{
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                backdrop-filter: blur(5px);
                transition: all 0.3s ease;
            }}
            .stButton button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .stProgress > div > div > div > div {{
                background-color: {colors['progress_color']};
            }}
            .stSelectbox, .stNumberInput {{
                background: rgba(255,255,255,0.1);
                border-radius: 5px;
                backdrop-filter: blur(5px);
            }}
        </style>
        """
        
    def _setup_app_layout(self):
        """Set up the main Streamlit app interface."""
        # Set page config
        st.set_page_config(
            page_title="Advanced Countdown Timer",
            page_icon="⏱️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Apply custom CSS
        st.markdown(self._get_css(), unsafe_allow_html=True)
        
        # Hide Streamlit default menu and footer
        hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display: none;}
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        
        # Title and description with custom styling
        st.markdown("""
            <h1 style='text-align: center; color: #333; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
                ⏱️ Advanced Countdown Timer
            </h1>
            <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
                A feature-rich countdown timer web app with presets and themes
            </p>
        """, unsafe_allow_html=True)
        
        # Create layout with columns
        col1, col2 = st.columns([3, 1])
        
        with col2:
            # Settings sidebar
            st.subheader("⚙️ Settings")
            
            # Theme selection
            theme_options = ["default", "dark", "ocean", "sunset"]
            st.session_state.theme = st.selectbox(
                "Select Theme",
                theme_options,
                index=theme_options.index(st.session_state.theme) if st.session_state.theme in theme_options else 0
            )
            
            # Timer name
            st.session_state.timer_name = st.text_input("Timer Name", st.session_state.timer_name)
            
            # Timer input
            st.subheader("⏲️ Set Timer")
            
            # Manual time input
            hours = st.number_input("Hours", min_value=0, max_value=23, step=1)
            minutes = st.number_input("Minutes", min_value=0, max_value=59, step=1)
            seconds = st.number_input("Seconds", min_value=0, max_value=59, step=5)
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if st.button("Set Timer") and total_seconds > 0:
                st.session_state.duration = total_seconds
                self._start_timer()
                st.rerun()  # Updated from experimental_rerun
            
            # Presets section
            st.subheader("🔖 Timer Presets")
            
            # Select from existing presets
            preset_options = list(st.session_state.presets.keys())
            if preset_options:
                selected_preset = st.selectbox("Select Preset", [""] + preset_options)
                if selected_preset and st.button("Load Preset"):
                    st.session_state.duration = st.session_state.presets[selected_preset]
                    self._start_timer()
                    st.rerun()  # Updated from experimental_rerun
            
            # Create new preset
            st.subheader("➕ Create Preset")
            preset_name = st.text_input("Preset Name")
            preset_minutes = st.number_input("Minutes", min_value=0, max_value=180, step=1, key="preset_minutes")
            
            if st.button("Save Preset") and preset_name and preset_minutes > 0:
                self._create_preset(preset_name, preset_minutes * 60)
                st.success(f"Preset '{preset_name}' saved!")
                st.rerun()  # Updated from experimental_rerun
                
            # Delete preset
            if preset_options:
                st.subheader("🗑️ Delete Preset")
                preset_to_delete = st.selectbox("Select to Delete", [""] + preset_options, key="delete_preset")
                if preset_to_delete and st.button("Delete", type="primary"):
                    self._delete_preset(preset_to_delete)
                    st.success(f"Preset '{preset_to_delete}' deleted!")
                    st.rerun()  # Updated from experimental_rerun
        
        with col1:
            # Main timer display
            self._update_timer()
            
            # Timer container
            st.markdown(
                f"""
                <div class="timer-container">
                    <h2>{st.session_state.timer_name}</h2>
                    <div class="timer-display {'timer-finished' if st.session_state.show_finished else ''}">
                        {self._format_time(st.session_state.remaining)}
                    </div>
                    {f'<div class="completion-time">Finishes at: {st.session_state.completion_time.strftime("%H:%M:%S")}</div>' if st.session_state.completion_time and st.session_state.running else ''}
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Progress bar
            if st.session_state.running or st.session_state.show_finished:
                progress_percentage = 1.0 - min(1.0, max(0, st.session_state.remaining / st.session_state.duration))
                st.progress(progress_percentage)
            
            # Timer finished message
            if st.session_state.show_finished:
                st.balloons()
                st.success("⏰ Time's up! 🎉")
            
            # Timer controls
            st.subheader("⌨️ Controls")
            
            # Button row 1
            col_b1, col_b2, col_b3 = st.columns(3)
            
            with col_b1:
                if not st.session_state.running:
                    if st.button("▶️ Start", use_container_width=True):
                        if st.session_state.duration > 0:
                            self._start_timer()
                            st.rerun()  # Updated from experimental_rerun
                        else:
                            st.warning("Please set a duration first")
                else:
                    if st.session_state.paused:
                        if st.button("▶️ Resume", use_container_width=True):
                            self._resume_timer()
                            st.rerun()  # Updated from experimental_rerun
                    else:
                        if st.button("⏸️ Pause", use_container_width=True):
                            self._pause_timer()
                            st.rerun()  # Updated from experimental_rerun
            
            with col_b2:
                if st.session_state.running:
                    if st.button("⏹️ Stop", use_container_width=True):
                        self._stop_timer()
                        st.rerun()  # Updated from experimental_rerun
            
            with col_b3:
                if st.session_state.running:
                    if st.button("🔄 Reset", use_container_width=True):
                        self._stop_timer()
                        self._start_timer()
                        st.rerun()  # Updated from experimental_rerun
            
            # Quick buttons row
            if st.session_state.running:
                st.subheader("⏱️ Quick Time Adjust")
                col_q1, col_q2, col_q3, col_q4 = st.columns(4)
                
                with col_q1:
                    if st.button("+10s", use_container_width=True):
                        self._add_time(10)
                        st.rerun()  # Updated from experimental_rerun
                
                with col_q2:
                    if st.button("+1m", use_container_width=True):
                        self._add_time(60)
                        st.rerun()  # Updated from experimental_rerun
                        
                with col_q3:
                    if st.button("+5m", use_container_width=True):
                        self._add_time(300)
                        st.rerun()  # Updated from experimental_rerun
                
                with col_q4:
                    if st.button("+10m", use_container_width=True):
                        self._add_time(600)
                        st.rerun()  # Updated from experimental_rerun
            
            # Common timer buttons
            st.subheader("⏱️ Quick Start")
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            with col_c1:
                if st.button("5 mins", use_container_width=True):
                    st.session_state.duration = 300
                    self._start_timer()
                    st.rerun()  # Updated from experimental_rerun
            
            with col_c2:
                if st.button("10 mins", use_container_width=True):
                    st.session_state.duration = 600
                    self._start_timer()
                    st.rerun()  # Updated from experimental_rerun
            
            with col_c3:
                if st.button("25 mins", use_container_width=True):
                    st.session_state.duration = 1500
                    self._start_timer()
                    st.rerun()  # Updated from experimental_rerun
            
            with col_c4:
                if st.button("60 mins", use_container_width=True):
                    st.session_state.duration = 3600
                    self._start_timer()
                    st.rerun()  # Updated from experimental_rerun
        
        # Footer
        st.markdown("---")
        st.markdown("Created with ❤️ by Asadullah | [GitHub](https://github.com/asadullah48)")
        
        # Set up auto-refresh
        if st.session_state.running and not st.session_state.paused:
            st.experimental_set_query_params(refresh=int(time.time()))
            st.rerun()  # Updated from experimental_rerun

# Run the app
if __name__ == "__main__":
    app = StreamlitCountdownTimer()
