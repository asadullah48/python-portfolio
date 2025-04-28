
import random
import streamlit as st
from enum import Enum
from typing import Tuple, Dict
import sqlite3
from datetime import datetime

# Database connection helper
def get_db():
    return sqlite3.connect('game.db')

# Set page config immediately at the top of the script
# before any other Streamlit commands
st.set_page_config(
    page_title="Rock Paper Scissors Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded",
)

class Difficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    
    def __str__(self):
        return self.value

class Choice(Enum):
    """Enumeration of possible game choices."""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    
    def __str__(self):
        return self.name.title()
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to Choice enum value"""
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"'{value}' is not a valid Choice")

class GameResult(Enum):
    """Possible game outcomes."""
    WIN = "WIN"
    LOSE = "LOSE"
    DRAW = "DRAW"
    
    def __str__(self):
        return self.value

class RockPaperScissors:
    """A complete Rock-Paper-Scissors game implementation for Streamlit."""
    
    WIN_CONDITIONS = {
        (Choice.ROCK, Choice.SCISSORS): GameResult.WIN,
        (Choice.PAPER, Choice.ROCK): GameResult.WIN,
        (Choice.SCISSORS, Choice.PAPER): GameResult.WIN,
    }
    
    EMOJIS = {
        Choice.ROCK: "🪨",
        Choice.PAPER: "📄",
        Choice.SCISSORS: "✂️"
    }
    
    def __init__(self):
        """Initialize game with score tracking."""
        # Initialize session state if needed
        if 'scores' not in st.session_state:
            st.session_state.scores = {"player": 0, "computer": 0, "ties": 0}
        if 'round' not in st.session_state:
            st.session_state.round = 0
        if 'game_history' not in st.session_state:
            st.session_state.game_history = []
        if 'last_result' not in st.session_state:
            st.session_state.last_result = None
        if 'current_streak' not in st.session_state:
            st.session_state.current_streak = 0
        if 'difficulty' not in st.session_state:
            st.session_state.difficulty = Difficulty.NORMAL
            
    @property
    def scores(self):
        """Access scores from session state"""
        return st.session_state.scores

    @property
    def round(self):
        """Access current round from session state"""
        return st.session_state.round

    def _get_computer_choice(self, user_choice: Choice) -> Choice:
        """Enhanced computer choice based on difficulty level"""
        if st.session_state.difficulty == Difficulty.EASY:
            # 40% chance to let player win
            if random.random() < 0.4:
                losing_choices = [c for c, r in self.WIN_CONDITIONS.items() 
                                if r == GameResult.WIN and c[0] == user_choice]
                if losing_choices:
                    return losing_choices[0][1]
                    
        elif st.session_state.difficulty == Difficulty.HARD:
            # 40% chance to make winning choice
            if random.random() < 0.4:
                winning_choices = [c[1] for c, r in self.WIN_CONDITIONS.items() 
                                 if r == GameResult.WIN and c[0] == user_choice]
                if winning_choices:
                    return winning_choices[0]
                    
        return random.choice(list(Choice))

    def _check_achievements(self):
        """Check and award achievements"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Check win-based achievements
            total_wins = st.session_state.scores["player"]
            cursor.execute("""
                SELECT id, name, condition_value, icon 
                FROM achievements 
                WHERE condition_type = 'wins' 
                AND condition_value <= ? 
                AND id NOT IN (SELECT achievement_id FROM player_achievements)
            """, (total_wins,))
            
            new_achievements = cursor.fetchall()
            for achievement in new_achievements:
                cursor.execute(
                    "INSERT INTO player_achievements (achievement_id) VALUES (?)",
                    (achievement[0],)
                )
                st.balloons()
                st.success(f"🏆 Achievement Unlocked: {achievement[1]} {achievement[3]}")
            
            # Check streak achievements
            if st.session_state.current_streak > 0:
                cursor.execute("""
                    SELECT id, name, condition_value, icon 
                    FROM achievements 
                    WHERE condition_type = 'streak' 
                    AND condition_value <= ? 
                    AND id NOT IN (SELECT achievement_id FROM player_achievements)
                """, (st.session_state.current_streak,))
                
                streak_achievements = cursor.fetchall()
                for achievement in streak_achievements:
                    cursor.execute(
                        "INSERT INTO player_achievements (achievement_id) VALUES (?)",
                        (achievement[0],)
                    )
                    st.balloons()
                    st.success(f"🏆 Achievement Unlocked: {achievement[1]} {achievement[3]}")
            
            conn.commit()

    def _determine_winner(self, user: Choice, computer: Choice) -> GameResult:
        """Determine the game outcome based on choices."""
        if user == computer:
            return GameResult.DRAW
        return self.WIN_CONDITIONS.get((user, computer), GameResult.LOSE)

    def play_round(self, user_choice: Choice) -> GameResult:
        """Play one round of the game with the given user choice."""
        st.session_state.round += 1
        
        computer_choice = self._get_computer_choice(user_choice)
        result = self._determine_winner(user_choice, computer_choice)
        
        # Update scores and streak
        if result == GameResult.WIN:
            st.session_state.scores["player"] += 1
            st.session_state.current_streak += 1
        elif result == GameResult.LOSE:
            st.session_state.scores["computer"] += 1
            st.session_state.current_streak = 0
        else:
            st.session_state.scores["ties"] += 1
            
        # Store round in database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO game_history 
                (player_choice, computer_choice, result, difficulty) 
                VALUES (?, ?, ?, ?)
            """, (
                user_choice.name,  # Store enum name instead of str(enum)
                computer_choice.name,
                str(result),
                st.session_state.difficulty.value
            ))
            conn.commit()
            
        # Check achievements
        self._check_achievements()
        
        # Store round results in session
        round_result = {
            "round": st.session_state.round,
            "user_choice": user_choice,  # Store actual enum value
            "computer_choice": computer_choice,
            "result": result
        }
        st.session_state.game_history.append(round_result)
        st.session_state.last_result = round_result
        
        return result
        
    def reset_game(self):
        """Reset the game state."""
        st.session_state.scores = {"player": 0, "computer": 0, "ties": 0}
        st.session_state.round = 0
        st.session_state.game_history = []
        st.session_state.last_result = None
        st.session_state.current_streak = 0
        

def init_db():
    """Initialize the database with required tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create game_history table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_choice TEXT NOT NULL,
            computer_choice TEXT NOT NULL,
            result TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create achievements table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            condition_type TEXT NOT NULL,
            condition_value INTEGER NOT NULL
        )
        """)
        
        # Create player_achievements table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            achievement_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (achievement_id) REFERENCES achievements (id)
        )
        """)
        
        # Insert default achievements if they don't exist
        cursor.execute("SELECT COUNT(*) FROM achievements")
        if cursor.fetchone()[0] == 0:
            achievements = [
                ("First Victory", "Win your first game", "🏆", "wins", 1),
                ("Getting Started", "Win 5 games", "🌟", "wins", 5),
                ("Experienced Player", "Win 10 games", "🎮", "wins", 10),
                ("Master Player", "Win 25 games", "👑", "wins", 25),
                ("Winning Streak", "Win 3 games in a row", "🔥", "streak", 3),
                ("Hot Streak", "Win 5 games in a row", "🌋", "streak", 5),
                ("Unstoppable", "Win 10 games in a row", "⚡", "streak", 10),
            ]
            cursor.executemany("""
                INSERT INTO achievements (name, description, icon, condition_type, condition_value)
                VALUES (?, ?, ?, ?, ?)
            """, achievements)
            
        conn.commit()

def main():
    # Initialize database
    init_db()
    
    # Initialize game
    game = RockPaperScissors()
    
    # App header
    st.title("🎮 Rock Paper Scissors")
    st.markdown("### Play the classic game against the computer!")
    
    # Difficulty selector
    difficulty = st.selectbox(
        "Select Difficulty",
        [d.value for d in Difficulty],
        index=1
    )
    st.session_state.difficulty = Difficulty(difficulty)
    
    # Game rules in sidebar
    with st.sidebar:
        st.header("Game Rules")
        st.markdown("""
        - 🪨 Rock beats ✂️ Scissors
        - 📄 Paper beats 🪨 Rock
        - ✂️ Scissors beats 📄 Paper
        """)
        
        # Stats in sidebar
        st.header("📊 Game Statistics")
        st.metric("Total Rounds", game.round)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Your Wins", game.scores["player"])
        col2.metric("Computer Wins", game.scores["computer"])
        col3.metric("Ties", game.scores["ties"])
        
        # Win rate calculation
        non_tie_games = game.round - game.scores["ties"]
        if non_tie_games > 0:
            win_rate = (game.scores["player"] / non_tie_games) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
            
        # Reset button
        if st.button("🔄 Reset Game", use_container_width=True):
            game.reset_game()
            st.success("Game has been reset!")
            st.rerun()
    
    # Enhanced statistics in sidebar
    with st.sidebar:
        st.header("📊 Advanced Statistics")
        
        # Win rate by difficulty
        st.subheader("Win Rates by Difficulty")
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    difficulty,
                    COUNT(*) as total_games,
                    SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins
                FROM game_history
                GROUP BY difficulty
            """)
            
            for diff, total, wins in cursor.fetchall():
                win_rate = (wins / total * 100) if total > 0 else 0
                st.metric(
                    f"{diff.title()} Mode",
                    f"{win_rate:.1f}%",
                    f"{wins}/{total} games"
                )
        
        # Current streak
        st.metric("Current Win Streak", st.session_state.current_streak)
        
        # Achievements
        st.subheader("🏆 Achievements")
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.name, a.icon, a.description
                FROM achievements a
                JOIN player_achievements pa ON a.id = pa.achievement_id
                ORDER BY pa.earned_at DESC
            """)
            
            achievements = cursor.fetchall()
            if achievements:
                for name, icon, desc in achievements:
                    st.markdown(f"**{name}** {icon}")
                    st.caption(desc)
            else:
                st.caption("No achievements unlocked yet!")

    # Display last result
    if st.session_state.last_result:
        last = st.session_state.last_result
        st.markdown("---")
        st.markdown("### Last Round Result")
        
        # Create columns for choices
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### You chose")
            user_choice = last['user_choice']
            # Convert string to Choice enum if needed
            if isinstance(user_choice, str):
                try:
                    user_choice = Choice[user_choice.upper()]
                except KeyError:
                    st.error(f"Invalid choice value: {user_choice}")
                    user_choice = None
            
            if user_choice and isinstance(user_choice, Choice):
                st.markdown(f"# {game.EMOJIS[user_choice]} {user_choice}")
            
        with col2:
            st.markdown(f"#### Computer chose")
            computer_choice = last['computer_choice']
            # Convert string to Choice enum if needed
            if isinstance(computer_choice, str):
                try:
                    computer_choice = Choice[computer_choice.upper()]
                except KeyError:
                    st.error(f"Invalid choice value: {computer_choice}")
                    computer_choice = None
            
            if computer_choice and isinstance(computer_choice, Choice):
                st.markdown(f"# {game.EMOJIS[computer_choice]} {computer_choice}")

    # Game area
    st.markdown("## Make your choice:")
    
    # Choice buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🪨 Rock", use_container_width=True):
            game.play_round(Choice.ROCK)
            st.rerun()
            
    with col2:
        if st.button("📄 Paper", use_container_width=True):
            game.play_round(Choice.PAPER)
            st.rerun()
            
    with col3:
        if st.button("✂️ Scissors", use_container_width=True):
            game.play_round(Choice.SCISSORS)
            st.rerun()

    # Game history
    if st.session_state.game_history:
        st.markdown("---")
        with st.expander("📜 Game History"):
            history_df = []
            for round_data in st.session_state.game_history:
                user_choice = round_data['user_choice']
                computer_choice = round_data['computer_choice']
                
                # Convert string to Choice enum if needed
                if isinstance(user_choice, str):
                    try:
                        user_choice = Choice[user_choice.upper()]
                    except KeyError:
                        continue
                
                if isinstance(computer_choice, str):
                    try:
                        computer_choice = Choice[computer_choice.upper()]
                    except KeyError:
                        continue
                
                if isinstance(user_choice, Choice) and isinstance(computer_choice, Choice):
                    history_df.append({
                        "Round": round_data["round"],
                        "Your Choice": f"{game.EMOJIS[user_choice]} {user_choice}",
                        "Computer's Choice": f"{game.EMOJIS[computer_choice]} {computer_choice}",
                        "Result": "You Win 🏆" if round_data["result"] == GameResult.WIN else 
                                 "Computer Wins 🤖" if round_data["result"] == GameResult.LOSE else 
                                 "Tie 🤝"
                    })
            
            if history_df:
                st.dataframe(history_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Created by Asadullah48 | [GitHub Repository](https://github.com/asadullah48/rock-paper-scissors)")

if __name__ == "__main__":
    main()
