import random
import streamlit as st
from enum import Enum, auto
from typing import Tuple, Dict

# Set page config immediately at the top of the script
# before any other Streamlit commands
st.set_page_config(
    page_title="Rock Paper Scissors Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded",
)

class Choice(Enum):
    """Enumeration of possible game choices."""
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def __str__(self):
        return self.name.lower()

class GameResult(Enum):
    """Possible game outcomes."""
    WIN = auto()
    LOSE = auto()
    DRAW = auto()

class RockPaperScissors:
    """A complete Rock-Paper-Scissors game implementation for Streamlit."""
    
    WIN_CONDITIONS: Dict[Tuple[Choice, Choice], GameResult] = {
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

    @property
    def scores(self):
        return st.session_state.scores
        
    @property
    def round(self):
        return st.session_state.round
        
    @property
    def game_history(self):
        return st.session_state.game_history
    
    def _get_computer_choice(self) -> Choice:
        """Generate a random choice for the computer."""
        return random.choice(list(Choice))

    def _determine_winner(self, user: Choice, computer: Choice) -> GameResult:
        """Determine the game outcome based on choices."""
        if user == computer:
            return GameResult.DRAW
        return self.WIN_CONDITIONS.get((user, computer), GameResult.LOSE)

    def play_round(self, user_choice: Choice) -> GameResult:
        """Play one round of the game with the given user choice."""
        st.session_state.round += 1
        
        computer_choice = self._get_computer_choice()
        result = self._determine_winner(user_choice, computer_choice)
        
        # Update scores
        if result == GameResult.WIN:
            st.session_state.scores["player"] += 1
        elif result == GameResult.LOSE:
            st.session_state.scores["computer"] += 1
        else:
            st.session_state.scores["ties"] += 1
            
        # Store round results
        round_result = {
            "round": st.session_state.round,
            "user_choice": user_choice,
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
        

def main():
    # Initialize game
    game = RockPaperScissors()
    
    # App header
    st.title("🎮 Rock Paper Scissors")
    st.markdown("### Play the classic game against the computer!")
    
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
        total_games = sum(game.scores.values())
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
    
    # Display last result
    if st.session_state.last_result:
        last = st.session_state.last_result
        st.markdown("---")
        st.markdown("### Last Round Result")
        
        # Create columns for choices
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### You chose")
            st.markdown(f"# {game.EMOJIS[last['user_choice']]} {last['user_choice']}")
            
        with col2:
            st.markdown(f"#### Computer chose")
            st.markdown(f"# {game.EMOJIS[last['computer_choice']]} {last['computer_choice']}")
        
        # Show result with appropriate styling
        if last["result"] == GameResult.WIN:
            st.success("### 🎉 You win this round!", icon="🏆")
        elif last["result"] == GameResult.LOSE:
            st.error("### 💻 Computer wins this round!", icon="🤖")
        else:
            st.info("### 🤝 It's a tie!", icon="🔄")
            
        # Current score summary
        st.markdown(f"**Score:** You {game.scores['player']} - {game.scores['computer']} Computer (Ties: {game.scores['ties']})")
    
    # Game history
    if game.game_history:
        st.markdown("---")
        with st.expander("📜 Game History"):
            history_df = []
            for round_data in game.game_history:
                history_df.append({
                    "Round": round_data["round"],
                    "Your Choice": f"{game.EMOJIS[round_data['user_choice']]} {round_data['user_choice']}",
                    "Computer's Choice": f"{game.EMOJIS[round_data['computer_choice']]} {round_data['computer_choice']}",
                    "Result": "You Win 🏆" if round_data["result"] == GameResult.WIN else 
                             "Computer Wins 🤖" if round_data["result"] == GameResult.LOSE else 
                             "Tie 🤝"
                })
            st.dataframe(history_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Created by Asadullah48 | [GitHub Repository](https://github.com/asadullah48/rock-paper-scissors)")

if __name__ == "__main__":
    main()