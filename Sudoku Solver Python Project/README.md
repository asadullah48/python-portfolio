# 🧩 Sudoku Solver & Game

A beautiful, interactive Sudoku game and solver built with Streamlit.

![Sudoku Screenshot](https://raw.githubusercontent.com/asadullah48/sudoku-solver/main/game.png)

## ✨ Features

- 🎮 Interactive Sudoku game with four difficulty levels
- 🎯 Real-time validation of moves
- 💡 Hint system to help when you're stuck
- ⏱️ Game timer to track your solving speed
- 🔄 Reset and solve options
- 📱 Responsive design that works on desktop and mobile
- 🌈 Beautiful, clean UI

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

1. Select a difficulty level (Easy, Medium, Hard, or Expert)
2. Click on "New Game" to start
3. Select a cell by using the row and column selectors
4. Enter numbers using the number buttons
5. Use the "Hint" button if you need help
6. Complete the grid following these rules:
   - Each row must contain all numbers from 1-9 without repetition
   - Each column must contain all numbers from 1-9 without repetition
   - Each 3x3 box must contain all numbers from 1-9 without repetition

## 📝 Game Controls

- **New Game**: Start a new puzzle with selected difficulty
- **Hint**: Get help with a cell (increases hint counter)
- **Solve Puzzle**: Automatically solve the current puzzle
- **Reset Puzzle**: Reset the current puzzle to its initial state
- **Select Cell**: Choose a cell to modify
- **Number Buttons**: Enter a number in the selected cell

## 📊 Game Statistics

The game tracks:
- Time elapsed
- Number of hints used
- Number of mistakes made

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
