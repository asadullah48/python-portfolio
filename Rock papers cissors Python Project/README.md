# 🪓 **Project 4: Rock, Paper, Scissors** 🖐️

#### **Description**
This project implements the classic Rock, Paper, Scissors game where the user plays against the computer. The user inputs their choice, and the computer randomly selects one of the three options. The game then determines the winner based on the standard rules of the game.

# 🎮 Rock Paper Scissors Game

A modern, interactive implementation of the classic Rock Paper Scissors game built with Python and Streamlit.

![Rock Paper Scissors Demo](https://github.com/asadullah48/rock-paper-scissors/raw/main/demo.png)

## ✨ Features

- 🎲 Play the classic Rock Paper Scissors game against the computer
- 📊 Track game statistics and win rates
- 📜 View complete game history
- 🌈 Clean, intuitive user interface with emoji feedback
- 🔄 Reset game functionality

## 🚀 Live Demo

Check out the live demo: [Rock Paper Scissors Game](https://rock-paper-scissors-asadullah48.streamlit.app/)

## 🛠️ Installation

Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone https://github.com/asadullah48/rock-paper-scissors.git
cd rock-paper-scissors

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📋 Requirements

The following packages are required:

```
streamlit>=1.27.0
```

These can be installed using the `requirements.txt` file.

## 🏃‍♂️ Running the Application

Run the Streamlit app locally:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## 💻 Code Structure

- `app.py`: The main application file containing the Streamlit UI and game logic
- `requirements.txt`: List of Python dependencies
- `LICENSE`: MIT License file
- `README.md`: This documentation file

## 🧩 How the Game Works

1. Choose your move: Rock, Paper, or Scissors
2. The computer randomly selects its move
3. The winner is determined based on the classic rules:
   - Rock beats Scissors
   - Paper beats Rock
   - Scissors beats Paper
4. Game statistics are updated and displayed

## 🔄 Future Improvements

- ✅ Add sound effects for game actions
- ✅ Implement difficulty levels for the computer opponent
- ✅ Create a multiplayer mode
- ✅ Add animations for the game choices
- ✅ Create a mobile-responsive design

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created by [Asadullah48](https://github.com/asadullah48)

Feel free to contribute to this project by submitting issues or pull requests!

---

#### **Code Overview**

```python
import random

def play():
    options = ["rock", "paper", "scissors"]
    user_choice = input("Choose rock, paper, or scissors: ").lower()
    
    if user_choice not in options:
        print("Invalid choice! Please select rock, paper, or scissors.")
        return play()

    computer_choice = random.choice(options)
    
    print(f"You chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")

    if user_choice == computer_choice:
        print("It's a tie! 🤝")
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        print("You win! 🎉")
    else:
        print("Computer wins! 😢")

play()
```

---

#### **How It Works**

1. **User Input**: The user is asked to choose between "rock", "paper", or "scissors". The input is converted to lowercase to handle case insensitivity.
2. **Input Validation**: If the user's choice is invalid (not one of the three options), the program prints a message and asks the user to input their choice again.
3. **Computer Choice**: The computer randomly selects one of the three options using `random.choice()`.
4. **Comparison**: The program compares the user's choice and the computer's choice to determine the winner:
   - **Tie**: If both choices are the same, it's a tie.
   - **User Wins**: If the user’s choice beats the computer’s choice, the user wins.
   - **Computer Wins**: Otherwise, the computer wins.
5. **Replay**: The game doesn't automatically restart, but if needed, you could add a replay option by calling `play()` again after each round.

---

#### **Example Output**

```
Choose rock, paper, or scissors: paper
You chose: paper
Computer chose: scissors
Computer wins! 😢
```

---

#### **Why Is This Fun?**
🎮 **Interactive**: You play directly against the computer.  
🏆 **Challenge**: Try to outguess the computer's choices!  
💻 **Python Practice**: Practice using conditional statements, random choices, and user input validation.

---
"# rock-paper-scissors" 
