# 🎮 Interactive Hangman Game

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.10%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

A modern, interactive implementation of the classic Hangman word-guessing game with a sleek UI powered by Streamlit.

## ✨ Features

- 🌟 Interactive web-based UI with Streamlit
- 🎯 Multiple word categories (Programming, Animals, Countries, Fruits, Movies)
- 🎭 Visual hangman progression with ASCII art
- 🏆 Score tracking system with streak bonuses
- 💡 Hint system to help when you're stuck
- 📱 Mobile-friendly responsive design
- 🎲 Dynamic difficulty based on word length

## 📸 Screenshots

![Game Screenshot](https://via.placeholder.com/800x450.png?text=Hangman+Game+Screenshot)

## 🚀 Installation & Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/asadullah48/hangman-game.git
   cd hangman-game
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   - For console version:
     ```bash
     python hangman_console.py
     ```
   - For web version:
     ```bash
     streamlit run hangman_streamlit.py
     ```

## 🎮 How to Play

1. Choose a word category
2. Guess one letter at a time
3. Try to reveal the hidden word before the hangman is complete
4. Use hints when needed (small score penalty applies)
5. Track your high score and win streak!

## 🧩 Game Mechanics

- Each incorrect guess brings the hangman closer to completion
- Score is calculated based on:
  - Word length
  - Number of incorrect guesses
  - Word difficulty
  - Current win streak
- Using hints reduces your score slightly
- Try to maintain a winning streak for bonus points!

## 🛠️ Technical Details

The game is implemented in Python with two interface options:
- Console-based version using Python's standard libraries
- Web-based version using Streamlit framework

### Code Structure:

- `hangman_console.py`: Original console-based implementation
- `hangman_streamlit.py`: Web interface implementation
- `requirements.txt`: Required Python packages
- `README.md`: Project documentation

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the game.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Asadullah** - [GitHub Profile](https://github.com/asadullah48)

---

Made with ❤️ and Python"# hangman-game" 
