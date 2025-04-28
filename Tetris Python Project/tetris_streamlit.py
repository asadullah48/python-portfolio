import streamlit as st
import pygame
import pygame.locals
import random
import base64
import io
from PIL import Image
import time
import json
import os
from datetime import datetime

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
if 'paused' not in st.session_state:
    st.session_state.paused = False
if 'held_piece' not in st.session_state:
    st.session_state.held_piece = None
if 'can_hold' not in st.session_state:
    st.session_state.can_hold = True
if 'game_stats' not in st.session_state:
    st.session_state.game_stats = {
        'pieces_placed': 0,
        'lines_cleared': 0,
        'tetris_count': 0,  # Count of 4-line clears
        'max_level': 1,
        'max_score': 0,
        'games_played': 0,
        'total_play_time': 0
    }
if 'game_start_time' not in st.session_state:
    st.session_state.game_start_time = time.time()
if 'leaderboard' not in st.session_state:
    # Try to load leaderboard from file if it exists
    if os.path.exists('tetris_leaderboard.json'):
        try:
            with open('tetris_leaderboard.json', 'r') as f:
                st.session_state.leaderboard = json.load(f)
        except:
            st.session_state.leaderboard = []
    else:
        st.session_state.leaderboard = []
if 'show_ghost' not in st.session_state:
    st.session_state.show_ghost = True
if 'theme' not in st.session_state:
    st.session_state.theme = 'classic'  # Options: 'classic', 'dark', 'neon'
if 'sound_enabled' not in st.session_state:
    st.session_state.sound_enabled = True

# Game constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
COLS = SCREEN_WIDTH // BLOCK_SIZE
SIDEBAR_WIDTH = 200  # Width for the sidebar (next piece, hold, etc.)
FULL_WIDTH = SCREEN_WIDTH + SIDEBAR_WIDTH

# Base Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Theme definitions
THEMES = {
    'classic': {
        'background': BLACK,
        'grid_lines': DARK_GRAY,
        'text': WHITE,
        'sidebar_bg': DARK_GRAY,
        'ui_accent': BLUE,
        'piece_colors': [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED],
        'ghost_alpha': 100,  # Transparency for ghost piece (0-255)
    },
    'dark': {
        'background': (20, 20, 30),
        'grid_lines': (40, 40, 60),
        'text': (220, 220, 255),
        'sidebar_bg': (30, 30, 45),
        'ui_accent': (100, 100, 255),
        'piece_colors': [(0, 240, 240), (0, 0, 240), (240, 160, 0), (240, 240, 0), (0, 240, 0), (240, 0, 240), (240, 0, 0)],
        'ghost_alpha': 80,
    },
    'neon': {
        'background': (10, 10, 20),
        'grid_lines': (30, 30, 50),
        'text': (255, 255, 255),
        'sidebar_bg': (20, 20, 40),
        'ui_accent': (0, 255, 200),
        'piece_colors': [(0, 255, 255), (0, 100, 255), (255, 150, 0), (255, 255, 0), (0, 255, 100), (255, 0, 255), (255, 50, 50)],
        'ghost_alpha': 60,
    }
}

# Default to classic theme
COLORS = THEMES['classic']['piece_colors']

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
    def __init__(self, shape=None, color=None, shape_idx=None):
        if shape is None:
            if shape_idx is None:
                shape_idx = random.randint(0, len(SHAPES) - 1)
            self.shape = [row[:] for row in SHAPES[shape_idx]]  # Deep copy
            self.color = THEMES[st.session_state.theme]['piece_colors'][shape_idx]
            self.shape_idx = shape_idx
        else:
            self.shape = shape
            self.color = color
            self.shape_idx = shape_idx if shape_idx is not None else -1

        self.x = int(COLS / 2) - int(len(self.shape[0]) / 2)
        self.y = 0
        self.rotation = 0  # Track rotation state (0, 1, 2, 3)

    def rotate(self, clockwise=True):
        """ Rotate the tetrimino by 90 degrees """
        original_shape = [row[:] for row in self.shape]  # Deep copy
        if clockwise:
            self.shape = [list(row) for row in zip(*self.shape[::-1])]
            self.rotation = (self.rotation + 1) % 4
        else:
            # Counter-clockwise rotation
            self.shape = [list(row) for row in zip(*[row[::-1] for row in self.shape])]
            self.rotation = (self.rotation - 1) % 4
        return original_shape

    def copy(self):
        """ Create a copy of this tetrimino """
        new_tetrimino = Tetrimino(
            shape=[row[:] for row in self.shape],  # Deep copy
            color=self.color,
            shape_idx=self.shape_idx
        )
        new_tetrimino.x = self.x
        new_tetrimino.y = self.y
        new_tetrimino.rotation = self.rotation
        return new_tetrimino

    def get_ghost_position(self, grid):
        """ Calculate where the piece would land if dropped """
        ghost = self.copy()
        while not check_collision(grid, ghost):
            ghost.y += 1
        ghost.y -= 1  # Move back up to last valid position
        return ghost

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
        # Update tetris count in stats
        if 'game_stats' in st.session_state:
            st.session_state.game_stats['tetris_count'] += 1
        return 800 * level  # Tetris!
    return 0

def hold_piece():
    """Hold the current piece and swap with previously held piece if any"""
    if not st.session_state.can_hold:
        return None  # Can only hold once per piece

    current = st.session_state.current_tetrimino

    if st.session_state.held_piece is None:
        # No piece currently held, store current and get a new one
        st.session_state.held_piece = current.shape_idx
        new_piece = st.session_state.next_tetrimino
        st.session_state.next_tetrimino = Tetrimino()
    else:
        # Swap with held piece
        held_idx = st.session_state.held_piece
        st.session_state.held_piece = current.shape_idx
        new_piece = Tetrimino(shape_idx=held_idx)

    st.session_state.can_hold = False  # Can't hold again until a new piece is placed
    return new_piece

def update_stats(score, level, lines_cleared):
    """Update game statistics"""
    stats = st.session_state.game_stats
    stats['lines_cleared'] = lines_cleared
    stats['max_score'] = max(stats['max_score'], score)
    stats['max_level'] = max(stats['max_level'], level)

def save_to_leaderboard(player_name, score, level, lines_cleared):
    """Save the current game score to the leaderboard"""
    if not player_name:
        player_name = "Anonymous"

    entry = {
        'name': player_name,
        'score': score,
        'level': level,
        'lines': lines_cleared,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    st.session_state.leaderboard.append(entry)
    # Sort by score (highest first)
    st.session_state.leaderboard = sorted(
        st.session_state.leaderboard,
        key=lambda x: x['score'],
        reverse=True
    )

    # Keep only top 10 scores
    if len(st.session_state.leaderboard) > 10:
        st.session_state.leaderboard = st.session_state.leaderboard[:10]

    # Save to file
    try:
        with open('tetris_leaderboard.json', 'w') as f:
            json.dump(st.session_state.leaderboard, f)
    except:
        pass  # Silently fail if we can't write to file

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

    # Get current theme
    theme = THEMES[st.session_state.theme]

    # Create a surface with sidebar
    screen = pygame.Surface((FULL_WIDTH, SCREEN_HEIGHT))
    screen.fill(theme['background'])

    # Draw background pattern or gradient based on theme
    if st.session_state.theme == 'neon':
        # Create a gradient background for neon theme
        for y in range(SCREEN_HEIGHT):
            # Gradient from dark blue to black
            color = (
                max(0, int(10 - y / SCREEN_HEIGHT * 10)),
                max(0, int(10 - y / SCREEN_HEIGHT * 5)),
                max(0, int(30 - y / SCREEN_HEIGHT * 10))
            )
            pygame.draw.line(screen, color, (0, y), (FULL_WIDTH, y))

    # Draw sidebar background
    pygame.draw.rect(screen, theme['sidebar_bg'],
                    (SCREEN_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))

    # Draw grid background
    pygame.draw.rect(screen, theme['background'],
                    (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw grid lines
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x],
                            (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, theme['grid_lines'],
                            (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw ghost piece if enabled
    if st.session_state.show_ghost and not st.session_state.paused:
        ghost = current_tetrimino.get_ghost_position(grid)
        for y, row in enumerate(ghost.shape):
            for x, cell in enumerate(row):
                if cell:
                    # Create a semi-transparent version of the piece color
                    ghost_color = list(current_tetrimino.color)
                    ghost_color.append(theme['ghost_alpha'])  # Add alpha channel

                    # Draw ghost piece with transparency
                    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    s.fill(ghost_color)
                    screen.blit(s, ((ghost.x + x) * BLOCK_SIZE, (ghost.y + y) * BLOCK_SIZE))

                    # Draw outline
                    pygame.draw.rect(screen, theme['grid_lines'],
                                    ((ghost.x + x) * BLOCK_SIZE,
                                     (ghost.y + y) * BLOCK_SIZE,
                                     BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw current tetrimino
    for y, row in enumerate(current_tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_tetrimino.color,
                                ((current_tetrimino.x + x) * BLOCK_SIZE,
                                 (current_tetrimino.y + y) * BLOCK_SIZE,
                                 BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, theme['text'],
                                ((current_tetrimino.x + x) * BLOCK_SIZE,
                                 (current_tetrimino.y + y) * BLOCK_SIZE,
                                 BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw sidebar content
    sidebar_x = SCREEN_WIDTH + 20

    # Draw next piece preview
    font = pygame.font.SysFont('Arial', 24)
    next_text = font.render("NEXT", True, theme['text'])
    screen.blit(next_text, (sidebar_x, 20))

    # Draw next piece box
    preview_box_size = 120
    preview_box_x = sidebar_x
    preview_box_y = 50
    pygame.draw.rect(screen, theme['background'],
                    (preview_box_x, preview_box_y, preview_box_size, preview_box_size))
    pygame.draw.rect(screen, theme['ui_accent'],
                    (preview_box_x, preview_box_y, preview_box_size, preview_box_size), 2)

    # Draw next piece
    next_block_size = 25  # Smaller blocks for preview
    next_shape = next_tetrimino.shape
    next_color = next_tetrimino.color

    # Center the piece in the preview box
    next_offset_x = preview_box_x + (preview_box_size - len(next_shape[0]) * next_block_size) // 2
    next_offset_y = preview_box_y + (preview_box_size - len(next_shape) * next_block_size) // 2

    for y, row in enumerate(next_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_color,
                                (next_offset_x + x * next_block_size,
                                 next_offset_y + y * next_block_size,
                                 next_block_size, next_block_size))
                pygame.draw.rect(screen, theme['text'],
                                (next_offset_x + x * next_block_size,
                                 next_offset_y + y * next_block_size,
                                 next_block_size, next_block_size), 1)

    # Draw hold piece if available
    hold_text = font.render("HOLD", True, theme['text'])
    screen.blit(hold_text, (sidebar_x, 190))

    # Draw hold piece box
    hold_box_x = sidebar_x
    hold_box_y = 220
    pygame.draw.rect(screen, theme['background'],
                    (hold_box_x, hold_box_y, preview_box_size, preview_box_size))

    # Draw box with different color based on whether hold is available
    if st.session_state.can_hold:
        pygame.draw.rect(screen, theme['ui_accent'],
                        (hold_box_x, hold_box_y, preview_box_size, preview_box_size), 2)
    else:
        pygame.draw.rect(screen, (100, 100, 100),
                        (hold_box_x, hold_box_y, preview_box_size, preview_box_size), 2)

    # Draw held piece if any
    if st.session_state.held_piece is not None:
        held_shape = SHAPES[st.session_state.held_piece]
        held_color = theme['piece_colors'][st.session_state.held_piece]

        # Center the piece in the hold box
        held_offset_x = hold_box_x + (preview_box_size - len(held_shape[0]) * next_block_size) // 2
        held_offset_y = hold_box_y + (preview_box_size - len(held_shape) * next_block_size) // 2

        for y, row in enumerate(held_shape):
            for x, cell in enumerate(row):
                if cell:
                    # Draw with reduced opacity if can't hold
                    if st.session_state.can_hold:
                        pygame.draw.rect(screen, held_color,
                                        (held_offset_x + x * next_block_size,
                                         held_offset_y + y * next_block_size,
                                         next_block_size, next_block_size))
                    else:
                        # Draw grayed out
                        s = pygame.Surface((next_block_size, next_block_size), pygame.SRCALPHA)
                        s.fill((*held_color[:3], 128))  # Semi-transparent
                        screen.blit(s, (held_offset_x + x * next_block_size,
                                       held_offset_y + y * next_block_size))

                    pygame.draw.rect(screen, theme['text'],
                                    (held_offset_x + x * next_block_size,
                                     held_offset_y + y * next_block_size,
                                     next_block_size, next_block_size), 1)

    # Draw score and stats
    stats_y = 360
    score_text = font.render(f"SCORE", True, theme['text'])
    score_value = font.render(f"{score}", True, theme['ui_accent'])
    screen.blit(score_text, (sidebar_x, stats_y))
    screen.blit(score_value, (sidebar_x, stats_y + 30))

    level_text = font.render(f"LEVEL", True, theme['text'])
    level_value = font.render(f"{level}", True, theme['ui_accent'])
    screen.blit(level_text, (sidebar_x, stats_y + 70))
    screen.blit(level_value, (sidebar_x, stats_y + 100))

    lines_text = font.render(f"LINES", True, theme['text'])
    lines_value = font.render(f"{lines_cleared}", True, theme['ui_accent'])
    screen.blit(lines_text, (sidebar_x, stats_y + 140))
    screen.blit(lines_value, (sidebar_x, stats_y + 170))

    high_score_text = font.render(f"HIGH", True, theme['text'])
    high_score_value = font.render(f"{high_score}", True, theme['ui_accent'])
    screen.blit(high_score_text, (sidebar_x, stats_y + 210))
    screen.blit(high_score_value, (sidebar_x, stats_y + 240))

    # Draw pause overlay if game is paused
    if st.session_state.paused:
        # Semi-transparent overlay
        s = pygame.Surface((FULL_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  # Black with alpha
        screen.blit(s, (0, 0))

        # Pause text
        pause_font = pygame.font.SysFont('Arial', 48)
        pause_text = pause_font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(FULL_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, text_rect)

        # Instructions
        inst_font = pygame.font.SysFont('Arial', 24)
        inst_text = inst_font.render("Press Resume to continue", True, WHITE)
        inst_rect = inst_text.get_rect(center=(FULL_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(inst_text, inst_rect)

    # Convert to PIL image
    img = pygame_to_image(screen)
    return img

def game_step(grid, current_tetrimino, next_tetrimino, score, level, lines_cleared):
    """Perform one step of the game logic"""
    # If game is paused, don't update
    if st.session_state.paused:
        return grid, current_tetrimino, next_tetrimino, score, level, lines_cleared, False

    # Move piece down
    current_tetrimino.y += 1

    # Check for collision
    if check_collision(grid, current_tetrimino):
        current_tetrimino.y -= 1
        grid = lock_tetrimino(grid, current_tetrimino)

        # Update game stats
        st.session_state.game_stats['pieces_placed'] += 1

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

        # Update stats
        update_stats(score, level, lines_cleared)

        # Get next piece
        current_tetrimino = next_tetrimino
        next_tetrimino = Tetrimino()

        # Reset hold ability
        st.session_state.can_hold = True

        # Check if game is over
        game_over = check_collision(grid, current_tetrimino)

        return grid, current_tetrimino, next_tetrimino, score, level, lines_cleared, game_over

    return grid, current_tetrimino, next_tetrimino, score, level, lines_cleared, False

def handle_keyboard_input(key, grid, current_tetrimino):
    """Handle keyboard input for game controls"""
    # If game is paused, only respond to pause/unpause
    if st.session_state.paused and key != 'pause':
        return grid, current_tetrimino

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

    elif key == 'up' or key == 'rotate_cw':
        original_shape = current_tetrimino.rotate(clockwise=True)
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
                current_tetrimino.rotation = (current_tetrimino.rotation - 1) % 4

    elif key == 'rotate_ccw':
        original_shape = current_tetrimino.rotate(clockwise=False)
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
                current_tetrimino.rotation = (current_tetrimino.rotation + 1) % 4

    elif key == 'space':
        # Hard drop
        while not check_collision(grid, current_tetrimino):
            current_tetrimino.y += 1
        current_tetrimino.y -= 1  # Move back up to valid position

    elif key == 'hold':
        # Hold the current piece
        if st.session_state.can_hold:
            new_piece = hold_piece()
            if new_piece:
                current_tetrimino = new_piece

    elif key == 'pause':
        # Toggle pause state
        st.session_state.paused = not st.session_state.paused

    elif key == 'toggle_ghost':
        # Toggle ghost piece
        st.session_state.show_ghost = not st.session_state.show_ghost

    return grid, current_tetrimino

def start_game():
    """Initialize a new game"""
    # Update game stats
    if st.session_state.game_state == 'playing':
        st.session_state.game_stats['games_played'] += 1

    # Reset game state
    st.session_state.grid = create_grid()
    st.session_state.current_tetrimino = Tetrimino()
    st.session_state.next_tetrimino = Tetrimino()
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.lines_cleared = 0
    st.session_state.game_state = 'playing'
    st.session_state.last_update = time.time()
    st.session_state.game_start_time = time.time()
    st.session_state.paused = False
    st.session_state.held_piece = None
    st.session_state.can_hold = True

def restart_game():
    """Restart the game"""
    # Update game stats
    st.session_state.game_stats['games_played'] += 1

    # Save current game time
    if 'game_start_time' in st.session_state:
        play_time = time.time() - st.session_state.game_start_time
        st.session_state.game_stats['total_play_time'] += play_time

    start_game()

def toggle_theme():
    """Cycle through available themes"""
    themes = list(THEMES.keys())
    current_idx = themes.index(st.session_state.theme)
    next_idx = (current_idx + 1) % len(themes)
    st.session_state.theme = themes[next_idx]

def toggle_sound():
    """Toggle sound effects on/off"""
    st.session_state.sound_enabled = not st.session_state.sound_enabled

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