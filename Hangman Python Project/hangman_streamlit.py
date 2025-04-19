import streamlit as st
import random
from typing import List, Set

class Hangman:
    """A complete Hangman game implementation with ASCII art and enhanced features."""
    
    HANGMAN_STAGES = [
        """
          +---+
          |   |
              |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
          |   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         /    |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         / \\  |
              |
        =========
        """
    ]

    # Extended word categories for more fun
    WORD_CATEGORIES = {
        "Programming": ["python", "javascript", "algorithm", "database", "function", "variable", "inheritance", "framework"],
        "Animals": ["elephant", "giraffe", "kangaroo", "dolphin", "rhinoceros", "penguin", "tiger", "crocodile"],
        "Countries": ["canada", "brazil", "japan", "australia", "germany", "egypt", "sweden", "thailand"],
        "Fruits": ["apple", "banana", "orange", "strawberry", "pineapple", "watermelon", "blueberry"],
        "Movies": ["avatar", "titanic", "inception", "interstellar", "gladiator", "matrix"],
    }

    def __init__(self):
        """Initialize game with score tracking."""
        self.word = ""
        self.guessed_letters: Set[str] = set()
        self.incorrect_guesses: Set[str] = set()
        self.attempts_left = 6
        self.score = 0
        self.category = ""
        self.game_over = False
        self.win = False
        self.streak = 0
        self.high_score = 0

    def choose_word(self, category=None) -> None:
        """Select a random word and category."""
        if category:
            self.category = category
        else:
            self.category = random.choice(list(self.WORD_CATEGORIES.keys()))
        
        self.word = random.choice(self.WORD_CATEGORIES[self.category])
        self.guessed_letters = set()
        self.incorrect_guesses = set()
        self.attempts_left = 6
        self.game_over = False
        self.win = False

    def display_word(self) -> str:
        """Display the word with guessed letters revealed."""
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def process_guess(self, guess: str) -> tuple:
        """Process the player's guess and return status with message."""
        guess = guess.lower()
        
        if len(guess) != 1 or not guess.isalpha():
            return False, "Please enter a single letter!"
            
        if guess in self.guessed_letters.union(self.incorrect_guesses):
            return False, "You already guessed that letter!"
            
        if guess in self.word:
            self.guessed_letters.add(guess)
            
            # Check if player has won
            if set(self.word) <= self.guessed_letters:
                self.win = True
                self.game_over = True
                round_score = self.calculate_score()
                self.score += round_score
                self.streak += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                return True, f"🎉 Congratulations! You guessed: {self.word}\nRound score: {round_score}"
                
            return True, f"Good guess! '{guess}' is in the word."
        else:
            self.incorrect_guesses.add(guess)
            self.attempts_left -= 1
            
            if self.attempts_left <= 0:
                self.game_over = True
                self.streak = 0
                return False, f"💀 Game Over! The word was: {self.word}"
                
            return False, f"Sorry, '{guess}' is not in the word."

    def calculate_score(self) -> int:
        """Calculate score based on performance and word difficulty."""
        # Base score depends on word length
        base_score = len(self.word) * 10
        
        # Penalty for incorrect guesses
        penalty = len(self.incorrect_guesses) * 5
        
        # Bonus for more difficult words
        difficulty_bonus = 0
        if len(self.word) >= 8:
            difficulty_bonus = 20
        elif len(self.word) >= 6:
            difficulty_bonus = 10
            
        # Streak bonus
        streak_bonus = min(self.streak * 5, 50)  # Cap at 50
        
        return max(0, base_score - penalty + difficulty_bonus + streak_bonus)

    def get_hint(self) -> str:
        """Provide a hint by revealing one unguessed letter."""
        unguessed = [letter for letter in self.word if letter not in self.guessed_letters]
        if not unguessed:
            return "No hints available - you've guessed all letters!"
            
        hint_letter = random.choice(unguessed)
        self.guessed_letters.add(hint_letter)
        
        # Small penalty for using hint
        self.score = max(0, self.score - 5)
        
        return f"Hint: The letter '{hint_letter}' is in the word!"

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'game' not in st.session_state:
        st.session_state.game = Hangman()
    if 'message' not in st.session_state:
        st.session_state.message = ""
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

def main():
    st.set_page_config(
        page_title="Hangman Game",
        page_icon="🎮",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    game = st.session_state.game
    
    # Title and instructions
    st.title("🎮 Hangman Game")
    st.markdown("""
    ### How to Play
    1. Choose a category and click "Start Game"
    2. Guess letters by typing them in the input box
    3. Try to guess the word before the hangman is complete!
    """)
    
    # Game setup
    if not st.session_state.game_started:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            category = st.selectbox(
                "Select a category:",
                options=list(game.WORD_CATEGORIES.keys())
            )
        
        with col2:
            if st.button("Start Game", key="start_button"):
                game.choose_word(category)
                st.session_state.game_started = True
                st.session_state.message = f"Category: {game.category}. Good luck!"
                st.rerun()
    
    # Game play
    else:
        # Display game state
        st.code(game.HANGMAN_STAGES[len(game.incorrect_guesses)], language=None)
        
        # Game information
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Category:** {game.category}")
            st.markdown(f"**Word:** {game.display_word()}")
        
        with col2:
            st.markdown(f"**Attempts left:** {game.attempts_left}")
            st.markdown(f"**Incorrect guesses:** {', '.join(sorted(game.incorrect_guesses)) or 'None'}")
        
        # Score information
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", game.score)
        with col2:
            st.metric("Streak", game.streak)
        with col3:
            st.metric("High Score", game.high_score)
        
        # Display message
        if st.session_state.message:
            st.info(st.session_state.message)
        
        # Game controls
        if not game.game_over:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                guess = st.text_input("Enter a letter:", max_chars=1, key="guess_input")
                if guess:
                    success, message = game.process_guess(guess)
                    st.session_state.message = message
                    st.rerun()
            
            with col2:
                if st.button("Get Hint"):
                    st.session_state.message = game.get_hint()
                    st.rerun()
        
        # Game over options
        else:
            if game.win:
                st.balloons()
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Play Again"):
                    game.choose_word(game.category)
                    st.session_state.message = f"New game started! Category: {game.category}"
                    st.session_state.game_over = False
                    st.rerun()
            
            with col2:
                if st.button("Change Category"):
                    st.session_state.game_started = False
                    st.rerun()
            
            if st.button("Reset Game"):
                st.session_state.game = Hangman()
                st.session_state.game_started = False
                st.session_state.message = ""
                st.rerun()

if __name__ == "__main__":
    main()