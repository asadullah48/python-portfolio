import random
import os
import time
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

    # Enhanced word categories
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
        self.streak = 0
        self.high_score = 0
        self.difficulty_level = "medium"  # default difficulty

    def _clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _choose_word(self) -> None:
        """Select a random word and category."""
        # Allow user to choose category
        print("\nAvailable categories:")
        for i, category in enumerate(self.WORD_CATEGORIES.keys(), 1):
            print(f"{i}. {category}")
        
        try:
            choice = input("\nSelect a category (number) or press Enter for random: ").strip()
            if choice and choice.isdigit():
                index = int(choice) - 1
                categories = list(self.WORD_CATEGORIES.keys())
                if 0 <= index < len(categories):
                    self.category = categories[index]
                else:
                    print("Invalid selection. Choosing random category.")
                    time.sleep(1)
                    self.category = random.choice(list(self.WORD_CATEGORIES.keys()))
            else:
                self.category = random.choice(list(self.WORD_CATEGORIES.keys()))
                
            # Select word based on difficulty
            words = self.WORD_CATEGORIES[self.category]
            if self.difficulty_level == "easy":
                # Choose shorter words
                candidates = [w for w in words if len(w) <= 6]
            elif self.difficulty_level == "hard":
                # Choose longer words
                candidates = [w for w in words if len(w) >= 7]
            else:  # medium
                candidates = words
                
            # If no words match difficulty criteria, use all words
            if not candidates:
                candidates = words
                
            self.word = random.choice(candidates)
            
        except Exception as e:
            print(f"Error selecting word: {e}. Using random selection.")
            time.sleep(1)
            self.category = random.choice(list(self.WORD_CATEGORIES.keys()))
            self.word = random.choice(self.WORD_CATEGORIES[self.category])
            
        self.guessed_letters = set()
        self.incorrect_guesses = set()
        self.attempts_left = 6

    def _display_word(self) -> str:
        """Display the word with guessed letters revealed."""
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def _display_game_state(self) -> None:
        """Show current game status with ASCII art."""
        self._clear_screen()
        print("\n" + "=" * 50)
        print(" HANGMAN GAME ".center(50, "🎮"))
        print("=" * 50)
        
        print(self.HANGMAN_STAGES[len(self.incorrect_guesses)])
        print(f"\nCategory: {self.category}")
        print(f"Word: {self._display_word()}")
        print(f"\nAttempts left: {self.attempts_left}")
        print(f"Incorrect guesses: {', '.join(sorted(self.incorrect_guesses)) or 'None'}")
        print(f"Score: {self.score} | Streak: {self.streak} | High Score: {self.high_score}")
        print(f"Difficulty: {self.difficulty_level.capitalize()}")

    def _process_guess(self, guess: str) -> bool:
        """Process the player's guess and return if correct."""
        guess = guess.lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter!")
            time.sleep(1)
            return False
            
        if guess in self.guessed_letters.union(self.incorrect_guesses):
            print("You already guessed that letter!")
            time.sleep(1)
            return False
            
        if guess in self.word:
            self.guessed_letters.add(guess)
            print(f"Good guess! '{guess}' is in the word.")
            return True
        else:
            self.incorrect_guesses.add(guess)
            self.attempts_left -= 1
            print(f"Sorry, '{guess}' is not in the word.")
            return False

    def _calculate_score(self) -> int:
        """Calculate score based on performance."""
        # Base score depends on word length
        base_score = len(self.word) * 10
        
        # Penalty for incorrect guesses
        penalty = len(self.incorrect_guesses) * 5
        
        # Bonus for difficulty
        difficulty_bonus = {
            "easy": 0,
            "medium": 10,
            "hard": 20
        }.get(self.difficulty_level, 0)
            
        # Streak bonus
        streak_bonus = min(self.streak * 5, 50)  # Cap at 50
        
        return max(0, base_score - penalty + difficulty_bonus + streak_bonus)

    def _get_hint(self) -> None:
        """Provide a hint by revealing one unguessed letter."""
        unguessed = [letter for letter in self.word if letter not in self.guessed_letters]
        if not unguessed:
            print("No hints available - you've guessed all the correct letters!")
            return
            
        hint_letter = random.choice(unguessed)
        self.guessed_letters.add(hint_letter)
        
        # Small penalty for using hint
        self.score = max(0, self.score - 5)
        
        print(f"Hint: The letter '{hint_letter}' is in the word!")
        print("(5 points deducted for using a hint)")
        time.sleep(2)

    def _set_difficulty(self) -> None:
        """Set the game difficulty level."""
        print("\nDifficulty Levels:")
        print("1. Easy   - Shorter words")
        print("2. Medium - Mixed length words (default)")
        print("3. Hard   - Longer words")
        
        choice = input("\nSelect difficulty (1-3): ").strip()
        
        if choice == "1":
            self.difficulty_level = "easy"
        elif choice == "3":
            self.difficulty_level = "hard"
        else:
            self.difficulty_level = "medium"
            
        print(f"Difficulty set to {self.difficulty_level.capitalize()}")
        time.sleep(1)

    def _play_round(self) -> bool:
        """Play one round of Hangman."""
        self._choose_word()
        
        while self.attempts_left > 0:
            self._display_game_state()
            
            print("\nOptions:")
            print("1. Guess a letter")
            print("2. Get a hint")
            print("3. Quit game")
            
            choice = input("\nSelect an option (1-3): ").strip()
            
            if choice == "3":
                return False
            elif choice == "2":
                self._get_hint()
                continue
            else:
                guess = input("Enter your letter guess: ").strip().lower()
                
                if guess == 'quit':
                    return False
                    
                self._process_guess(guess)
                
                if set(self.word) <= self.guessed_letters:
                    round_score = self._calculate_score()
                    self.score += round_score
                    self.streak += 1
                    
                    if self.score > self.high_score:
                        self.high_score = self.score
                        
                    self._display_game_state()
                    print(f"\n🎉 Congratulations! You guessed: {self.word}")
                    print(f"Round score: {round_score}")
                    input("\nPress Enter to continue...")
                    return True
                    
                time.sleep(0.5)
        
        self._display_game_state()
        print(f"\n💀 Game Over! The word was: {self.word}")
        self.streak = 0  # Reset streak on loss
        input("\nPress Enter to continue...")
        return True  # Continue to menu even after loss

    def _show_welcome(self) -> None:
        """Display welcome message and instructions."""
        self._clear_screen()
        print("\n" + "=" * 50)
        print(" HANGMAN GAME ".center(50, "🎮"))
        print("=" * 50)
        print("\nGuess the word letter by letter before the hangman is complete!")
        print("Each incorrect guess brings you closer to losing.")
        print("Build up your streak to earn bonus points!")
        print("\nInstructions:")
        print("- You can choose word categories")
        print("- Adjust difficulty for more challenge")
        print("- Use hints if you're stuck (costs 5 points)")
        print("- Try to maintain your streak for bonus points!")
        input("\nPress Enter to continue...")

    def run(self) -> None:
        """Run the game with multiple rounds and menu system."""
        self._show_welcome()
        
        while True:
            self._clear_screen()
            print("\n" + "=" * 50)
            print(" HANGMAN GAME - MAIN MENU ".center(50, "🎮"))
            print("=" * 50)
            print(f"\nCurrent Score: {self.score} | High Score: {self.high_score}")
            print(f"Current Difficulty: {self.difficulty_level.capitalize()}")
            print("\nOptions:")
            print("1. Play Game")
            print("2. Set Difficulty")
            print("3. View Instructions")
            print("4. Exit Game")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                if not self._play_round():
                    break
            elif choice == "2":
                self._set_difficulty()
            elif choice == "3":
                self._show_welcome()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                
        print(f"\n🏆 Final score: {self.score}")
        print("Thanks for playing! Goodbye!")

if __name__ == "__main__":
    try:
        game = Hangman()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")