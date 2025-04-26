import streamlit as st
import random
import pandas as pd
import altair as alt
from typing import Tuple, Optional
import time
import datetime

class SmartComputerGuesser:
    """A smarter computer guesser using binary search algorithm."""
    
    def __init__(self, min_num: int = 1, max_num: int = 100):
        """Initialize the guesser with number range."""
        self.min_num = min_num
        self.max_num = max_num
        self.reset()
    
    def reset(self):
        """Reset the guesser state."""
        self.current_min = self.min_num
        self.current_max = self.max_num
        self.attempts = 0
        self.guess_history = []
        
    def make_guess(self) -> int:
        """Make a guess using binary search."""
        # Binary search algorithm - take the middle of the current range
        guess = (self.current_min + self.current_max) // 2
        self.attempts += 1
        return guess
    
    def process_feedback(self, guess: int, feedback: str) -> bool:
        """
        Process user feedback and adjust search range.
        
        Returns:
            bool: True if game should continue, False if inconsistent feedback
        """
        if feedback == "higher":
            self.current_min = guess + 1
            self.guess_history.append((guess, "Too low"))
        elif feedback == "lower":
            self.current_max = guess - 1
            self.guess_history.append((guess, "Too high"))
            
        # Check for contradictory feedback
        if self.current_min > self.current_max:
            return False
        return True
    
    def get_optimal_guess_count(self) -> int:
        """Calculate the optimal number of guesses needed for current range."""
        return max(1, int(st.session_state.get('optimal_guesses', 0)))

def calculate_optimal_guesses(min_num: int, max_num: int) -> int:
    """Calculate optimal number of guesses using log2 formula."""
    import math
    return math.ceil(math.log2(max_num - min_num + 1))

def animate_success():
    """Display a success animation."""
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)
    progress_bar.empty()

def create_number_guessing_app():
    # Set page config
    st.set_page_config(
        page_title="Mind Reader: Computer Guesses Your Number",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS for better UI
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            border-radius: 20px;
            height: 3em;
            font-weight: bold;
        }
        h1, h2, h3 {
            color: #1E3A8A;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for persistent data
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
        st.session_state.guesser = SmartComputerGuesser()
        st.session_state.games_played = 0
        st.session_state.games_won = 0
        st.session_state.best_score = float('inf')
        st.session_state.best_time = float('inf')
        st.session_state.current_guess = None
        st.session_state.message = ""
        st.session_state.difficulty = "normal"
        st.session_state.start_time = None
        st.session_state.high_scores = []
        st.session_state.unlocked_levels = ["easy", "normal"]
        st.session_state.achievements = []
        st.session_state.player_name = "Player"
    
    # App UI
    col_title, col_emoji = st.columns([5, 1])
    with col_title:
        st.title("🧠 Mind Reader: Computer Guesses Your Number")
    with col_emoji:
        st.markdown("<h1 style='font-size:50px;'>🔮</h1>", unsafe_allow_html=True)
    
    st.markdown("### Let the computer read your mind and guess your secret number!")
    
    # Sidebar for statistics and settings
    with st.sidebar:
        # Player profile section
        st.header("👤 Player Profile")
        player_name = st.text_input("Your Name:", value=st.session_state.player_name)
        if player_name != st.session_state.player_name:
            st.session_state.player_name = player_name

        st.header("📊 Game Statistics")
        st.metric("Games Played", st.session_state.games_played)
        st.metric("Games Won", st.session_state.games_won)
        
        if st.session_state.games_played > 0:
            win_rate = (st.session_state.games_won / st.session_state.games_played) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
            
        if st.session_state.best_score != float('inf'):
            st.metric("Best Score (Attempts)", st.session_state.best_score)
            
        if st.session_state.best_time != float('inf'):
            st.metric("Best Time", f"{st.session_state.best_time:.2f}s")
        
        st.divider()
        st.header("🏆 Achievements")
        if st.session_state.achievements:
            for achievement in st.session_state.achievements:
                st.success(achievement)
        else:
            st.info("Complete games to earn achievements!")
            
        st.divider()
        st.header("⚙️ Settings")
        
        # Only show unlocked difficulty levels
        difficulty_options = st.session_state.unlocked_levels
        if "custom" not in difficulty_options:
            difficulty_options.append("custom")
            
        difficulty = st.radio(
            "Difficulty Level:",
            options=difficulty_options,
            index=difficulty_options.index(st.session_state.difficulty),
            key="difficulty_setting"
        )
        
        if difficulty == "custom":
            col1, col2 = st.columns(2)
            with col1:
                min_num = st.number_input("Min Number", value=1, min_value=0)
            with col2:
                max_num = st.number_input("Max Number", value=100, min_value=min_num + 10)
        else:
            if difficulty == "easy":
                min_num, max_num = 1, 50
            elif difficulty == "normal":
                min_num, max_num = 1, 100
            elif difficulty == "hard":
                min_num, max_num = 1, 500
            elif difficulty == "extreme":
                min_num, max_num = 1, 1000
        
        # Calculate optimal guesses for the current range
        optimal_guesses = calculate_optimal_guesses(min_num, max_num)
        st.session_state.optimal_guesses = optimal_guesses
        
        st.info(f"Optimal guess count: {optimal_guesses}")
        
        if difficulty != st.session_state.difficulty:
            st.session_state.difficulty = difficulty
            # Reset guesser with new range when difficulty changes
            st.session_state.guesser = SmartComputerGuesser(min_num, max_num)
    
    # Main game area
    if not st.session_state.game_active:
        st.write(f"#### 🤔 Think of a number between {min_num} and {max_num}")
        st.write("I'll try to guess it with your feedback! Just tell me if my guess is too high, too low, or correct.")
        
        # How to play instructions
        with st.expander("📖 How to Play"):
            st.markdown("""
                1. Think of a secret number within the specified range.
                2. The computer will make a guess.
                3. Tell the computer if its guess is:
                   - Too low (click "Higher")
                   - Too high (click "Lower")
                   - Correct (click "Correct!")
                4. Keep providing feedback until the computer guesses correctly.
                5. Try to beat the optimal number of guesses!
            """)
        
        # Leaderboard display
        if st.session_state.high_scores:
            with st.expander("🏆 Leaderboard"):
                leaderboard_df = pd.DataFrame(st.session_state.high_scores, 
                                           columns=["Player", "Difficulty", "Attempts", "Time (s)", "Date"])
                st.table(leaderboard_df.sort_values(by=["Difficulty", "Attempts", "Time (s)"]))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Start New Game", use_container_width=True, key="start_button"):
                st.session_state.game_active = True
                st.session_state.guesser.reset()
                st.session_state.guesser.min_num = min_num
                st.session_state.guesser.max_num = max_num
                st.session_state.guesser.current_min = min_num
                st.session_state.guesser.current_max = max_num
                st.session_state.current_guess = st.session_state.guesser.make_guess()
                st.session_state.message = ""
                st.session_state.start_time = time.time()
                st.rerun()
                
        with col2:
            if st.button("❓ Get a Hint", use_container_width=True):
                hint_options = [
                    "The computer uses binary search to find your number efficiently.",
                    f"With the current range, it should take no more than {optimal_guesses} guesses to find any number.",
                    "Always provide honest feedback for the computer's guesses.",
                    "The more you play, the more difficulty levels you'll unlock!",
                    "Try to challenge yourself with higher difficulty levels."
                ]
                st.info(f"💡 **Hint:** {random.choice(hint_options)}")
    else:
        # Game is active
        # Calculate time elapsed
        elapsed_time = time.time() - st.session_state.start_time
        
        col_guess, col_time = st.columns([4, 1])
        with col_guess:
            st.subheader(f"🤖 Is your number {st.session_state.current_guess}?")
        with col_time:
            st.metric("Time", f"{elapsed_time:.1f}s")
            
        # Progress toward optimal solution
        optimal = st.session_state.optimal_guesses
        current = st.session_state.guesser.attempts
        
        progress_text = f"Attempt {current} of {optimal} (optimal)"
        progress_value = min(1.0, current / optimal)
        
        st.progress(progress_value, text=progress_text)
        
        # Display guess history if any
        if st.session_state.guesser.guess_history:
            with st.expander("📜 Guess History", expanded=True):
                # Create a dataframe for the history
                history_df = pd.DataFrame(
                    st.session_state.guesser.guess_history,
                    columns=["Guess", "Result"]
                )
                history_df.index = history_df.index + 1  # 1-based indexing
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Display history as a table
                    st.dataframe(history_df, use_container_width=True)
                
                with col2:
                    # Create a line chart for visualization
                    history_df['Attempt'] = history_df.index
                    
                    chart = alt.Chart(history_df).mark_line(point=True).encode(
                        x=alt.X('Attempt:Q', title='Attempt Number'),
                        y=alt.Y('Guess:Q', title='Guess Value', scale=alt.Scale(domain=[min_num, max_num])),
                        tooltip=['Attempt', 'Guess', 'Result'],
                        color=alt.value("#1E88E5")
                    ).properties(
                        height=250
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
        
        # Display current range
        st.info(f"🔍 Current search range: {st.session_state.guesser.current_min} to {st.session_state.guesser.current_max}")
        
        # Show any message
        if st.session_state.message:
            st.warning(st.session_state.message)
        
        # User feedback buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👆 Higher", use_container_width=True, help="Click if your number is higher than my guess"):
                continue_game = st.session_state.guesser.process_feedback(
                    st.session_state.current_guess, "higher"
                )
                
                if continue_game:
                    st.session_state.current_guess = st.session_state.guesser.make_guess()
                else:
                    st.session_state.message = "🤨 I detect inconsistent feedback. Let's restart."
                    st.session_state.game_active = False
                st.rerun()
        
        with col2:
            if st.button("👇 Lower", use_container_width=True, help="Click if your number is lower than my guess"):
                continue_game = st.session_state.guesser.process_feedback(
                    st.session_state.current_guess, "lower"
                )
                
                if continue_game:
                    st.session_state.current_guess = st.session_state.guesser.make_guess()
                else:
                    st.session_state.message = "🤨 I detect inconsistent feedback. Let's restart."
                    st.session_state.game_active = False
                st.rerun()
        
        with col3:
            if st.button("✅ Correct!", use_container_width=True, help="Click if I guessed correctly"):
                attempts = st.session_state.guesser.attempts
                elapsed = time.time() - st.session_state.start_time
                
                st.session_state.games_played += 1
                st.session_state.games_won += 1
                
                # Check for new achievements
                if "hard" not in st.session_state.unlocked_levels and st.session_state.games_won >= 3:
                    st.session_state.unlocked_levels.append("hard")
                    st.session_state.achievements.append("🔓 Unlocked Hard difficulty!")
                
                if "extreme" not in st.session_state.unlocked_levels and st.session_state.games_won >= 5:
                    st.session_state.unlocked_levels.append("extreme")
                    st.session_state.achievements.append("🔓 Unlocked Extreme difficulty!")
                
                if attempts <= optimal_guesses and "Optimal Solver" not in st.session_state.achievements:
                    st.session_state.achievements.append("🏅 Optimal Solver: Computer guessed in optimal steps!")
                    
                # Update high scores
                st.session_state.high_scores.append([
                    st.session_state.player_name,
                    st.session_state.difficulty,
                    attempts,
                    round(elapsed, 2),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                ])
                
                # Update best scores
                if attempts < st.session_state.best_score:
                    st.session_state.best_score = attempts
                    message_prefix = f"🎉 I guessed your number in {attempts} attempts! That's a new best score! 🏆"
                else:
                    message_prefix = f"🎉 I guessed your number in {attempts} attempts!"
                
                if elapsed < st.session_state.best_time:
                    st.session_state.best_time = elapsed
                    message_prefix += f" New best time: {elapsed:.2f}s! ⏱️"
                
                st.session_state.message = message_prefix
                st.session_state.game_active = False
                
                # Animate success
                animate_success()
                st.balloons()
                st.rerun()
        
        # End current game
        if st.button("🛑 End Game", use_container_width=True):
            st.session_state.game_active = False
            st.session_state.games_played += 1
            st.session_state.message = "Game ended. Thanks for playing!"
            st.rerun()

if __name__ == "__main__":
    create_number_guessing_app()