# 🎮 Advanced Tic Tac Toe AI

A modern implementation of the classic Tic Tac Toe game with an unbeatable AI opponent using the Minimax algorithm. Play against an AI with adjustable difficulty levels in your browser with a sleek, professional interface!

![Tic Tac Toe Game Screenshot](https://i.ytimg.com/vi/mcP9qehN1_Q/maxresdefault.jpg)


## ✨ Features

- 🤖 Smart AI opponent using Minimax algorithm with alpha-beta pruning
- 🎚️ Three difficulty levels: Easy, Medium, and Hard
- 📊 Advanced game statistics with visualizations
- 📜 Detailed move history recording
- 🔄 Option to switch between X and O
- 🎨 Multiple theme options (Classic, Dark, Neon, Pastel)
- 🏆 Achievement system to track your progress
- 📱 Responsive design - play on desktop or mobile
- 💾 Game history persistence with SQLite database
- 📈 Performance tracking across different difficulty levels

## 🚀 Live Demo

Check out the live demo [here](https://tictactoe-ai-asadullah48.streamlit.app)

## 🛠️ Technologies Used

- **Streamlit**: For the web interface and interactive components
- **Python**: Core programming language
- **Minimax Algorithm**: For the AI opponent's decision making
- **Alpha-Beta Pruning**: For optimization of the AI's search process
- **SQLite**: For persistent storage of game history and achievements
- **Pandas**: For data manipulation and statistics
- **Custom CSS**: For enhanced visual styling and themes

## 📋 How to Play

1. Choose your preferred theme and difficulty level from the settings tab
2. Click on any empty cell to place your mark
3. Try to get three of your marks in a row (horizontally, vertically, or diagonally)
4. The AI will make its move automatically after you place your mark
5. Track your progress in the statistics tab and unlock achievements as you play
6. View your move history and game duration in real-time

## 🖥️ Local Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone this repository:
```bash
git clone https://github.com/asadullah48/tictactoe-ai.git
cd tictactoe-ai
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to http://localhost:8501

### Database

The application automatically creates a SQLite database (`tictactoe.db`) to store:
- Game history and statistics
- Achievements and progress
- Performance metrics across different difficulty levels

## 📊 Game Modes

### Easy Mode
The AI occasionally makes random moves and doesn't look far ahead in the game tree, making it possible for beginners to win.

### Medium Mode
The AI uses strategic moves but limited look-ahead, providing a moderate challenge.

### Hard Mode
The AI is unbeatable, using the full power of the Minimax algorithm with alpha-beta pruning.

## 🧠 About the Algorithm

The game uses the Minimax algorithm with alpha-beta pruning, a decision-making algorithm commonly used in two-player turn-based games. The algorithm recursively evaluates all possible moves, assuming both players play optimally.

Key aspects:
- **Minimax**: Evaluates all possible future moves, assuming optimal play
- **Alpha-Beta Pruning**: Optimizes by eliminating branches that won't affect the final decision
- **Difficulty Adjustment**: Limits search depth and introduces randomness for easier levels

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## 🏆 Achievements System

The game includes an achievements system to make gameplay more engaging:

- **First Win**: Win your first game against the AI
- **Master Strategist**: Win a game on Hard difficulty
- **Speed Demon**: Win a game in less than 10 seconds
- **Hat Trick**: Win 3 games in a row
- **Persistence**: Play 10 games

## 🎨 Themes

Choose from multiple visual themes to customize your gaming experience:

- **Classic**: Traditional blue and red on white background
- **Dark**: Modern dark mode with softer colors
- **Neon**: Vibrant cyberpunk-inspired colors
- **Pastel**: Soft, soothing color palette

## 🙏 Acknowledgements

- Original Pygame implementation inspired by classic game tutorials
- Streamlit for making web deployment straightforward
- Community feedback for UI/UX improvements

---

Developed with ❤️ by [Asadullah48](https://github.com/asadullah48)
