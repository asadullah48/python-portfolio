# 🎮 Tetris Game

A modern implementation of the classic Tetris game with multiple playing options.

![Tetris Game Screenshot](https://via.placeholder.com/600x400?text=Tetris+Game)

## ✨ Features

- 🎯 Classic Tetris gameplay
- 🎚️ Progressive difficulty with levels
- 🏆 High score tracking
- 🔊 Sound effects (in desktop version)
- ⏸️ Pause functionality
- 📱 Play in browser with Streamlit
- 🖥️ Full desktop experience with Pygame

## 🚀 Play Options

### Desktop Application

Run the desktop version with Pygame for the full gaming experience:

```bash
# Install requirements
pip install pygame

# Run the game
python tetris_game.py
```

### Web Version

Play Tetris in your browser using Streamlit:

```bash
# Install requirements
pip install streamlit pygame pillow

# Launch the game
streamlit run tetris_streamlit.py
```

## 🎮 Controls

### Desktop Version
- **Left/Right Arrow Keys**: Move piece horizontally
- **Up Arrow Key**: Rotate piece
- **Down Arrow Key**: Soft drop (move down faster)
- **Space**: Hard drop (instant placement)
- **P**: Pause game

### Web Version
- Use the on-screen control buttons to play

## 📝 Game Rules

1. Tetriminos (shapes) fall from the top of the screen
2. Arrange them to create complete rows
3. Completed rows are cleared and award points
4. The game speeds up as you clear more lines
5. Game ends when the stack reaches the top of the screen

## 🔧 Technical Details

- Built with Python 3.x
- Desktop version uses Pygame
- Web version uses Streamlit and Pygame rendering
- Score and high score persistence

## 💻 Development

Want to contribute? Here's how to set up the development environment:

```bash
# Clone the repository
git clone https://github.com/asadullah48/tetris.git
cd tetris

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

## 📋 Roadmap

- [ ] Add multiplayer functionality
- [ ] Create leaderboard system
- [ ] Add more visual themes
- [ ] Implement touch controls for mobile
- [ ] Add customizable keybindings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Asadullah** - [@asadullah48](https://github.com/asadullah48)

## 🙏 Acknowledgments

- Original Tetris game by Alexey Pajitnov
- Pygame community for the excellent game development library
- Streamlit team for making web deployment easy"# tetris" 
