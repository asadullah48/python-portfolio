import streamlit as st
import random
import time
import pandas as pd
from typing import Set
import requests

class Hangman:
    """A complete Hangman game implementation with enhanced features, graphics, and game mechanics."""

    # Colorful hangman stages with better visualization
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

    # Extended word categories with more options
    WORD_CATEGORIES = {
        "Programming": ["python", "javascript", "algorithm", "database", "function", "variable", "inheritance", "framework",
                       "compiler", "debugging", "interface", "recursion", "parameter", "iteration", "encapsulation"],
        "Animals": ["elephant", "giraffe", "kangaroo", "dolphin", "rhinoceros", "penguin", "tiger", "crocodile",
                   "cheetah", "flamingo", "hedgehog", "octopus", "panther", "squirrel", "walrus"],
        "Countries": ["canada", "brazil", "japan", "australia", "germany", "egypt", "sweden", "thailand",
                     "portugal", "argentina", "morocco", "singapore", "finland", "mexico", "norway"],
        "Fruits": ["apple", "banana", "orange", "strawberry", "pineapple", "watermelon", "blueberry",
                  "raspberry", "blackberry", "kiwi", "mango", "papaya", "apricot", "coconut", "peach"],
        "Movies": ["avatar", "titanic", "inception", "interstellar", "gladiator", "matrix",
                  "jaws", "casablanca", "psycho", "alien", "frozen", "godfather", "jurassic", "terminator"],
        "Sports": ["football", "basketball", "tennis", "volleyball", "cricket", "hockey", "badminton",
                  "swimming", "archery", "boxing", "cycling", "fencing", "gymnastics", "wrestling"],
        "Mythology": ["zeus", "apollo", "athena", "poseidon", "hercules", "medusa", "minotaur",
                     "pegasus", "phoenix", "chimera", "cyclops", "griffin", "hydra", "kraken"],
        "Science": ["gravity", "molecule", "electron", "photosynthesis", "evolution", "relativity", "quantum",
                   "nucleus", "chromosome", "ecosystem", "velocity", "momentum", "catalyst", "isotope"]
    }

    # Difficulty levels with different word length ranges
    DIFFICULTY_LEVELS = {
        "Easy": (3, 5),
        "Medium": (6, 8),
        "Hard": (9, 15)
    }

    # Achievements to unlock during gameplay
    ACHIEVEMENTS = {
        "First Win": "Win your first game",
        "Perfect Game": "Win without any incorrect guesses",
        "Quick Thinker": "Win a game in under 30 seconds",
        "Word Master": "Win 5 games in a row",
        "Category Expert": "Win games in 3 different categories",
        "Hard Mode Hero": "Win a game on Hard difficulty",
        "Alphabet Explorer": "Use 20 different letters across all games"
    }

    def __init__(self):
        """Initialize game with enhanced tracking and features."""
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
        self.difficulty = "Medium"  # Default difficulty
        self.start_time = None
        self.end_time = None
        self.game_duration = 0
        self.all_used_letters: Set[str] = set()  # Track all letters used across games
        self.games_won = 0
        self.perfect_games = 0
        self.categories_won: Set[str] = set()  # Track categories won
        self.unlocked_achievements: Set[str] = set()
        self.leaderboard = []  # Store high scores
        self.theme = "light"  # Default theme

    def choose_word(self, category=None, difficulty=None) -> None:
        """Select a random word based on category and difficulty."""
        if category:
            self.category = category
        else:
            self.category = random.choice(list(self.WORD_CATEGORIES.keys()))

        if difficulty:
            self.difficulty = difficulty

        # Filter words by difficulty level
        min_length, max_length = self.DIFFICULTY_LEVELS[self.difficulty]
        filtered_words = [word for word in self.WORD_CATEGORIES[self.category]
                         if min_length <= len(word) <= max_length]

        # If no words match the criteria, use all words in the category
        if not filtered_words:
            filtered_words = self.WORD_CATEGORIES[self.category]

        self.word = random.choice(filtered_words)
        self.guessed_letters = set()
        self.incorrect_guesses = set()
        self.attempts_left = 6
        self.game_over = False
        self.win = False
        self.start_time = time.time()  # Start the timer

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

        # Add to all used letters for achievement tracking
        self.all_used_letters.add(guess)

        if guess in self.word:
            self.guessed_letters.add(guess)

            # Check if player has won
            if set(self.word) <= self.guessed_letters:
                self.win = True
                self.game_over = True
                self.end_time = time.time()
                self.game_duration = self.end_time - self.start_time

                # Update game statistics
                self.games_won += 1
                self.categories_won.add(self.category)
                if not self.incorrect_guesses:
                    self.perfect_games += 1

                # Calculate score and update high score
                round_score = self.calculate_score()
                self.score += round_score
                self.streak += 1
                if self.score > self.high_score:
                    self.high_score = self.score

                # Add to leaderboard
                self.leaderboard.append({
                    "word": self.word,
                    "category": self.category,
                    "difficulty": self.difficulty,
                    "score": round_score,
                    "time": self.game_duration,
                    "perfect": not self.incorrect_guesses
                })

                # Sort leaderboard by score (highest first)
                self.leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)[:10]

                # Check for achievements
                self.check_achievements()

                achievement_msg = ""
                if self.unlocked_achievements:
                    achievement_msg = f"\n🏆 Achievement unlocked: {', '.join(self.unlocked_achievements)}"

                return True, f"🎉 Congratulations! You guessed: {self.word}\nRound score: {round_score}\nTime: {self.game_duration:.1f}s{achievement_msg}"

            return True, f"Good guess! '{guess}' is in the word."
        else:
            self.incorrect_guesses.add(guess)
            self.attempts_left -= 1

            if self.attempts_left <= 0:
                self.game_over = True
                self.streak = 0
                self.end_time = time.time()
                self.game_duration = self.end_time - self.start_time
                return False, f"💀 Game Over! The word was: {self.word}"

            return False, f"Sorry, '{guess}' is not in the word."

    def check_achievements(self) -> None:
        """Check and update achievements based on game performance."""
        newly_unlocked = set()

        # First Win
        if self.games_won == 1 and "First Win" not in self.unlocked_achievements:
            newly_unlocked.add("First Win")

        # Perfect Game
        if not self.incorrect_guesses and "Perfect Game" not in self.unlocked_achievements:
            newly_unlocked.add("Perfect Game")

        # Quick Thinker
        if self.game_duration < 30 and "Quick Thinker" not in self.unlocked_achievements:
            newly_unlocked.add("Quick Thinker")

        # Word Master
        if self.streak >= 5 and "Word Master" not in self.unlocked_achievements:
            newly_unlocked.add("Word Master")

        # Category Expert
        if len(self.categories_won) >= 3 and "Category Expert" not in self.unlocked_achievements:
            newly_unlocked.add("Category Expert")

        # Hard Mode Hero
        if self.difficulty == "Hard" and "Hard Mode Hero" not in self.unlocked_achievements:
            newly_unlocked.add("Hard Mode Hero")

        # Alphabet Explorer
        if len(self.all_used_letters) >= 20 and "Alphabet Explorer" not in self.unlocked_achievements:
            newly_unlocked.add("Alphabet Explorer")

        self.unlocked_achievements.update(newly_unlocked)

    def calculate_score(self) -> int:
        """Calculate score based on performance, word difficulty, and game speed."""
        # Base score depends on word length
        base_score = len(self.word) * 10

        # Penalty for incorrect guesses
        penalty = len(self.incorrect_guesses) * 5

        # Difficulty bonus
        difficulty_bonus = 0
        if self.difficulty == "Easy":
            difficulty_bonus = 0
        elif self.difficulty == "Medium":
            difficulty_bonus = 20
        elif self.difficulty == "Hard":
            difficulty_bonus = 40

        # Streak bonus
        streak_bonus = min(self.streak * 5, 50)  # Cap at 50

        # Speed bonus (faster = more points)
        speed_bonus = 0
        if self.game_duration < 15:
            speed_bonus = 30
        elif self.game_duration < 30:
            speed_bonus = 20
        elif self.game_duration < 60:
            speed_bonus = 10

        # Perfect game bonus
        perfect_bonus = 25 if not self.incorrect_guesses else 0

        return max(0, base_score - penalty + difficulty_bonus + streak_bonus + speed_bonus + perfect_bonus)

    def get_hint(self) -> str:
        """Provide a hint by revealing one unguessed letter."""
        unguessed = [letter for letter in self.word if letter not in self.guessed_letters]
        if not unguessed:
            return "No hints available - you've guessed all letters!"

        hint_letter = random.choice(unguessed)
        self.guessed_letters.add(hint_letter)

        # Penalty for using hint (scales with difficulty)
        if self.difficulty == "Easy":
            penalty = 5
        elif self.difficulty == "Medium":
            penalty = 10
        else:
            penalty = 15

        self.score = max(0, self.score - penalty)

        return f"Hint: The letter '{hint_letter}' is in the word! (-{penalty} points)"

    def get_word_definition(self) -> str:
        """Fetch the definition of the current word using a dictionary API."""
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}")
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    meanings = data[0].get("meanings", [])
                    if meanings and len(meanings) > 0:
                        definition = meanings[0].get("definitions", [{}])[0].get("definition", "")
                        if definition:
                            return f"Definition: {definition}"
            return f"No definition found for '{self.word}'"
        except Exception:
            return f"Could not fetch definition for '{self.word}'"

    def toggle_theme(self) -> None:
        """Toggle between light and dark theme."""
        self.theme = "dark" if self.theme == "light" else "light"

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'game' not in st.session_state:
        st.session_state.game = Hangman()
    if 'message' not in st.session_state:
        st.session_state.message = ""
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'show_leaderboard' not in st.session_state:
        st.session_state.show_leaderboard = False
    if 'show_achievements' not in st.session_state:
        st.session_state.show_achievements = False
    if 'show_definition' not in st.session_state:
        st.session_state.show_definition = False
    if 'keyboard_enabled' not in st.session_state:
        st.session_state.keyboard_enabled = True

def get_background_image():
    """Return a background image for the app."""
    return """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/abstract-blue-geometric-shapes-background_1035-17545.jpg");
        background-size: cover;
    }
    </style>
    """

def get_custom_css(theme="light"):
    """Return custom CSS for styling the app based on theme."""
    if theme == "dark":
        return """
        <style>
        .stApp {
            background-color: #121212;
            color: #FFFFFF;
        }
        .css-18e3th9 {
            padding-top: 2rem;
            padding-bottom: 10rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .css-1d391kg {
            padding-top: 3.5rem;
            padding-right: 1rem;
            padding-bottom: 3.5rem;
            padding-left: 1rem;
        }
        .stButton>button {
            background-color: #BB86FC;
            color: #000000;
            border-radius: 20px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #03DAC6;
            transform: scale(1.05);
        }
        .word-display {
            font-size: 2.5rem;
            font-weight: bold;
            letter-spacing: 0.5rem;
            color: #03DAC6;
        }
        .hangman-container {
            background-color: #1F1B24;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .game-info {
            background-color: #2D2D2D;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .achievement {
            background-color: #3700B3;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #BB86FC;
        }
        </style>
        """
    else:
        return """
        <style>
        .stApp {
            background-color: #F8F9FA;
        }
        .css-18e3th9 {
            padding-top: 2rem;
            padding-bottom: 10rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .css-1d391kg {
            padding-top: 3.5rem;
            padding-right: 1rem;
            padding-bottom: 3.5rem;
            padding-left: 1rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        .word-display {
            font-size: 2.5rem;
            font-weight: bold;
            letter-spacing: 0.5rem;
            color: #1E88E5;
        }
        .hangman-container {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .game-info {
            background-color: #E3F2FD;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .achievement {
            background-color: #FFF8E1;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #FFC107;
        }
        </style>
        """

def create_virtual_keyboard():
    """Create a virtual keyboard for letter input."""
    keyboard_rows = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    ]

    for row in keyboard_rows:
        cols = st.columns(len(row))
        for i, letter in enumerate(cols):
            if i < len(row):
                with letter:
                    if st.button(row[i], key=f"key_{row[i]}"):
                        return row[i].lower()
    return None

def main():
    st.set_page_config(
        page_title="Hangman Game",
        page_icon="🎮",
        layout="wide"
    )

    # Initialize session state
    initialize_session_state()
    game = st.session_state.game

    # Apply custom styling
    st.markdown(get_background_image(), unsafe_allow_html=True)
    st.markdown(get_custom_css(game.theme), unsafe_allow_html=True)

    # App header with logo and theme toggle
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2534/2534183.png", width=100)
    with col2:
        st.title("🎮 Hangman Challenge")
        st.markdown("<p style='font-size: 1.2rem; font-style: italic;'>Test your vocabulary and word-guessing skills!</p>", unsafe_allow_html=True)
    with col3:
        if st.button("🌓 Toggle Theme"):
            game.toggle_theme()
            st.rerun()

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Play Game", "Leaderboard", "Achievements", "How to Play"])

    with tab1:  # Main game tab
        if not st.session_state.game_started:
            # Game setup with enhanced UI
            st.markdown("<div class='game-info'>", unsafe_allow_html=True)
            st.subheader("Game Setup")

            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox(
                    "Select a category:",
                    options=list(game.WORD_CATEGORIES.keys())
                )

                difficulty = st.select_slider(
                    "Select difficulty:",
                    options=list(game.DIFFICULTY_LEVELS.keys()),
                    value="Medium"
                )

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                **Game Features:**
                - 8 word categories with 15+ words each
                - 3 difficulty levels
                - Score system with bonuses
                - Achievements to unlock
                - Word definitions
                - Customizable theme
                """)

            st.markdown("</div>", unsafe_allow_html=True)

            # Start game button
            if st.button("🚀 Start Game", key="start_button", use_container_width=True):
                game.choose_word(category, difficulty)
                st.session_state.game_started = True
                st.session_state.message = f"Category: {game.category} | Difficulty: {game.difficulty} | Good luck!"
                st.rerun()

        # Game play
        else:
            # Game container with enhanced styling
            st.markdown("<div class='hangman-container'>", unsafe_allow_html=True)

            # Game header with stats
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.subheader(f"Category: {game.category} | Difficulty: {game.difficulty}")
            with col2:
                st.metric("Attempts Left", game.attempts_left, delta=None)
            with col3:
                # Display timer if game is in progress
                if not game.game_over and game.start_time:
                    elapsed = time.time() - game.start_time
                    st.metric("Time", f"{elapsed:.1f}s", delta=None)
                elif game.game_over and game.end_time:
                    st.metric("Final Time", f"{game.game_duration:.1f}s", delta=None)

            # Display hangman visualization
            col1, col2 = st.columns([1, 2])
            with col1:
                # Enhanced hangman display with color
                stage_index = len(game.incorrect_guesses)
                hangman_colors = ["#4CAF50", "#8BC34A", "#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#F44336"]
                color = hangman_colors[stage_index] if stage_index < len(hangman_colors) else hangman_colors[-1]

                st.markdown(f"<pre style='color:{color}; font-size:1.2rem;'>{game.HANGMAN_STAGES[stage_index]}</pre>", unsafe_allow_html=True)

                # Display incorrect guesses
                st.markdown("### Incorrect Guesses")
                incorrect = ', '.join(sorted(game.incorrect_guesses)) or 'None'
                st.markdown(f"<p style='color:{color};'>{incorrect}</p>", unsafe_allow_html=True)

            with col2:
                # Word display with enhanced styling
                st.markdown("### Current Word")
                st.markdown(f"<p class='word-display'>{game.display_word()}</p>", unsafe_allow_html=True)

                # Score information
                score_cols = st.columns(3)
                with score_cols[0]:
                    st.metric("Score", game.score)
                with score_cols[1]:
                    st.metric("Streak", game.streak)
                with score_cols[2]:
                    st.metric("High Score", game.high_score)

            # Display message
            if st.session_state.message:
                message_type = "success" if "Congratulations" in st.session_state.message else "info"
                if "Game Over" in st.session_state.message:
                    message_type = "error"
                getattr(st, message_type)(st.session_state.message)

            st.markdown("</div>", unsafe_allow_html=True)

            # Game controls
            if not game.game_over:
                st.markdown("<div class='game-info'>", unsafe_allow_html=True)
                st.subheader("Make Your Guess")

                # Letter input options
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    guess = st.text_input("Enter a letter:", max_chars=1, key="guess_input")
                    if guess:
                        _, message = game.process_guess(guess)
                        st.session_state.message = message
                        st.rerun()

                with col2:
                    if st.button("💡 Get Hint", use_container_width=True):
                        st.session_state.message = game.get_hint()
                        st.rerun()

                with col3:
                    keyboard_toggle = st.toggle("Virtual Keyboard", value=st.session_state.keyboard_enabled)
                    if keyboard_toggle != st.session_state.keyboard_enabled:
                        st.session_state.keyboard_enabled = keyboard_toggle
                        st.rerun()

                # Virtual keyboard
                if st.session_state.keyboard_enabled:
                    st.markdown("### Virtual Keyboard")
                    key_press = create_virtual_keyboard()
                    if key_press:
                        _, message = game.process_guess(key_press)
                        st.session_state.message = message
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

            # Game over options
            else:
                if game.win:
                    st.balloons()

                    # Show word definition
                    if not st.session_state.show_definition:
                        if st.button("📚 Show Word Definition"):
                            st.session_state.show_definition = True
                            st.rerun()
                    else:
                        definition = game.get_word_definition()
                        st.info(definition)

                st.markdown("<div class='game-info'>", unsafe_allow_html=True)
                st.subheader("Game Options")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🔄 Play Again", use_container_width=True):
                        game.choose_word(game.category, game.difficulty)
                        st.session_state.message = f"New game started! Category: {game.category}"
                        st.session_state.show_definition = False
                        st.session_state.game_over = False
                        st.rerun()

                with col2:
                    if st.button("🔀 Change Category", use_container_width=True):
                        st.session_state.game_started = False
                        st.session_state.show_definition = False
                        st.rerun()

                with col3:
                    if st.button("🔁 Reset Game", use_container_width=True):
                        st.session_state.game = Hangman()
                        st.session_state.game_started = False
                        st.session_state.message = ""
                        st.session_state.show_definition = False
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    with tab2:  # Leaderboard tab
        st.subheader("🏆 Leaderboard")

        if game.leaderboard:
            # Create a DataFrame for the leaderboard
            leaderboard_data = pd.DataFrame(game.leaderboard)

            # Format the time column
            leaderboard_data["time"] = leaderboard_data["time"].apply(lambda x: f"{x:.1f}s")

            # Add rank column
            leaderboard_data.insert(0, "Rank", range(1, len(leaderboard_data) + 1))

            # Rename columns for display
            leaderboard_data.columns = ["Rank", "Word", "Category", "Difficulty", "Score", "Time", "Perfect Game"]

            # Display the leaderboard
            st.dataframe(leaderboard_data, use_container_width=True, hide_index=True)
        else:
            st.info("No games completed yet. Play a game to see your scores here!")

    with tab3:  # Achievements tab
        st.subheader("🏅 Achievements")

        # Display all achievements with locked/unlocked status
        for achievement, description in game.ACHIEVEMENTS.items():
            col1, col2 = st.columns([1, 4])

            with col1:
                if achievement in game.unlocked_achievements:
                    st.markdown("🔓 **UNLOCKED**")
                else:
                    st.markdown("🔒 *LOCKED*")

            with col2:
                st.markdown(f"**{achievement}**: {description}")

            st.markdown("---")

        # Display achievement stats
        st.subheader("Stats")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Games Won", game.games_won)
        with col2:
            st.metric("Perfect Games", game.perfect_games)
        with col3:
            st.metric("Categories Played", len(game.categories_won))

    with tab4:  # How to play tab
        st.subheader("📋 How to Play Hangman")

        st.markdown("""
        ### Game Rules
        1. The computer selects a random word based on your chosen category and difficulty.
        2. Your goal is to guess the word one letter at a time.
        3. Each incorrect guess adds a part to the hangman figure.
        4. You win if you guess the word before the hangman is complete (6 incorrect guesses).

        ### Scoring System
        - Base score depends on word length
        - Bonus points for harder difficulty levels
        - Speed bonus for quick solves
        - Streak bonus for consecutive wins
        - Perfect game bonus (no incorrect guesses)
        - Penalty for using hints

        ### Difficulty Levels
        - **Easy**: Words with 3-5 letters
        - **Medium**: Words with 6-8 letters
        - **Hard**: Words with 9+ letters

        ### Tips
        - Start with common vowels (a, e, i, o, u)
        - Look for common consonants like t, n, s, r
        - Use the hint feature strategically
        - Pay attention to word patterns
        """)

        # Credits
        st.markdown("---")
        st.markdown("### Credits")
        st.markdown("Developed with ❤️ using Python and Streamlit")
        st.markdown("Icons by [Flaticon](https://www.flaticon.com)")
        st.markdown("Background by [Freepik](https://www.freepik.com)")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>© 2025 Hangman Challenge | v2.0</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()