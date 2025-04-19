# ⏱️ Advanced Countdown Timer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://advanced-countdown-timer.streamlit.app/)
![License](https://img.shields.io/github/license/asadullah48/countdown-timer)
![GitHub last commit](https://img.shields.io/github/last-commit/asadullah48/countdown-timer)

A feature-rich countdown timer application with both command-line and web interfaces. Perfect for productivity, time management, and task scheduling.

## 🌟 Features

- **Multiple Interfaces**: Command-line and web app (Streamlit) versions
- **Rich Visualization**: Progress bars, digital displays, and visual feedback
- **User Controls**: Pause, resume, stop, and add/remove time on-the-fly
- **Presets System**: Save and reuse your common timer durations
- **Themes**: Choose from multiple visual themes
- **Sound Alerts**: Audio notifications when timers complete
- **Responsive Design**: Works on desktop and mobile devices (web version)

## 📦 Installation

### Command-line Version

```bash
# Clone the repository
git clone https://github.com/asadullah48/countdown-timer.git
cd countdown-timer

# Run the command-line version
python countdown_timer.py
```

### Web Application (Streamlit)

```bash
# Install requirements
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_timer.py
```

## 🚀 Deployment

The Streamlit version can be easily deployed to Streamlit Cloud:

1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy the app from your forked repository

## 💻 Usage

### Command-line Version

The CLI version supports:
- Timer presets with custom names
- Multiple themes
- Interactive controls during countdown
- Sound notifications

```
# Basic usage
python countdown_timer.py

# Follow the on-screen prompts to set duration and control the timer
```

### Streamlit Web App

The web app offers:
- Visual timer with progress indication
- Theme selection
- Timer presets management
- Quick timer buttons
- Time adjustment controls
- Completion notifications

Open the app in your browser and use the intuitive interface to manage your timers.

## 🔧 Customization

### Adding New Presets

Command-line version:
```
# When prompted for time, use the format:
PresetName:seconds
```

Web version:
- Use the "Create Preset" section to add new timer presets

### Changing Themes

Command-line version:
- Select theme when prompted at startup

Web version:
- Use the "Select Theme" dropdown in the settings panel

## 📊 Project Structure

```
countdown-timer/
├── countdown_timer.py      # Command-line interface version
├── streamlit_timer.py      # Streamlit web application
├── requirements.txt        # Python dependencies
├── presets/                # Saved timer presets
│   └── timer_presets.json
└── README.md               # Documentation
```

## 📋 Requirements

- Python 3.7+
- Streamlit (for web app)
- Unix-like system for best terminal experience (command-line version)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b)    "# countdown-timer" 
