import streamlit as st
import pygame
import numpy as np
from PIL import Image
import time

# Streamlit configuration
st.set_page_config(
    page_title="Connect Four Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game constants
ROW_COUNT = 6
COL_COUNT = 7
SQUARE_SIZE = 80
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = COL_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class ConnectFourGame:
    def __init__(self):
        """Initialize the Connect Four game with an empty board."""
        self.board = np.zeros((ROW_COUNT, COL_COUNT))
        self.game_over = False
        self.turn = 0  # 0 for Player 1 (Red), 1 for Player 2 (Yellow)
        self.winner = None
        self.moves_count = 0
        
        # Initialize Pygame for rendering
        pygame.init()
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("Arial", 36)

    def draw_board(self):
        """Draw the current state of the board and return as PIL Image."""
        # Fill background
        self.screen.fill(WHITE)
        
        # Draw the blue board with circular holes
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, 
                               (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(self.screen, WHITE, 
                                (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                 int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        
        # Draw the game pieces (Red and Yellow)
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == 1:  # Red pieces (Player 1)
                    pygame.draw.circle(self.screen, RED, 
                                     (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                      HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:  # Yellow pieces (Player 2)
                    pygame.draw.circle(self.screen, YELLOW, 
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

# Application setup
def main():
    st.title("🎮 Connect Four - Streamlit Edition")
    
    # Game description
    with st.expander("How to Play"):
        st.markdown("""
        ### Rules:
        1. Players take turns dropping colored discs into the board
        2. The first player to connect 4 discs in a row (horizontally, vertically, or diagonally) wins
        3. If the board fills up without a winner, the game is a draw
        
        ### Controls:
        - Click on the column buttons (1-7) to drop your disc
        - Use the Reset button to start a new game
        """)
    
    # Initialize game in session state if not already present
    if 'game' not in st.session_state:
        st.session_state.game = ConnectFourGame()
        st.session_state.message = None
    
    # Layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display game board
        game_img = st.session_state.game.draw_board()
        st.image(game_img, use_container_width=True)
    
    with col2:
        st.header("Game Controls")
        
        # Column selection buttons
        st.write("Drop your piece in a column:")
        
        # Display buttons in a row with custom colors
        cols = st.columns(7)
        for i in range(7):
            with cols[i]:
                button_color = "normal"
                # Disable button if column is full
                disabled = not st.session_state.game.is_valid_location(i) or st.session_state.game.game_over
                if st.button(str(i+1), key=f"col_{i}", disabled=disabled):
                    st.session_state.message = st.session_state.game.make_move(i)
                    st.rerun()
        
        # Game status display
        st.markdown("---")
        if st.session_state.message:
            if "wins" in st.session_state.message:
                st.success(st.session_state.message)
            elif "draw" in st.session_state.message:
                st.info(st.session_state.message)
            else:
                st.warning(st.session_state.message)
        
        # Current turn indicator
        if not st.session_state.game.game_over:
            current_player = "Red" if st.session_state.game.turn == 0 else "Yellow"
            current_color = "🔴" if st.session_state.game.turn == 0 else "🟡"
            st.info(f"Current Turn: {current_color} {current_player}")
        
        # Reset game button
        if st.button("🔄 Reset Game", type="primary"):
            st.session_state.game.reset()
            st.session_state.message = None
            st.rerun()
        
        # Game statistics
        st.markdown("---")
        st.markdown(f"**Moves played:** {st.session_state.game.moves_count}")
        
        # Credits
        st.markdown("---")
        st.markdown("Created by [asadullah48](https://github.com/asadullah48)")

if __name__ == "__main__":
    main()