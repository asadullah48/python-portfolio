# 💣 Minesweeper Game

![Minesweeper Banner](https://minesweepergame.streamlit.app/)

A modern implementation of the classic Minesweeper game with both command-line and web-based interfaces using Streamlit.

## 🎮 Features

- **Two Gameplay Modes**:
  - Command-line interface for terminal enthusiasts
  - Streamlit web application for a graphical experience
- **Game Mechanics**:
  - Variable board sizes (5x5 up to 15x15)
  - Adjustable difficulty levels
  - Flag placement to mark potential bombs
  - Auto-reveal for empty cells
- **UI Improvements**:
  - Emoji-based interface (💣, 🚩, etc.)
  - Timer and move counter
  - Interactive grid-based UI in Streamlit

## 📋 Requirements

- Python 3.6+
- Streamlit (`uv add streamlit`)

## 🚀 Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/asadullah48/minesweeper.git
   cd minesweeper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the command-line version:
   ```bash
   python minesweeper_cli.py
   ```

4. Run the Streamlit web app:
   ```bash
   streamlit run minesweeper_app.py
   ```

## 💻 Command-line Usage

```
🎮 Welcome to Minesweeper! 🎮
Enter 'r row col' to reveal a cell
Enter 'f row col' to flag/unflag a cell
Enter 'q' to quit
```

## 🌐 Streamlit App Preview

The Streamlit app provides an intuitive interface where you can:
- Select board size and difficulty
- Left-click to reveal cells
- Toggle between reveal and flag modes
- Track your progress with a timer and move counter

## 📝 Commit History

- 🎮 Initial game implementation
- 🐛 Fixed bomb counting logic
- ✨ Added flag functionality
- 🖥️ Implemented Streamlit UI
- 📊 Added game statistics tracking
- 🔄 Improved game reset functionality
- 📚 Added documentation and README

## 🛠️ Development Roadmap

- [ ] Add sound effects
- [ ] Implement leaderboard functionality
- [ ] Add themes and customization options
- [ ] Create a mobile-friendly version

## 👨‍💻 Author

**Asadullah** - [GitHub Profile](https://github.com/asadullah48)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details."# minesweeper" 
