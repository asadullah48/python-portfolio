# 🚀 Space Invaders

A classic arcade space shooter game built with Pygame and deployable through Streamlit.

![Space Invaders](https://raw.githubusercontent.com/asadullah48/space-invaders/main/assets/gameplay.png)

## 📋 Features

- 🎮 Simple and intuitive controls
- 👾 Progressive difficulty with advancing levels
- 🛡️ Power-ups (Shield, Extra Life, Rapid Fire)
- 💥 Explosion effects and sound
- 🏆 Score tracking and level progression
- 🌐 Web deployment through Streamlit

## 🔧 Installation

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/asadullah48/space-invaders.git
   cd space-invaders
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python space_invaders.py
   ```

### Streamlit Web Interface

To run the game through the Streamlit web interface:

```bash
streamlit run app.py
```

This will open a web browser with the game deployment interface where you can download and play the game.

## 🎮 Controls

- **Left/Right Arrow Keys**: Move spaceship
- **Space**: Shoot
- **ESC**: Pause/Menu
- **Enter**: Start game / Restart after game over

## 🚀 Power-ups

Collect power-ups to gain special abilities:

- 🔵 **Blue**: Shield (temporary invulnerability)
- 🟢 **Green**: Extra Life
- 🟡 **Yellow**: Rapid Fire (triple shot)

## 📁 Project Structure

```
space-invaders/
├── space_invaders.py   # Main game file
├── app.py              # Streamlit deployment interface
├── requirements.txt    # Python dependencies
├── .streamlit/         # Streamlit configuration
│   └── config.toml     # Streamlit theme and settings
├── assets/             # Game assets
│   ├── player.png
│   ├── enemy.png
│   ├── space_icon.png
│   ├── laser.wav
│   ├── explosion.wav
│   ├── game_over.wav
│   └── background.mp3
├── screenshots/        # Game screenshots for documentation
│   └── gameplay.png
├── LICENSE             # MIT License
└── README.md           # This file
```

## 🛠️ Development

This game was built with:
- Python 3.8+
- Pygame 2.0.0+
- Streamlit 1.23.0+

### Commit History

```
🎮 Initial commit: Basic Space Invaders game
🔧 Added asset loading with error handling
✨ Added power-up system
🎯 Improved collision detection
🔊 Added sound effects and background music
🏆 Added scoring and level progression
📊 Added game states (menu, playing, game over)
🚀 Added Streamlit deployment interface
📝 Added documentation and README
📦 Project structure organization
```

## 🔄 Future Improvements

- [ ] Add different enemy types
- [ ] Implement boss battles
- [ ] Add local high score system
- [ ] Create more power-ups
- [ ] Implement levels with unique backgrounds
- [ ] Add multiplayer support
- [ ] Create mobile-friendly controls
- [ ] Add settings menu for customization

## 🌐 Deployment Options

### Streamlit Cloud

You can deploy the Streamlit app to [Streamlit Cloud](https://streamlit.io/cloud) for free:

1. Fork this repository
2. Sign up for Streamlit Cloud
3. Connect your GitHub account
4. Deploy the app by selecting this repository

### Heroku

You can also deploy to Heroku:

1. Create a Heroku account
2. Install the Heroku CLI
3. Run the following commands:
   ```bash
   heroku create space-invaders-app
   git push heroku main
   ```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Asadullah** - [GitHub Profile](https://github.com/asadullah48)

---

Feel free to contribute to this project by submitting pull requests or opening issues!"# space-invaders" 
