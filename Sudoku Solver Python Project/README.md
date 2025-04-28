# 🧩 Sudoku Solver Pro

A professional, feature-rich Sudoku game and solver built with Streamlit.

![Sudoku Screenshot](https://raw.githubusercontent.com/asadullah48/sudoku-solver/main/game.png)

## ✨ Features

### 🎮 Game Features
- Interactive Sudoku game with four difficulty levels
- Real-time validation of moves
- Hint system to help when you're stuck
- Game timer with pause functionality
- Reset and solve options
- Game history tracking
- Difficulty rating display

### 📝 Notes System
- Manual notes mode for advanced solving techniques
- Auto-notes feature to fill in all possible candidates
- Clear notes option
- Visual note display in a 3x3 grid

### 🎨 UI Features
- Dark/Light mode toggle
- Multiple color themes
- Highlight related cells (same row, column, and box)
- Responsive design that works on desktop and mobile
- Professional background and styling
- Animations and visual feedback

## 🚀 Live Demo

Try it out now! [Sudoku Solver App](https://sudoku-solver-asadullah48.streamlit.app/)

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository
```bash
git clone https://github.com/asadullah48/sudoku-solver.git
cd sudoku-solver
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
streamlit run app.py
```

5. Open your browser and go to `http://localhost:8501`

## 🎮 How to Play

### Basic Rules
1. Fill the 9×9 grid with digits 1-9
2. Each row must contain all digits 1-9 without repetition
3. Each column must contain all digits 1-9 without repetition
4. Each 3×3 box must contain all digits 1-9 without repetition

### Getting Started
1. Select a difficulty level (Easy, Medium, Hard, or Expert)
2. Click on "New Game" to start
3. Select a cell by using the row and column selectors
4. Enter numbers using the number buttons
5. Use the "Hint" button if you need help

### Advanced Features
- Toggle "Notes Mode" to add small candidate numbers in cells
- Use "Auto Notes" to automatically fill in all possible candidates
- Toggle "Highlight Related Cells" to see cells in the same row, column, and box
- Switch between light and dark mode for comfortable play in any environment
- View your game history to track your progress over time

## 📝 Game Controls

### Main Controls
- **New Game**: Start a new puzzle with selected difficulty
- **Hint**: Get help with a cell (increases hint counter)
- **Solve Puzzle**: Automatically solve the current puzzle
- **Reset Puzzle**: Reset the current puzzle to its initial state
- **Select Cell**: Choose a cell to modify
- **Number Buttons**: Enter a number in the selected cell
- **Clear Cell**: Remove the number from the selected cell

### Notes Features
- **Notes Mode**: Toggle between entering numbers and notes
- **Auto Notes**: Automatically fill in all possible candidates for empty cells
- **Clear Notes**: Remove all notes from the selected cell
- **Clear All Notes**: Remove all notes from the board

### Settings
- **Theme**: Choose from multiple color themes (Blue, Green, Purple, Dark)
- **Dark/Light Mode**: Toggle between dark and light mode
- **Highlight Related Cells**: Toggle highlighting of cells in the same row, column, and box
- **Timer Active**: Toggle the game timer on/off

### Keyboard Shortcuts
- **Number Keys (1-9)**: Enter numbers in the selected cell
- **Delete or 0**: Clear the selected cell
- **N**: Toggle notes mode
- **Arrow Keys**: Navigate the grid

## 📊 Game Statistics

### Real-time Stats
The game tracks in real-time:
- Time elapsed (with pause functionality)
- Number of hints used
- Number of mistakes made

### Game History
The app maintains a history of your completed games, including:
- Date and time
- Difficulty level
- Completion time
- Number of hints used
- Number of mistakes made
- Whether the puzzle was completed successfully

## 🧠 Algorithm

The Sudoku solver uses a backtracking algorithm to find the solution:

1. Find an empty cell
2. Try digits 1-9 in that cell
3. Check if the digit is valid in the current position
4. If valid, recursively try to fill the rest of the board
5. If invalid or if the recursive call fails, backtrack

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the wonderful web framework
- [NumPy](https://numpy.org/) for efficient array operations
- All the Sudoku enthusiasts out there!

---

Made with ❤️ by [Asadullah48](https://github.com/asadullah48)"# sudoku-solver"
