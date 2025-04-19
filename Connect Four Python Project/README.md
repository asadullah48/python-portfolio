# 🎮 Connect Four Game

![Connect Four Screenshot]
./assets/screenshot.png

A Python implementation of the classic Connect Four game using Pygame, with Streamlit deployment option.

# 🎮 Connect Four Game

![Connect Four Game](https://img.shields.io/badge/Game-Connect%20Four-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A classic Connect Four game with both web-based (Streamlit) and command-line interface (CLI) versions.

![Game Screenshot](https://via.placeholder.com/800x400?text=Connect+Four+Game)

## 🚀 Features

- 🎲 Classic Connect Four gameplay
- 🖥️ Two game modes:
  - Web application built with Streamlit
  - Command-line interface for terminal play
- 🎨 Visually appealing game board
- 🏆 Win detection for horizontal, vertical, and diagonal connections
- 🤝 Draw detection when the board is full
- 🔄 Easy game reset functionality
- 📱 Responsive design for the web version

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/asadullah48/connect-four-game.git
   cd connect-four-game
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 How to Play

### Web Version (Streamlit)

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

3. Click on column buttons (1-7) to drop your pieces and try to connect four in a row!

### CLI Version

1. Run the CLI version directly:
   ```bash
   python connect-four.py
   ```

2. Follow the on-screen instructions to play in your terminal

### Game Rules

- Players take turns dropping colored discs into the board
- Red always goes first, followed by Yellow
- The first player to connect 4 discs in a row (horizontally, vertically, or diagonally) wins
- If the board fills up without a winner, the game is a draw

## 📋 Requirements

The following dependencies are required:

```
streamlit>=1.28.0
pygame>=2.1.0
numpy>=1.22.0
pillow>=9.0.0
```

Note: The CLI version only requires numpy and can run without the other dependencies.

## 🚀 Deployment

### Web Version

The Streamlit version can be deployed to Streamlit Cloud for free:

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Select the main file (app.py)
5. Click "Deploy"

### CLI Version

The CLI version can be run on any system with Python 3.7+ and NumPy installed. It doesn't require any web deployment.

## 🧠 How It Works

Both versions share the same core game logic:

1. A game board is represented as a 6x7 grid (rows x columns)
2. Players take turns selecting columns to drop their pieces
3. Gravity pulls pieces to the lowest available position in a column
4. The game checks for winning connections after each move
5. When a win or draw is detected, the game ends

The web version uses:
- **Streamlit** for the interface and interactive elements
- **Pygame** for rendering the game board
- **PIL/Pillow** for image processing

The CLI version uses:
- **NumPy** for board state management
- **ANSI color codes** for colored terminal output

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Asadullah**
- GitHub: [@asadullah48](https://github.com/asadullah48)

---

Enjoy the game! 🎮