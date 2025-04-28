
import streamlit as st
import pygame
import numpy as np
from PIL import Image
import time
import sqlite3

# Streamlit configuration - MUST BE FIRST
st.set_page_config(
    page_title="Connect Four Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling (moved after set_page_config)
st.markdown("""
<style>
    /* Main background with enhanced gradient */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c 0%, #2a5298 50%, #1e3c72 100%);
        background-attachment: fixed;
    }
    
    /* Card-like containers with new colors */
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        transition: all 0.3s ease;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #FF8E8E, #FF6B6B);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    /* Enhanced game board container */
    .game-board-container {
        background: rgba(41, 59, 95, 0.9);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 25px 0;
    }
    
    /* Enhanced turn indicator */
    .turn-indicator {
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.2));
        padding: 15px 30px;
        border-radius: 50px;
        text-align: center;
        margin: 15px 0;
        font-weight: bold;
        letter-spacing: 1px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced winning message */
    .winning-message {
        animation: celebrate 1.5s infinite;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 25px 0;
        font-size: 1.5em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Enhanced dropdown and label styling */
    .stSelectbox label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background-color: #2C3E50 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2C3E50 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Style for dropdown options */
    div[data-baseweb="popover"] div[data-baseweb="select__option"] {
        background-color: #2C3E50 !important;
        color: #FFFFFF !important;
    }
    
    div[data-baseweb="popover"] div[data-baseweb="select__option"]:hover {
        background-color: #34495E !important;
    }
    
    /* Style for the dropdown container */
    div[data-baseweb="popover"] {
        background-color: #2C3E50 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Enhanced text input styling */
    .stTextInput label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .stTextInput input {
        background-color: #2C3E50 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Enhanced slider styling */
    .stSlider label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .stSlider [data-baseweb="slider"] {
        margin-top: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Game constants
ROW_COUNT = 6
COL_COUNT = 7
SQUARE_SIZE = 80
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = COL_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE

# Enhanced color scheme
COLORS = {
    'BOARD_BG': (41, 59, 95),      # Deep blue background
    'GRID': (65, 89, 136),         # Lighter blue for grid
    'EMPTY': (200, 200, 220),      # Light gray for empty slots
    'PLAYER1': (255, 107, 107),    # Coral red for player 1
    'PLAYER2': (255, 209, 102),    # Warm yellow for player 2
    'HOVER': (150, 170, 200, 128)  # Semi-transparent hover effect
}

def init_database():
    """Initialize the SQLite database and create necessary tables if they don't exist."""
    try:
        with sqlite3.connect('connect_four.db') as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS game_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1_name TEXT NOT NULL,
                    player2_name TEXT NOT NULL,
                    winner INTEGER NOT NULL,
                    moves_count INTEGER NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database initialization error: {e}")

def get_game_stats():
    """Get game statistics from the database"""
    try:
        # Initialize database if not already done
        init_database()
        
        with sqlite3.connect('connect_four.db') as conn:
            cursor = conn.cursor()
            # Get total games
            cursor.execute("SELECT COUNT(*) FROM game_stats")
            total_games = cursor.fetchone()[0]
            
            # Get average moves
            cursor.execute("SELECT AVG(moves_count) FROM game_stats")
            avg_moves = cursor.fetchone()[0]
            
            return {
                'total_games': total_games or 0,
                'avg_moves': round(avg_moves, 1) if avg_moves else 0
            }
    except sqlite3.Error as e:
        st.warning(f"Could not fetch game statistics: {e}")
        return {'total_games': 0, 'avg_moves': 0}

class ConnectFourGame:
    def __init__(self):
        """Initialize the Connect Four game with an empty board."""
        self.board = np.zeros((ROW_COUNT, COL_COUNT))
        self.game_over = False
        self.turn = 0  # 0 for Player 1 (Red), 1 for Player 2 (Yellow)
        self.winner = None
        self.moves_count = 0
        self.start_time = time.time()
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        
        # Initialize Pygame for rendering
        pygame.init()
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("Arial", 36)

    def draw_board(self):
        """Draw the current state of the board and return as PIL Image."""
        # Fill background with board background color
        self.screen.fill(COLORS['BOARD_BG'])
        
        # Draw the blue board with circular holes
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, COLORS['GRID'], 
                               (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(self.screen, COLORS['EMPTY'], 
                                (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                 int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        
        # Draw the game pieces
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == 1:  # Player 1 pieces
                    pygame.draw.circle(self.screen, COLORS['PLAYER1'], 
                                     (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                      HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:  # Player 2 pieces
                    pygame.draw.circle(self.screen, COLORS['PLAYER2'], 
                                     (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                      HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        
        # Convert Pygame surface to PIL Image
        img_str = pygame.image.tostring(self.screen, 'RGB')
        img = Image.frombytes('RGB', (WIDTH, HEIGHT), img_str)
        return img

    def make_move(self, col):
        """Process a move in the selected column and return game status message."""
        if self.game_over:
            return "Game is over! Please reset to play again."
            
        if not self.is_valid_location(col):
            return "Column is full! Choose another column."
            
        # Find the next open row and drop the piece
        row = self.get_next_open_row(col)
        piece = 1 if self.turn == 0 else 2
        self.drop_piece(row, col, piece)
        self.moves_count += 1
        
        # Check for win condition
        if self.check_win(piece):
            self.game_over = True
            self.winner = piece
            return f"🎉 Player {piece} ({self.get_player_color(piece)}) wins!"
        
        # Check for draw condition
        if self.moves_count == ROW_COUNT * COL_COUNT:
            self.game_over = True
            return "🤝 It's a draw!"
        
        # Switch turns
        self.turn = 1 - self.turn
        return None

    def get_player_color(self, piece):
        """Return the color name of the player piece."""
        return "Red" if piece == 1 else "Yellow"

    def drop_piece(self, row, col, piece):
        """Place a piece on the board at the specified position."""
        self.board[row][col] = piece

    def is_valid_location(self, col):
        """Check if a piece can be placed in the specified column."""
        return 0 <= col < COL_COUNT and self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        """Find the lowest empty row in the specified column."""
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r
        return -1  # Should never reach here if is_valid_location is checked first

    def check_win(self, piece):
        """Check if the current player has won after placing their piece."""
        # Horizontal check
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical check
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal check (positive slope)
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal check (negative slope)
        for c in range(COL_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True
                    
        return False

    def reset(self):
        """Reset the game to its initial state."""
        self.board = np.zeros((ROW_COUNT, COL_COUNT))
        self.game_over = False
        self.turn = 0
        self.winner = None
        self.moves_count = 0
        self.start_time = time.time()

    def save_game_stats(self):
        """Save game statistics to database."""
        try:
            duration = int(time.time() - self.start_time)
            winner = 0 if self.winner is None else self.winner
            
            query = """
            INSERT INTO game_stats 
            (player1_name, player2_name, winner, moves_count, duration_seconds)
            VALUES (?, ?, ?, ?, ?)
            """
            params = (self.player1_name, self.player2_name, winner, 
                     self.moves_count, duration)
            
            with sqlite3.connect('connect_four.db') as conn:
                conn.execute(query, params)
                conn.commit()
        except sqlite3.Error as e:
            st.error(f"Failed to save game statistics: {e}")

def main():
    # Initialize game in session state if not already present
    if 'game' not in st.session_state:
        st.session_state.game = ConnectFourGame()
        st.session_state.message = None
        st.session_state.game_mode = "Player vs Player"  # Default game mode
    
    # Custom container for title
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                🎮 Connect Four Game
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with game settings
    with st.sidebar:
        st.markdown("""
            <div style='background: rgba(44, 62, 80, 0.9); 
                        padding: 20px; 
                        border-radius: 10px; 
                        margin-bottom: 20px;'>
                <h2 style='color: white; text-align: center;'>⚙️ Game Settings</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Game mode selection
        st.markdown("""
            <div style='background: rgba(44, 62, 80, 0.9); 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin-bottom: 20px;'>
        """, unsafe_allow_html=True)
        
        st.session_state.game_mode = st.selectbox(
            "🎮 Game Mode",
            ["Player vs Player", "Player vs AI"],
            key="game_mode_select"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # AI difficulty selection (if AI mode is selected)
        if st.session_state.game_mode == "Player vs AI":
            st.markdown("""
                <div style='background: rgba(44, 62, 80, 0.9); 
                            padding: 15px; 
                            border-radius: 10px; 
                            margin-bottom: 20px;'>
            """, unsafe_allow_html=True)
            
            st.session_state.ai_difficulty = st.select_slider(
                "🤖 AI Difficulty",
                options=["easy", "medium", "hard"],
                value="medium",
                key="ai_difficulty_select"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Player names input
        st.markdown("""
            <div style='background: rgba(44, 62, 80, 0.9); 
                        padding: 15px; 
                        border-radius: 10px;'>
        """, unsafe_allow_html=True)
        
        st.session_state.player1_name = st.text_input(
            "🔴 Player 1 Name",
            value="Player 1" if "player1_name" not in st.session_state else st.session_state.player1_name
        )
        
        if st.session_state.game_mode == "Player vs Player":
            st.session_state.player2_name = st.text_input(
                "🟡 Player 2 Name",
                value="Player 2" if "player2_name" not in st.session_state else st.session_state.player2_name
            )
        else:
            st.session_state.player2_name = "AI"
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Game statistics with custom styling
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.1); 
                        padding: 20px; 
                        border-radius: 10px; 
                        margin-top: 20px;'>
                <h3 style='color: white; text-align: center;'>📊 Game Statistics</h3>
            </div>
        """, unsafe_allow_html=True)
        
        stats = get_game_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div>Games Played</div>
                    <div class='metric-value'>{stats['total_games']}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div>Avg Moves</div>
                    <div class='metric-value'>{stats['avg_moves']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Main game area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Game board container with glass morphism effect
        st.markdown("<div class='game-board-container'>", unsafe_allow_html=True)
        game_img = st.session_state.game.draw_board()
        st.image(game_img, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.1); 
                        padding: 20px; 
                        border-radius: 10px;'>
                <h3 style='color: white; text-align: center;'>Game Controls</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Column selection buttons
        st.write("Drop your piece in a column:")
        cols = st.columns(6)  # Changed from 7
        for i in range(6):    # Changed from 7
            with cols[i]:
                disabled = not st.session_state.game.is_valid_location(i) or st.session_state.game.game_over
                if st.button(str(i+1), key=f"col_{i}", disabled=disabled):
                    st.session_state.message = st.session_state.game.make_move(i)
                    st.rerun()
        
        # Game status display with enhanced styling
        if st.session_state.message:
            if "wins" in st.session_state.message:
                st.markdown(f"""
                    <div class='winning-message'>
                        {st.session_state.message}
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.game.save_game_stats()
            elif "draw" in st.session_state.message:
                st.info(st.session_state.message)
                st.session_state.game.save_game_stats()
            else:
                st.warning(st.session_state.message)
        
        # Current turn indicator with custom styling
        if not st.session_state.game.game_over:
            current_player = "Red" if st.session_state.game.turn == 0 else "Yellow"
            current_color = "🔴" if st.session_state.game.turn == 0 else "🟡"
            st.markdown(f"""
                <div class='turn-indicator'>
                    Current Turn: {current_color} {current_player}
                </div>
            """, unsafe_allow_html=True)
        
        # Reset game button with custom styling
        if st.button("🔄 Reset Game", type="primary"):
            st.session_state.game.reset()
            st.session_state.message = None
            st.rerun()
        
        # Moves counter with custom styling
        st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.1); 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin-top: 20px; 
                        text-align: center;'>
                <span style='color: white;'>Moves played: {st.session_state.game.moves_count}</span>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    init_database()
    main()
