# 💣 Minesweeper Pro

![Minesweeper Banner](https://minesweepergame.streamlit.app/)

A modern, enhanced implementation of the classic Minesweeper game with both command-line and web-based interfaces using Streamlit. Now with improved UI/UX, professional styling, and additional features!

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
  - Color-coded numbers for better readability
  - Custom CSS styling for a professional look
  - Background image customization (online URLs or local files)
  - Preset background options for quick customization
  - Responsive design for different screen sizes
  - Improved game statistics dashboard

## 📋 Requirements

- Python 3.6+
- Streamlit (`pip install streamlit` or `uv add streamlit`)
- Pillow for image processing
- NumPy for array operations
- Streamlit-extras for enhanced components

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

5. Run the Enhanced Minesweeper Pro version:
   ```bash
   python run_enhanced_minesweeper.py
   ```
   or
   ```bash
   streamlit run enhanced_minesweeper.py
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

### Enhanced Version Features
The enhanced Minesweeper Pro version includes:
- Professional UI with custom styling
- Background image customization:
  - Use online image URLs
  - Use local image files from your computer
  - Choose from preset background options
- Color-coded numbers for easier gameplay
- Improved game statistics dashboard
- Responsive design for different screen sizes
- Better difficulty presets (Beginner, Intermediate, Expert)
- Detailed instructions and tips in the sidebar
- Celebration animations when you win

## 📝 Commit History

- 🎮 Initial game implementation
- 🐛 Fixed bomb counting logic
- ✨ Added flag functionality
- 🖥️ Implemented Streamlit UI
- 📊 Added game statistics tracking
- 🔄 Improved game reset functionality
- 📚 Added documentation and README
- 🎨 Enhanced UI with professional styling
- 🖼️ Added background image support
- 🎯 Improved difficulty presets
- 🎉 Added celebration animations
- 📱 Made design responsive

## 🛠️ Development Roadmap

- [ ] Add sound effects
- [ ] Implement leaderboard functionality
- [ ] Add more themes and customization options
- [ ] Create a mobile-friendly version
- [ ] Add user accounts and save game progress
- [ ] Implement multiplayer functionality
- [ ] Create a dark mode option

## 👨‍💻 Author

**Asadullah** - [GitHub Profile](https://github.com/asadullah48)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details."# minesweeper"
