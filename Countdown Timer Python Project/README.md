# ⏱️ Advanced Countdown Timer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://advanced-countdown-timer.streamlit.app/)
![License](https://img.shields.io/github/license/asadullah48/countdown-timer)
![GitHub last commit](https://img.shields.io/github/last-commit/asadullah48/countdown-timer)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit Version](https://img.shields.io/badge/streamlit-1.28%2B-red)](https://streamlit.io/)

A feature-rich countdown timer application with both command-line and web interfaces. Perfect for productivity, time management, and task scheduling. Built with Python and Streamlit, featuring a modern UI with customizable themes and real-time updates.

[Live Demo](https://advanced-countdown-timer.streamlit.app/) | [Report Bug](https://github.com/asadullah48/countdown-timer/issues) | [Request Feature](https://github.com/asadullah48/countdown-timer/issues)

## 🌟 Features

### Core Features
- **Multiple Interfaces**: Command-line and web app (Streamlit) versions
- **Rich Visualization**: Progress bars, digital displays, and visual feedback
- **User Controls**: Pause, resume, stop, and add/remove time on-the-fly
- **Presets System**: Save and reuse your common timer durations

### UI/UX Features
- **Modern Design**: Clean, responsive interface with glassmorphism effects
- **Theme System**: Choose from multiple visual themes:
  - Default (Light)
  - Dark Mode
  - Ocean Theme
  - Sunset Theme
- **Visual Feedback**: Progress indicators and animations
- **Sound Alerts**: Audio notifications when timers complete

### Technical Features
- **Real-time Updates**: Live countdown without page refreshes
- **State Management**: Persistent timer state across sessions
- **Responsive Design**: Works on desktop and mobile devices
- **Keyboard Shortcuts**: Quick controls for common actions

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Command-line Version

```bash
# Clone the repository
git clone https://github.com/asadullah48/countdown-timer.git
cd countdown-timer

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the command-line version
python countdown_timer.py
```

### Web Application (Streamlit)

```bash
# Install requirements if not already done
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_timer.py
```

## 🚀 Deployment

### Streamlit Cloud Deployment
1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy the app from your forked repository
4. Configure environment variables if needed

### Manual Deployment
```bash
# Clone repository
git clone https://github.com/asadullah48/countdown-timer.git

# Install dependencies
pip install -r requirements.txt

# Start the application
streamlit run streamlit_timer.py --server.port $PORT
```

## 💻 Usage

### Command-line Version

```bash
# Basic usage
python countdown_timer.py

# With preset (format: PresetName:seconds)
python countdown_timer.py --preset "Pomodoro:1500"

# With theme
python countdown_timer.py --theme dark
```

### Web Application Features

#### Timer Controls
- **Start/Stop**: Begin or end countdown
- **Pause/Resume**: Temporarily halt countdown
- **Add/Remove Time**: Adjust duration during countdown
- **Reset**: Return to initial state

#### Preset Management
- Create custom presets
- Load saved presets
- Delete unwanted presets
- Export/Import preset configurations

#### Theme Customization
- Switch between visual themes
- Automatic dark mode detection
- Custom color schemes
- Responsive layout adjustments

## 🔧 Configuration

### Environment Variables
```env
STREAMLIT_THEME=dark
STREAMLIT_SERVER_PORT=8501
SOUND_ENABLED=true
```

### Custom Themes
Create new themes by adding to `_get_theme_colors()`:
```python
"custom_theme": {
    "progress_color": "#YOUR_COLOR",
    "bg_color": "#YOUR_BG_COLOR",
    "text_color": "#YOUR_TEXT_COLOR",
    "bg_image": "YOUR_GRADIENT"
}
```

## 📊 Project Structure

```
countdown-timer/
├── countdown_timer.py      # Command-line interface
├── streamlit_timer.py      # Streamlit web application
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project metadata
├── presets/               # Timer presets directory
│   └── timer_presets.json # Saved presets
├── static/                # Static assets
│   ├── sounds/           # Audio notifications
│   └── images/           # UI images
├── tests/                 # Test suite
└── README.md             # Documentation
```

## 📋 Technical Requirements

- **Python**: 3.8+
- **Streamlit**: 1.28+
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Browser**: Modern web browser for web interface
- **Storage**: Local storage for presets
- **Memory**: Minimal (< 100MB)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Python Community](https://www.python.org/psf/) for support
- All contributors who have helped this project grow

## 📬 Contact

Asadullah - [@asadullah48](https://github.com/asadullah48)

Project Link: [https://github.com/asadullah48/countdown-timer](https://github.com/asadullah48/countdown-timer)

---
Made with ❤️ by Asadullah


