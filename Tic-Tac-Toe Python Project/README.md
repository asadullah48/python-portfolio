# 🎮 Tic Tac Toe Game

![License](https://img.shields.io/github/license/asadullah48/tic-tac-toe)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.20%2B-red)
![Pygame](https://img.shields.io/badge/pygame-2.1%2B-green)

A modern implementation of the classic Tic Tac Toe game with both desktop (Pygame) and web (Streamlit) versions.

## ✨ Features

- 🎯 Two implementations: Desktop (Pygame) and Web (Streamlit)
- 👥 Two play modes: Player vs Player and Player vs Computer
- 🧠 Three AI difficulty levels:
  - 🟢 Easy: Random moves
  - 🟡 Medium: Mix of random and optimal moves
  - 🔴 Hard: Unbeatable AI using Minimax algorithm with Alpha-Beta pruning
- 📊 Score tracking
- 🎨 Modern and clean UI
- 🔊 Sound effects (in Pygame version)
- 📱 Responsive design (in Streamlit version)

## 🚀 Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/asadullah48/tic-tac-toe.git
   cd tic-tac-toe
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

#### Desktop Version (Pygame)
```bash
python pygame_tictactoe.py
```

#### Web Version (Streamlit)
```bash
streamlit run streamlit_tictactoe.py
```

## 🎯 How to Play

### Desktop Version
- Click on any empty cell to place your mark
- Press `R` to restart the game
- Press `M` to return to the main menu
- Use the main menu to select game mode and difficulty

### Web Version
- Click on any empty cell to place your mark
- Use the buttons to select game mode and difficulty
- Click "New Game" to restart while keeping scores
- Click "Reset Scores" to start completely fresh

## 💻 Implementation Details

### Pygame Version
The desktop version is implemented using Pygame and features:
- Smooth animations
- Sound effects
- Full menu system
- Optimized AI using the Minimax algorithm

### Streamlit Version
The web version is implemented using Streamlit and features:
- Clean, responsive web interface
- Session-based state management
- Interactive elements

## 🧠 AI Implementation

The computer opponent uses a Minimax algorithm with Alpha-Beta pruning for optimal moves. The difficulty levels control how often the AI makes optimal moves:

- **Easy**: Always makes random moves
- **Medium**: 60% optimal moves, 40% random moves
- **Hard**: Always makes optimal moves (unbeatable)

## 📋 Future Improvements

- [ ] Add online multiplayer functionality
- [ ] Create custom themes/skins
- [ ] Implement user accounts and persistent leaderboards
- [ ] Add time-based gameplay modes
- [ ] Create larger board options (4x4, 5x5)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Asadullah48** - [GitHub](https://github.com/asadullah48)

---

Enjoy the game! 🎮 Feel free to contribute or report issues."# tic-tac-toe" 
