import streamlit as st
import pygame
import pygame.locals
import random
import base64
import io
from PIL import Image
import time

# Initialize session state variables if they don't exist
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'lines_cleared' not in st.session_state:
    st.session_state.lines_cleared = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'frame' not in st.session_state:
    st.session_state.frame = None

# Game constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
COLS = SCREEN_WIDTH // BLOCK_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

class Tetrimino:
    def __init__(self, shape=None, color=None):
        if shape is None:
            shape_idx = random.randint(0, len(SHAPES) - 1)
            self.shape = SHAPES[shape_idx]
            self.color = COLORS[shape_idx]
        else:
            self.shape = shape
            self.color = color
        
        self.x = int(COLS / 2) - int(len(self.shape[0]) / 2)
        self.y = 0

    def rotate(self):
        """ Rotate the tetrimino by 90 degrees """
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid():
    return [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

def check_collision(grid, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                if x + tetrimino.x < 0 or x + tetrimino.x >= COLS or y + tetrimino.y >= ROWS:
                    return True
                if y + tetrimino.y >= 0 and grid[y + tetrimino.y][x + tetrimino.x] != BLACK:
                    return True
    return False

def lock_tetrimino(grid, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell and y + tetrimino.y >= 0:
                grid[y + tetrimino.y][x + tetrimino.x] = tetrimino.color
    return grid

def clear_lines(grid):
    lines_cleared = 0
    for i in range(len(grid) - 1, -1, -1):
        if all(cell != BLACK for cell in grid[i]):
            grid.pop(i)
            grid.insert(0, [BLACK for _ in range(COLS)])
            lines_cleared += 1
    return lines_cleared

def calculate_score(lines_cleared, level):
    if lines_cleared == 1:
        return 100 * level
    elif lines_cleared == 2:
        return 300 * level
    elif lines_cleared == 3:
        return 500 * level
    elif lines_cleared == 4:
        return 800 * level  # Tetris!
    return 0

def pygame_to_image(surface):
    """Convert pygame surface to an image"""
    data = pygame.image.tostring(surface, 'RGB')
    img = Image.frombytes('RGB', surface.get_size(), data)
    return img

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return img_str

def draw_game_screen(grid, current_tetrimino, next_tetrimino, score, level, lines_cleared, high_score):
    """Draw the game screen and return a PIL image"""
    # Initialize pygame if not already done
    pygame.init()
    
    # Create a surface
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    
    # Draw grid
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    # Draw current tetrimino
    for y, row in enumerate(current_tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_tetrimino.color, 
                                ((current_tetrimino.x + x) * BLOCK_SIZE, 
                                 (current_tetrimino.y + y) * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, 
                                ((current_tetrimino.x + x) * BLOCK_SIZE, 
                                 (current_tetrimino.y + y) * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE), 1)
    
    # Draw score and level
    font = pygame.font.SysFont('Arial', 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lines_text = font.render(f"Lines: {lines_cleared}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(lines_text, (10, 70))
    
    # Convert to PIL image
    img = pygame_to_image(screen)
    return img

def game_step(grid, current_tetrimino, next_tetrimino, score, level, lines_cleared):
    """Perform one step of the game logic"""
    # Move piece down
    current_tetrimino.y += 1
    
    # Check for collision
    if check_collision(grid, current_tetrimino):
        current_tetrimino.y -= 1
        grid = lock_tetrimino(grid, current_tetrimino)
        
        # Check for cleared lines
        new_lines_cleared = clear_lines(grid)
        lines_cleared += new_lines_cleared
        
        # Update score
        if new_lines_cleared > 0:
            score += calculate_score(new_lines_cleared, level)
        
        # Check for level up
        new_level = lines_cleared // 10 + 1
        level_up = new_level > level
        level = new_level
        
        # Get next piece
        current_tetrimino = next_tetrimino
        next_tetrimino = Tetrimino()
        
        # Check if game is over
        game_over = check_collision(grid, current_tetrimino)
        
        return grid, current_tetrimino, next_tetrimino, score, level, lines_cleared, game_over
    
    return grid, current_tetrimino, next_tetrimino, score, level, lines_cleared, False

def handle_keyboard_input(key, grid, current_tetrimino):
    """Handle keyboard input for game controls"""
    if key == 'left':
        current_tetrimino.x -= 1
        if check_collision(grid, current_tetrimino):
            current_tetrimino.x += 1
    
    elif key == 'right':
        current_tetrimino.x += 1
        if check_collision(grid, current_tetrimino):
            current_tetrimino.x -= 1
    
    elif key == 'down':
        current_tetrimino.y += 1
        if check_collision(grid, current_tetrimino):
            current_tetrimino.y -= 1
    
    elif key == 'up':
        original_shape = [row[:] for row in current_tetrimino.shape]
        current_tetrimino.rotate()
        if check_collision(grid, current_tetrimino):
            # Try to adjust position to make rotation work
            original_x = current_tetrimino.x
            
            # Try moving left or right to fit
            for adjust in [-1, 1, -2, 2]:
                current_tetrimino.x += adjust
                if not check_collision(grid, current_tetrimino):
                    break
                current_tetrimino.x = original_x
            else:
                # If no position works, revert the rotation
                current_tetrimino.shape = original_shape
    
    elif key == 'space':
        # Hard drop
        while not check_collision(grid, current_tetrimino):
            current_tetrimino.y += 1
        current_tetrimino.y -= 1  # Move back up to valid position
    
    return grid, current_tetrimino

def start_game():
    """Initialize a new game"""
    st.session_state.grid = create_grid()
    st.session_state.current_tetrimino = Tetrimino()
    st.session_state.next_tetrimino = Tetrimino()
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.lines_cleared = 0
    st.session_state.game_state = 'playing'
    st.session_state.last_update = time.time()

def restart_game():
    """Restart the game"""
    start_game()

def main():
    st.set_page_config(page_title="Streamlit Tetris", layout="centered")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 20px;
    }
    .game-container {
        display: flex;
        justify-content: center;
    }
    .controls {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .controls-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .control-key {
        font-weight: bold;
        background-color: #404040;
        padding: 3px 7px;
        border-radius: 4px;
        margin-right: 5px;
    }
    .score-display {
        font-size: 20px;
        margin: 10px 0;
    }
    button {
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="title">Streamlit Tetris</div>', unsafe_allow_html=True)
    
    # Game state handling
    if st.session_state.game_state == 'start':
        st.markdown("Welcome to Tetris! Press 'Start Game' to begin playing.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Game", key="start_button"):
                start_game()
        
        # Instructions
        st.markdown("## How to Play")
        st.markdown("* Use the arrow buttons to move and rotate the pieces")
        st.markdown("* Clear lines to score points")
        st.markdown("* The game speeds up as you level up")
        st.markdown("* Game ends when pieces stack to the top")
        
    elif st.session_state.game_state == 'playing':
        # Get current game state
        if 'grid' not in st.session_state:
            st.session_state.grid = create_grid()
        if 'current_tetrimino' not in st.session_state:
            st.session_state.current_tetrimino = Tetrimino()
        if 'next_tetrimino' not in st.session_state:
            st.session_state.next_tetrimino = Tetrimino()
        
        # Game display
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Auto-update the game at regular intervals based on level
            current_time = time.time()
            time_since_last_update = current_time - st.session_state.last_update
            fall_speed = max(0.1, 1.0 - (st.session_state.level - 1) * 0.05)  # Speed increases with level
            
            # Check if it's time to update the game state
            if time_since_last_update > fall_speed:
                st.session_state.grid, st.session_state.current_tetrimino, st.session_state.next_tetrimino, \
                st.session_state.score, st.session_state.level, st.session_state.lines_cleared, game_over = \
                    game_step(
                        st.session_state.grid, 
                        st.session_state.current_tetrimino, 
                        st.session_state.next_tetrimino, 
                        st.session_state.score, 
                        st.session_state.level, 
                        st.session_state.lines_cleared
                    )
                
                st.session_state.last_update = current_time
                
                # Update high score if needed
                if st.session_state.score > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.score
                
                # Check for game over
                if game_over:
                    st.session_state.game_state = 'game_over'
                    st.rerun()
            
            # Generate game display
            game_image = draw_game_screen(
                st.session_state.grid,
                st.session_state.current_tetrimino,
                st.session_state.next_tetrimino,
                st.session_state.score,
                st.session_state.level,
                st.session_state.lines_cleared,
                st.session_state.high_score
            )
            
            # Display the game
            st.image(game_image, use_container_width=True)
        
        with col2:
            st.markdown(f"<div class='score-display'>Score: {st.session_state.score}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='score-display'>Level: {st.session_state.level}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='score-display'>Lines: {st.session_state.lines_cleared}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='score-display'>High Score: {st.session_state.high_score}</div>", unsafe_allow_html=True)
            
            if st.button("Restart", key="restart_button"):
                restart_game()
        
        # Game controls
        st.markdown("<div class='controls'>", unsafe_allow_html=True)
        st.markdown("<div class='controls-title'>Controls</div>", unsafe_allow_html=True)
        
        # Create rows of control buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Row 1 - Rotate
        col1.write("")
        if col2.button("⬆️ Rotate"):
            st.session_state.grid, st.session_state.current_tetrimino = handle_keyboard_input(
                'up', st.session_state.grid, st.session_state.current_tetrimino
            )
        col3.write("")
        
        # Row 2 - Left, Down, Right
        if col1.button("⬅️ Left"):
            st.session_state.grid, st.session_state.current_tetrimino = handle_keyboard_input(
                'left', st.session_state.grid, st.session_state.current_tetrimino
            )
        
        if col2.button("⬇️ Down"):
            st.session_state.grid, st.session_state.current_tetrimino = handle_keyboard_input(
                'down', st.session_state.grid, st.session_state.current_tetrimino
            )
        
        if col3.button("➡️ Right"):
            st.session_state.grid, st.session_state.current_tetrimino = handle_keyboard_input(
                'right', st.session_state.grid, st.session_state.current_tetrimino
            )
        
        # Row 3 - Hard Drop
        col1.write("")
        if col2.button("🔽 Hard Drop"):
            st.session_state.grid, st.session_state.current_tetrimino = handle_keyboard_input(
                'space', st.session_state.grid, st.session_state.current_tetrimino
            )
            # Immediately apply the result of hard drop
            st.session_state.grid, st.session_state.current_tetrimino, st.session_state.next_tetrimino, \
            st.session_state.score, st.session_state.level, st.session_state.lines_cleared, game_over = \
                game_step(
                    st.session_state.grid, 
                    st.session_state.current_tetrimino, 
                    st.session_state.next_tetrimino, 
                    st.session_state.score, 
                    st.session_state.level, 
                    st.session_state.lines_cleared
                )
            
            # Check for game over
            if game_over:
                st.session_state.game_state = 'game_over'
                st.experimental_rerun()
        col3.write("")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Auto-refresh to update game state
        st.empty()
        time.sleep(0.1)  # Small delay to prevent excessive refreshing
        st.rerun()
        
    elif st.session_state.game_state == 'game_over':
        st.markdown("<h1 style='text-align: center; color: red;'>Game Over!</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>Final Score: {st.session_state.score}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px;'>High Score: {st.session_state.high_score}</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Play Again", key="play_again"):
                restart_game()

if __name__ == "__main__":
    main()