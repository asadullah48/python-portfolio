import pygame
import random
import json
import os
from pathlib import Path

pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 500  # Increased to accommodate next piece preview
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 300
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
COLS = GRID_WIDTH // BLOCK_SIZE
BORDER_WIDTH = 4

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
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)

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

# Game settings
BASE_FALL_SPEED = 1000  # in milliseconds
LEVEL_SPEED_DECREASE = 100  # speed up per level

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Load or create high score file
def get_high_score():
    high_score_file = Path("tetris_high_score.json")
    if high_score_file.exists():
        try:
            with open(high_score_file, "r") as f:
                return json.load(f)
        except:
            return 0
    return 0

def save_high_score(score):
    high_score = get_high_score()
    if score > high_score:
        with open("tetris_high_score.json", "w") as f:
            json.dump(score, f)
        return True
    return False

# Load sound effects
try:
    rotate_sound = pygame.mixer.Sound("rotate.wav")
    clear_sound = pygame.mixer.Sound("clear.wav")
    drop_sound = pygame.mixer.Sound("drop.wav")
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    level_up_sound = pygame.mixer.Sound("level_up.wav")
except:
    # If sounds can't be loaded, create silent sounds
    rotate_sound = pygame.mixer.Sound(buffer=bytearray(100))
    clear_sound = pygame.mixer.Sound(buffer=bytearray(100))
    drop_sound = pygame.mixer.Sound(buffer=bytearray(100))
    game_over_sound = pygame.mixer.Sound(buffer=bytearray(100))
    level_up_sound = pygame.mixer.Sound(buffer=bytearray(100))

class Tetrimino:
    def __init__(self, shape=None, color=None):
        if shape is None:
            shape_idx = random.randint(0, len(SHAPES) - 1)
            self.shape = SHAPES[shape_idx]
            self.color = COLORS[shape_idx]
        else:
            self.shape = shape
            self.color = color if color else random.choice(COLORS)
        
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
    
    if lines_cleared > 0:
        clear_sound.play()
    
    return lines_cleared

def calculate_score(lines_cleared, level):
    # Score calculation: lines cleared * level * 100
    # Bonus for multiple lines cleared
    if lines_cleared == 1:
        return 100 * level
    elif lines_cleared == 2:
        return 300 * level
    elif lines_cleared == 3:
        return 500 * level
    elif lines_cleared == 4:
        return 800 * level  # Tetris!
    return 0

def draw_grid_border():
    border_rect = pygame.Rect(0, 0, GRID_WIDTH + BORDER_WIDTH * 2, SCREEN_HEIGHT)
    pygame.draw.rect(screen, WHITE, border_rect, BORDER_WIDTH)

def draw_next_piece(next_piece):
    # Draw next piece preview box
    preview_x = GRID_WIDTH + BLOCK_SIZE
    preview_y = BLOCK_SIZE * 5
    preview_width = BLOCK_SIZE * 5
    preview_height = BLOCK_SIZE * 5
    
    # Draw box
    preview_rect = pygame.Rect(preview_x, preview_y, preview_width, preview_height)
    pygame.draw.rect(screen, DARK_GRAY, preview_rect)
    pygame.draw.rect(screen, WHITE, preview_rect, 2)
    
    # Draw "Next" text
    font = pygame.font.SysFont('Arial', 24)
    next_text = font.render("Next", True, WHITE)
    screen.blit(next_text, (preview_x + 10, preview_y - 30))
    
    # Draw the next piece
    shape_width = len(next_piece.shape[0])
    shape_height = len(next_piece.shape)
    
    # Calculate center position
    center_x = preview_x + (preview_width - shape_width * BLOCK_SIZE) // 2
    center_y = preview_y + (preview_height - shape_height * BLOCK_SIZE) // 2
    
    for y, row in enumerate(next_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_piece.color, 
                                (center_x + x * BLOCK_SIZE, 
                                 center_y + y * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, 
                                (center_x + x * BLOCK_SIZE, 
                                 center_y + y * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_screen(grid, score, level, lines_cleared, high_score, next_piece=None, paused=False):
    screen.fill(BLACK)
    
    # Draw grid border
    draw_grid_border()
    
    # Draw grid and current tetrimino
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], 
                           (x * BLOCK_SIZE + BORDER_WIDTH, 
                            y * BLOCK_SIZE + BORDER_WIDTH, 
                            BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, DARK_GRAY, 
                           (x * BLOCK_SIZE + BORDER_WIDTH, 
                            y * BLOCK_SIZE + BORDER_WIDTH, 
                            BLOCK_SIZE, BLOCK_SIZE), 1)
    
    # Draw next piece preview
    if next_piece:
        draw_next_piece(next_piece)
    
    # Draw score information
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lines_text = font.render(f"Lines: {lines_cleared}", True, WHITE)
    
    # Draw statistics on right side
    stats_x = GRID_WIDTH + BLOCK_SIZE
    screen.blit(score_text, (stats_x, BLOCK_SIZE))
    screen.blit(high_score_text, (stats_x, BLOCK_SIZE * 2))
    screen.blit(level_text, (stats_x, BLOCK_SIZE * 3))
    screen.blit(lines_text, (stats_x, BLOCK_SIZE * 4))
    
    # Draw controls help
    controls_font = pygame.font.SysFont('Arial', 16)
    controls_text = [
        "Controls:",
        "← → : Move",
        "↑ : Rotate",
        "↓ : Soft Drop",
        "Space : Hard Drop",
        "P : Pause"
    ]
    
    for i, text in enumerate(controls_text):
        rendered_text = controls_font.render(text, True, WHITE)
        screen.blit(rendered_text, (stats_x, BLOCK_SIZE * 11 + i * 20))
    
    # Draw pause overlay if paused
    if paused:
        pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(pause_overlay, (0, 0))
        
        pause_font = pygame.font.SysFont('Arial', 36)
        pause_text = pause_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, pause_rect)
        
        continue_font = pygame.font.SysFont('Arial', 24)
        continue_text = continue_font.render("Press P to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(continue_text, continue_rect)
    
    pygame.display.update()

def show_game_over(score, high_score, new_high_score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont('Arial', 48)
    font_medium = pygame.font.SysFont('Arial', 32)
    font_small = pygame.font.SysFont('Arial', 24)
    
    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    
    if new_high_score:
        high_score_text = font_medium.render(f"NEW HIGH SCORE: {high_score}", True, YELLOW)
    else:
        high_score_text = font_medium.render(f"High Score: {high_score}", True, WHITE)
    
    restart_text = font_small.render("Press R to restart", True, WHITE)
    quit_text = font_small.render("Press Q to quit", True, WHITE)
    
    screen.blit(game_over_text, 
               (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                SCREEN_HEIGHT // 3))
    screen.blit(score_text, 
               (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 60))
    screen.blit(high_score_text, 
               (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 100))
    screen.blit(restart_text, 
               (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 160))
    screen.blit(quit_text, 
               (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 190))
    
    pygame.display.update()

def hard_drop(grid, tetrimino):
    original_y = tetrimino.y
    
    # Drop as far as possible
    while not check_collision(grid, tetrimino):
        tetrimino.y += 1
    
    # Move back up one step (to valid position)
    tetrimino.y -= 1
    
    # Calculate drop distance for score
    drop_distance = tetrimino.y - original_y
    
    # Play sound for hard drop
    drop_sound.play()
    
    return drop_distance

def game():
    grid = create_grid()
    score = 0
    level = 1
    total_lines_cleared = 0
    high_score = get_high_score()
    
    clock = pygame.time.Clock()
    current_tetrimino = Tetrimino()
    next_tetrimino = Tetrimino()
    
    # Game state variables
    fall_time = 0
    fall_speed = BASE_FALL_SPEED
    paused = False
    game_over = False
    new_high_score = False
    
    # Main game loop
    running = True
    while running:
        # Reset fall time and get rawtime
        delta_time = clock.get_rawtime()
        clock.tick()
        
        # Handle game over state
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        return True  # Signal to restart
                    if event.key == pygame.K_q:  # Quit game
                        return False  # Signal to quit
            
            show_game_over(score, high_score, new_high_score)
            continue
        
        # Handle pause state
        if paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
            
            draw_screen(grid, score, level, total_lines_cleared, high_score, next_tetrimino, paused)
            continue
        
        # Normal gameplay
        if not paused and not game_over:
            fall_time += delta_time
            
            # Handle piece falling
            if fall_time >= fall_speed:
                fall_time = 0
                current_tetrimino.y += 1
                if check_collision(grid, current_tetrimino):
                    current_tetrimino.y -= 1
                    grid = lock_tetrimino(grid, current_tetrimino)
                    
                    # Check for cleared lines
                    lines_cleared = clear_lines(grid)
                    total_lines_cleared += lines_cleared
                    
                    # Update score
                    if lines_cleared > 0:
                        score += calculate_score(lines_cleared, level)
                    
                    # Check for level up (every 10 lines)
                    if total_lines_cleared // 10 + 1 > level:
                        level = total_lines_cleared // 10 + 1
                        fall_speed = max(100, BASE_FALL_SPEED - (level - 1) * LEVEL_SPEED_DECREASE)
                        level_up_sound.play()
                    
                    # Get next piece
                    current_tetrimino = next_tetrimino
                    next_tetrimino = Tetrimino()
                    
                    # Check if game is over
                    if check_collision(grid, current_tetrimino):
                        game_over = True
                        game_over_sound.play()
                        
                        # Check for new high score
                        if score > high_score:
                            new_high_score = save_high_score(score)
                            high_score = score
            
            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_tetrimino.x -= 1
                        if check_collision(grid, current_tetrimino):
                            current_tetrimino.x += 1
                    
                    elif event.key == pygame.K_RIGHT:
                        current_tetrimino.x += 1
                        if check_collision(grid, current_tetrimino):
                            current_tetrimino.x -= 1
                    
                    elif event.key == pygame.K_DOWN:
                        current_tetrimino.y += 1
                        if check_collision(grid, current_tetrimino):
                            current_tetrimino.y -= 1
                    
                    elif event.key == pygame.K_UP:
                        original_shape = [row[:] for row in current_tetrimino.shape]
                        current_tetrimino.rotate()
                        if check_collision(grid, current_tetrimino):
                            # Try to adjust position to make rotation work
                            original_x = current_tetrimino.x
                            
                            # Try moving left or right to fit
                            for adjust in [-1, 1, -2, 2]:
                                current_tetrimino.x += adjust
                                if not check_collision(grid, current_tetrimino):
                                    rotate_sound.play()
                                    break
                                current_tetrimino.x = original_x
                            else:
                                # If no position works, revert the rotation
                                current_tetrimino.shape = original_shape
                        else:
                            rotate_sound.play()
                    
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        drop_distance = hard_drop(grid, current_tetrimino)
                        score += drop_distance  # Add score for hard drop
                        grid = lock_tetrimino(grid, current_tetrimino)
                        
                        # Check for cleared lines
                        lines_cleared = clear_lines(grid)
                        total_lines_cleared += lines_cleared
                        
                        # Update score
                        if lines_cleared > 0:
                            score += calculate_score(lines_cleared, level)
                        
                        # Check for level up
                        if total_lines_cleared // 10 + 1 > level:
                            level = total_lines_cleared // 10 + 1
                            fall_speed = max(100, BASE_FALL_SPEED - (level - 1) * LEVEL_SPEED_DECREASE)
                            level_up_sound.play()
                        
                        # Get next piece
                        current_tetrimino = next_tetrimino
                        next_tetrimino = Tetrimino()
                        
                        # Check if game is over
                        if check_collision(grid, current_tetrimino):
                            game_over = True
                            game_over_sound.play()
                            
                            # Check for new high score
                            if score > high_score:
                                new_high_score = save_high_score(score)
                                high_score = score
                    
                    elif event.key == pygame.K_p:
                        paused = True
            
            # Draw next frame
            draw_screen(grid, score, level, total_lines_cleared, high_score, next_tetrimino)
            
            # Draw current tetrimino
            for y, row in enumerate(current_tetrimino.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, current_tetrimino.color, 
                                       ((current_tetrimino.x + x) * BLOCK_SIZE + BORDER_WIDTH, 
                                        (current_tetrimino.y + y) * BLOCK_SIZE + BORDER_WIDTH, 
                                        BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(screen, WHITE, 
                                       ((current_tetrimino.x + x) * BLOCK_SIZE + BORDER_WIDTH, 
                                        (current_tetrimino.y + y) * BLOCK_SIZE + BORDER_WIDTH, 
                                        BLOCK_SIZE, BLOCK_SIZE), 1)
            
            pygame.display.update()
    
    pygame.quit()
    return False

def main():
    restart = True
    while restart:
        restart = game()

if __name__ == "__main__":
    main()