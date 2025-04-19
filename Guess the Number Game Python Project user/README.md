# 🧠 Mind Reader: Computer Guesses Your Number

![Mind Reader Game](https://img.shields.io/badge/Game-Mind%20Reader-blue)
![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A captivating interactive game where the computer reads your mind and guesses your secret number! Built with Streamlit and enhanced with beautiful visualizations.

![Game Screenshot](https://raw.githubusercontent.com/streamlit/streamlit/develop/examples/streamlit_app_screenshot.png)

## 🎮 Play Online

Try the game online at:
[Mind Reader Game](https://asadullah48-mind-reader.streamlit.app/)

## ✨ Features

- 🧠 Smart computer guesser using binary search algorithm
- 📊 Real-time visualization of guesses
- 🎯 Multiple difficulty levels (Easy, Normal, Hard, Extreme)
- ⏱️ Timer and performance tracking
- 🏆 Leaderboard and achievements system
- 📱 Responsive design for both desktop and mobile
- 📈 Game statistics and performance metrics
- 🎨 Beautiful UI with animations
- 🔓 Progressive difficulty unlocking system

## 🚀 How to Play

1. Think of a secret number within the specified range
2. The computer will make a guess
3. Tell the computer if its guess is:
   - Too low (click "Higher")
   - Too high (click "Lower")
   - Correct (click "Correct!")
4. Keep providing feedback until the computer guesses correctly
5. Try to beat the optimal number of guesses!

## 📋 Requirements

- Python 3.7+
- Streamlit
- Pandas
- Altair

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/asadullah48/mind-reader-game.git
cd mind-reader-game

# Install the requirements
pip install streamlit pandas altair

# Run the app
streamlit run app.py
```

## 🧩 How It Works

The game uses a binary search algorithm to efficiently guess your number:

1. Start with the middle of the current range as a guess
2. Based on feedback (higher/lower), eliminate half of the remaining range
3. Repeat until the correct number is found

With this approach, the computer can find any number in the range [1, n] in at most log₂(n) guesses!

## 🔧 Code Structure

- `SmartComputerGuesser`: The core class implementing binary search algorithm
- `calculate_optimal_guesses`: Calculates the theoretical optimal number of guesses
- `animate_success`: Creates visual feedback for successful guesses
- `create_number_guessing_app`: Main function that builds the Streamlit app interface

## 🔮 Future Enhancements

- [ ] Add multiplayer mode
- [ ] Implement daily challenges
- [ ] Create global leaderboard
- [ ] Add sound effects
- [ ] Implement different guessing algorithms
- [ ] Create mobile app version

## 👨‍💻 About the Developer

Created by [Asadullah](https://github.com/asadullah48) as a demonstration of interactive web applications with Streamlit and Python.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💖 Acknowledgements

- [Streamlit](https://www.streamlit.io/) for the amazing framework
- [Altair](https://altair-viz.github.io/) for beautiful visualizations
- [Binary Search Algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm) for the efficient search method"# mind-reader-game" 
