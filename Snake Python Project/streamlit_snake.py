import streamlit as st
import pygame
import numpy as np
import time
from PIL import Image
import io
import random
import json
import os
import base64
from datetime import datetime

# Set up the page configuration
st.set_page_config(
    page_title="Snake Game by Asadullah",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Game Constants
BLOCK_SIZE = 20
FPS_OPTIONS = {"Easy": 5, "Medium": 7, "Hard": 10}
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = BLOCK_SIZE * GRID_WIDTH
HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
PURPLE = (128, 0, 128)

# Load assets
def load_image(file_path):
    if os.path.exists(file_path):
        return Image.open(file_path)
    return None

# Load CSS
def load_css(file_path):
    with open(file_path, "r") as f:
        return f.read()

# Apply CSS if style file exists
if os.path.exists("assets/style.css"):
    st.markdown(f"<style>{load_css('assets/style.css')}</style>", unsafe_allow_html=True)

# Load background image
def get_base64_encoded_image(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set background image if it exists
bg_image = get_base64_encoded_image("assets/snake_bg.png")
if bg_image:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state variables if not already set
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.snake_positions = [(GRID_WIDTH // 4, GRID_HEIGHT // 2),
                                      (GRID_WIDTH // 4 - 1, GRID_HEIGHT // 2),
                                      (GRID_WIDTH // 4 - 2, GRID_HEIGHT // 2)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food_position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.high_scores = {"Easy": 0, "Medium": 0, "Hard": 0}
    st.session_state.difficulty = "Medium"
    st.session_state.special_food = False
    st.session_state.theme = "Classic"
    st.session_state.leaderboard = []
    st.session_state.countdown = 0
    st.session_state.power_up = None
    st.session_state.power_up_active = False
    st.session_state.power_up_timer = 0
    st.session_state.game_start_time = None

def reset_game():
    st.session_state.game_active = True
    st.session_state.snake_positions = [(GRID_WIDTH // 4, GRID_HEIGHT // 2),
                                      (GRID_WIDTH // 4 - 1, GRID_HEIGHT // 2),
                                      (GRID_WIDTH // 4 - 2, GRID_HEIGHT // 2)]
    st.session_state.direction = 'RIGHT'
    place_food()
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.countdown = 3  # 3 second countdown before game starts
    st.session_state.power_up = None
    st.session_state.power_up_active = False
    st.session_state.power_up_timer = 0
    st.session_state.game_start_time = datetime.now()

def place_food():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in st.session_state.snake_positions:
            st.session_state.food_position = (x, y)

            # Determine food type
            food_chance = random.random()
            if food_chance < 0.2:  # 20% chance for special food
                st.session_state.special_food = True
            else:
                st.session_state.special_food = False

            # Chance for power-up to appear (10% chance, only if not special food)
            if not st.session_state.special_food and random.random() < 0.1 and not st.session_state.power_up_active:
                power_ups = ["speed", "shield", "double_points"]
                st.session_state.power_up = random.choice(power_ups)
                st.session_state.power_up_position = (x, y)
            break

def move_snake():
    # Handle countdown
    if st.session_state.countdown > 0:
        st.session_state.countdown -= 1
        return

    if st.session_state.game_over:
        return

    # Handle power-up timer
    if st.session_state.power_up_active:
        st.session_state.power_up_timer -= 1
        if st.session_state.power_up_timer <= 0:
            st.session_state.power_up_active = False
            st.session_state.power_up = None

    head_x, head_y = st.session_state.snake_positions[0]

    # Determine new head position based on direction
    if st.session_state.direction == 'UP':
        new_head = (head_x, head_y - 1)
    elif st.session_state.direction == 'DOWN':
        new_head = (head_x, head_y + 1)
    elif st.session_state.direction == 'LEFT':
        new_head = (head_x - 1, head_y)
    elif st.session_state.direction == 'RIGHT':
        new_head = (head_x + 1, head_y)

    # Check for collision with walls or self
    collision = (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in st.session_state.snake_positions)

    # Shield power-up prevents one collision
    if collision and st.session_state.power_up_active and st.session_state.power_up == "shield":
        # Deactivate shield after use
        st.session_state.power_up_active = False
        st.session_state.power_up = None

        # Wrap around instead of collision
        if new_head[0] < 0:
            new_head = (GRID_WIDTH - 1, new_head[1])
        elif new_head[0] >= GRID_WIDTH:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], GRID_HEIGHT - 1)
        elif new_head[1] >= GRID_HEIGHT:
            new_head = (new_head[0], 0)
        elif new_head in st.session_state.snake_positions:
            # If self-collision, just continue (one-time immunity)
            pass

        collision = False

    if collision:
        st.session_state.game_over = True

        # Update high score if needed
        if st.session_state.score > st.session_state.high_scores[st.session_state.difficulty]:
            st.session_state.high_scores[st.session_state.difficulty] = st.session_state.score

            # Add to leaderboard
            st.session_state.leaderboard.append({
                "score": st.session_state.score,
                "difficulty": st.session_state.difficulty,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            # Sort leaderboard by score (descending)
            st.session_state.leaderboard = sorted(
                st.session_state.leaderboard,
                key=lambda x: x["score"],
                reverse=True
            )[:10]  # Keep only top 10

        return

    # Add new head
    st.session_state.snake_positions.insert(0, new_head)

    # Check for food collision
    if new_head == st.session_state.food_position:
        # Calculate points based on power-ups
        points = 1
        if st.session_state.special_food:
            points = 3

        # Double points power-up
        if st.session_state.power_up_active and st.session_state.power_up == "double_points":
            points *= 2

        st.session_state.score += points
        place_food()
    else:
        # Remove tail if no food was eaten
        st.session_state.snake_positions.pop()

    # Check for power-up collision
    if hasattr(st.session_state, 'power_up_position') and new_head == st.session_state.power_up_position:
        # Activate power-up
        st.session_state.power_up_active = True
        st.session_state.power_up_timer = 20  # Power-up lasts for 20 moves

        # Remove power-up from board
        st.session_state.power_up_position = None

def render_game(pygame_surface):
    # Fill background with a gradient
    for y in range(HEIGHT):
        # Create a gradient from dark to slightly lighter
        color_value = 20 + int(y / HEIGHT * 20)
        pygame.draw.line(pygame_surface, (color_value, color_value, color_value), (0, y), (WIDTH, y))

    # Draw grid with subtle lines
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(pygame_surface, (60, 60, 60), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(pygame_surface, (60, 60, 60), (0, y), (WIDTH, y))

    # Draw border
    pygame.draw.rect(pygame_surface, (80, 80, 80), (0, 0, WIDTH, HEIGHT), 3)

    # Draw power-up if active
    if hasattr(st.session_state, 'power_up_position') and st.session_state.power_up_position:
        power_x, power_y = st.session_state.power_up_position

        # Different colors for different power-ups
        if st.session_state.power_up == "speed":
            power_color = BLUE
        elif st.session_state.power_up == "shield":
            power_color = PURPLE
        elif st.session_state.power_up == "double_points":
            power_color = (255, 165, 0)  # Orange

        # Draw power-up as a diamond shape
        center_x = power_x * BLOCK_SIZE + BLOCK_SIZE // 2
        center_y = power_y * BLOCK_SIZE + BLOCK_SIZE // 2
        size = BLOCK_SIZE // 2

        points = [
            (center_x, center_y - size),  # Top
            (center_x + size, center_y),  # Right
            (center_x, center_y + size),  # Bottom
            (center_x - size, center_y)   # Left
        ]

        pygame.draw.polygon(pygame_surface, power_color, points)

        # Add pulsing effect
        pulse = abs(int(time.time() * 5) % 10 - 5) / 5  # Value between 0 and 1
        inner_size = int(size * (0.6 + 0.4 * pulse))

        inner_points = [
            (center_x, center_y - inner_size),
            (center_x + inner_size, center_y),
            (center_x, center_y + inner_size),
            (center_x - inner_size, center_y)
        ]

        pygame.draw.polygon(pygame_surface, (255, 255, 255), inner_points)

    # Draw snake with improved visuals
    for i, position in enumerate(st.session_state.snake_positions):
        x, y = position

        if i == 0:  # Head
            # Draw head with eyes
            pygame.draw.rect(pygame_surface, DARK_GREEN, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(pygame_surface, GREEN, (x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

            # Add eyes based on direction
            eye_radius = BLOCK_SIZE // 6
            eye_offset = BLOCK_SIZE // 4

            # Base eye positions
            left_eye_x = x * BLOCK_SIZE + eye_offset
            right_eye_x = x * BLOCK_SIZE + BLOCK_SIZE - eye_offset
            eye_y = y * BLOCK_SIZE + eye_offset

            # Adjust eye positions based on direction
            if st.session_state.direction == 'UP':
                pass  # Default position is good for up
            elif st.session_state.direction == 'DOWN':
                eye_y = y * BLOCK_SIZE + BLOCK_SIZE - eye_offset
            elif st.session_state.direction == 'LEFT':
                left_eye_x = x * BLOCK_SIZE + eye_offset
                right_eye_x = x * BLOCK_SIZE + 2 * eye_offset
                eye_y = y * BLOCK_SIZE + BLOCK_SIZE // 2
            elif st.session_state.direction == 'RIGHT':
                left_eye_x = x * BLOCK_SIZE + BLOCK_SIZE - 2 * eye_offset
                right_eye_x = x * BLOCK_SIZE + BLOCK_SIZE - eye_offset
                eye_y = y * BLOCK_SIZE + BLOCK_SIZE // 2

            # Draw eyes
            pygame.draw.circle(pygame_surface, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(pygame_surface, WHITE, (right_eye_x, eye_y), eye_radius)

            # Draw pupils
            pygame.draw.circle(pygame_surface, BLACK, (left_eye_x, eye_y), eye_radius // 2)
            pygame.draw.circle(pygame_surface, BLACK, (right_eye_x, eye_y), eye_radius // 2)

        else:  # Body
            # Draw body segments with gradient effect
            color_intensity = max(100, 255 - i * 5)  # Gradually decrease intensity
            body_color = (0, color_intensity, 0)
            border_color = (0, max(50, color_intensity - 50), 0)

            pygame.draw.rect(pygame_surface, border_color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(pygame_surface, body_color, (x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

    # Draw food with improved visuals
    food_x, food_y = st.session_state.food_position

    if st.session_state.special_food:
        # Golden food (special)
        pygame.draw.circle(pygame_surface, YELLOW,
                          (food_x * BLOCK_SIZE + BLOCK_SIZE // 2, food_y * BLOCK_SIZE + BLOCK_SIZE // 2),
                          BLOCK_SIZE // 2)

        # Add shine effect
        shine_radius = BLOCK_SIZE // 4
        shine_x = food_x * BLOCK_SIZE + BLOCK_SIZE // 3
        shine_y = food_y * BLOCK_SIZE + BLOCK_SIZE // 3
        pygame.draw.circle(pygame_surface, WHITE, (shine_x, shine_y), shine_radius // 2)
    else:
        # Regular food (apple-like)
        pygame.draw.circle(pygame_surface, RED,
                          (food_x * BLOCK_SIZE + BLOCK_SIZE // 2, food_y * BLOCK_SIZE + BLOCK_SIZE // 2),
                          BLOCK_SIZE // 2)

        # Add stem
        stem_width = BLOCK_SIZE // 8
        stem_height = BLOCK_SIZE // 3
        stem_x = food_x * BLOCK_SIZE + BLOCK_SIZE // 2 - stem_width // 2
        stem_y = food_y * BLOCK_SIZE + BLOCK_SIZE // 4 - stem_height // 2
        pygame.draw.rect(pygame_surface, (101, 67, 33), (stem_x, stem_y, stem_width, stem_height))

    # Draw countdown if active
    if st.session_state.countdown > 0:
        font = pygame.font.SysFont("Arial", 72, bold=True)
        countdown_text = font.render(str(st.session_state.countdown), True, WHITE)
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame_surface.blit(countdown_text, text_rect)

    # Draw active power-up indicator
    if st.session_state.power_up_active:
        power_up_names = {
            "speed": "Speed Boost",
            "shield": "Shield",
            "double_points": "Double Points"
        }

        power_up_colors = {
            "speed": BLUE,
            "shield": PURPLE,
            "double_points": (255, 165, 0)  # Orange
        }

        font = pygame.font.SysFont("Arial", 18)
        power_text = font.render(f"{power_up_names[st.session_state.power_up]}: {st.session_state.power_up_timer}", True, power_up_colors[st.session_state.power_up])
        pygame_surface.blit(power_text, (WIDTH - power_text.get_width() - 10, 10))

    # Draw score
    font = pygame.font.SysFont("Arial", 24, bold=True)
    score_text = font.render(f"Score: {st.session_state.score}", True, WHITE)
    pygame_surface.blit(score_text, (10, 10))

    # Draw difficulty
    diff_text = font.render(f"Difficulty: {st.session_state.difficulty}", True, WHITE)
    pygame_surface.blit(diff_text, (10, 40))

    return pygame_surface

def pygame_to_image(pygame_surface):
    # Convert Pygame surface to PIL Image
    raw_str = pygame.image.tostring(pygame_surface, 'RGB')
    return Image.frombytes('RGB', pygame_surface.get_size(), raw_str)

def main():
    # Custom title with styling
    st.markdown('<h1 class="game-title">🐍 Snake Game Pro</h1>', unsafe_allow_html=True)

    # Instructions with better styling
    with st.expander("📖 How to Play"):
        st.markdown("""
        <div class="instructions">
        <h3>Game Controls</h3>
        <ul>
            <li>Use the direction buttons or keyboard arrows to control the snake.</li>
            <li>Eat regular food (red apples) to grow longer and earn 1 point.</li>
            <li>Golden apples are special and worth 3 points!</li>
            <li>Collect power-ups for special abilities:
                <ul>
                    <li>🔵 <b>Speed Boost</b>: Temporarily increases snake speed</li>
                    <li>🟣 <b>Shield</b>: Protects from one collision</li>
                    <li>🟠 <b>Double Points</b>: Doubles points for a limited time</li>
                </ul>
            </li>
            <li>Avoid hitting the walls or yourself.</li>
            <li>Select difficulty level to change the game speed.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Game area with improved layout
    col1, col2, col3 = st.columns([1, 3, 1])

    # Sidebar with better styling
    with st.sidebar:
        st.markdown('<h2 style="color:#4CAF50;">Game Settings</h2>', unsafe_allow_html=True)

        # Theme selection
        themes = ["Classic", "Neon", "Retro", "Dark"]
        st.session_state.theme = st.selectbox("Select Theme",
                                            themes,
                                            index=themes.index(st.session_state.theme) if st.session_state.theme in themes else 0)

        # Difficulty selection with better styling
        st.markdown('<div class="difficulty-selector">', unsafe_allow_html=True)
        st.session_state.difficulty = st.selectbox("Select Difficulty",
                                                 ["Easy", "Medium", "Hard"],
                                                 index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty))
        st.markdown('</div>', unsafe_allow_html=True)

        # Start/Reset button with better styling
        if st.button("Start/Reset Game", key="start_button", use_container_width=True):
            reset_game()

        # High scores with better styling
        st.markdown('<h2 style="color:#FFD700;">High Scores</h2>', unsafe_allow_html=True)
        for diff, score in st.session_state.high_scores.items():
            st.markdown(f'<div style="background-color:#333; padding:5px 10px; margin:2px 0; border-radius:5px;">{diff}: <b>{score}</b></div>', unsafe_allow_html=True)

        # Leaderboard
        if st.session_state.leaderboard:
            st.markdown('<h2 style="color:#4CAF50;">Leaderboard</h2>', unsafe_allow_html=True)
            for i, entry in enumerate(st.session_state.leaderboard[:5]):  # Show top 5
                st.markdown(f'<div style="background-color:#333; padding:5px 10px; margin:2px 0; border-radius:5px;">{i+1}. <b>{entry["score"]}</b> ({entry["difficulty"]}) - {entry["date"]}</div>', unsafe_allow_html=True)

    # Control buttons with better styling
    with col1:
        st.markdown('<h3 style="text-align:center; color:#4CAF50;">Controls</h3>', unsafe_allow_html=True)

        # Up button
        st.markdown('<div style="display:flex; justify-content:center;">', unsafe_allow_html=True)
        if st.button("⬆️", key="up", use_container_width=True):
            if st.session_state.direction != 'DOWN':
                st.session_state.direction = 'UP'
        st.markdown('</div>', unsafe_allow_html=True)

        # Left, Space, Right buttons in a row
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            if st.button("⬅️", key="left", use_container_width=True):
                if st.session_state.direction != 'RIGHT':
                    st.session_state.direction = 'LEFT'

        # Middle button (pause/resume)
        with col1_2:
            if st.button("⏸️", key="pause", use_container_width=True):
                st.session_state.game_active = not st.session_state.game_active

        with col1_3:
            if st.button("➡️", key="right", use_container_width=True):
                if st.session_state.direction != 'LEFT':
                    st.session_state.direction = 'RIGHT'

        # Down button
        st.markdown('<div style="display:flex; justify-content:center;">', unsafe_allow_html=True)
        if st.button("⬇️", key="down", use_container_width=True):
            if st.session_state.direction != 'UP':
                st.session_state.direction = 'DOWN'
        st.markdown('</div>', unsafe_allow_html=True)

        # Game stats with better styling
        st.markdown('<div class="score-display">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:#4CAF50; margin:0;">Score: {st.session_state.score}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="margin:5px 0;">Difficulty: {st.session_state.difficulty}</p>', unsafe_allow_html=True)

        # Show active power-up
        if st.session_state.power_up_active:
            power_up_names = {
                "speed": "Speed Boost 🔵",
                "shield": "Shield 🟣",
                "double_points": "Double Points 🟠"
            }
            st.markdown(f'<p style="color:#FFD700; margin:5px 0;">Active: {power_up_names[st.session_state.power_up]}</p>', unsafe_allow_html=True)

        # Game status
        if st.session_state.game_active:
            if st.session_state.countdown > 0:
                st.markdown(f'<p style="color:#2196F3; margin:5px 0;">Starting in: {st.session_state.countdown}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#4CAF50; margin:5px 0;">Game Status: Active</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#FF5252; margin:5px 0;">Game Status: Paused</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Keyboard controls info
        st.markdown("""
        <div style="background-color:#333; padding:10px; border-radius:5px; margin-top:10px; font-size:12px;">
        <p style="margin:0; text-align:center;">You can also use keyboard arrows!</p>
        <p style="margin:0; text-align:center;">Press 'P' to pause/resume</p>
        </div>
        """, unsafe_allow_html=True)

    # Game display with better styling
    with col2:
        # Add a container with styling for the game board
        st.markdown('<div class="game-board">', unsafe_allow_html=True)

        # Initialize Pygame if game is active
        if st.session_state.game_active and not st.session_state.game_over:
            pygame.init()
            surface = pygame.Surface((WIDTH, HEIGHT))

            # Move snake and render
            move_snake()
            surface = render_game(surface)

            # Display the game
            st.image(pygame_to_image(surface), use_container_width=True)

            # Adjust speed based on power-up
            fps = FPS_OPTIONS[st.session_state.difficulty]
            if st.session_state.power_up_active and st.session_state.power_up == "speed":
                fps = int(fps * 1.5)  # 50% speed boost

            # Don't update during countdown
            if st.session_state.countdown > 0:
                time.sleep(1.0)  # 1 second per countdown number
            else:
                time.sleep(1.0 / fps)

            st.rerun()

        elif st.session_state.game_over:
            # Game over display with improved visuals
            pygame.init()
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface = render_game(surface)
            st.image(pygame_to_image(surface), use_container_width=True)

            # Game over message with better styling
            st.markdown('<div class="game-over">', unsafe_allow_html=True)
            st.markdown(f'<h2>Game Over! Your Score: {st.session_state.score}</h2>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # New high score celebration
            if st.session_state.score == st.session_state.high_scores[st.session_state.difficulty]:
                st.balloons()
                st.markdown('<div class="high-score">', unsafe_allow_html=True)
                st.markdown('<h2>🏆 New High Score! 🏆</h2>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Restart button
            if st.button("Play Again", key="play_again", use_container_width=True):
                reset_game()

        else:
            # Default empty game board with improved visuals
            pygame.init()
            surface = pygame.Surface((WIDTH, HEIGHT))

            # Fill with gradient background
            for y in range(HEIGHT):
                color_value = 20 + int(y / HEIGHT * 20)
                pygame.draw.line(surface, (color_value, color_value, color_value), (0, y), (WIDTH, y))

            # Draw grid
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(surface, (60, 60, 60), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(surface, (60, 60, 60), (0, y), (WIDTH, y))

            # Draw border
            pygame.draw.rect(surface, (80, 80, 80), (0, 0, WIDTH, HEIGHT), 3)

            # Add welcome text
            font = pygame.font.SysFont("Arial", 36, bold=True)
            welcome_text = font.render("Welcome to Snake Game Pro!", True, (0, 200, 0))
            text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            surface.blit(welcome_text, text_rect)

            # Add start instruction
            font = pygame.font.SysFont("Arial", 24)
            start_text = font.render("Press 'Start/Reset Game' to begin playing!", True, (200, 200, 200))
            text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            surface.blit(start_text, text_rect)

            st.image(pygame_to_image(surface), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Additional features column
    with col3:
        # Game timer if game is active
        if st.session_state.game_active and st.session_state.game_start_time and not st.session_state.game_over:
            elapsed_time = (datetime.now() - st.session_state.game_start_time).total_seconds()
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)

            st.markdown('<div class="score-display">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="margin:0;">Time</h3>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:24px; margin:0;">{minutes:02d}:{seconds:02d}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Power-ups explanation
        st.markdown('<div style="background-color:#333; padding:10px; border-radius:5px; margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin:0; color:#4CAF50;">Power-ups</h3>', unsafe_allow_html=True)
        st.markdown("""
        <ul style="margin:5px 0; padding-left:20px;">
            <li style="color:#0088FF;">Speed Boost: Move faster</li>
            <li style="color:#8800FF;">Shield: Survive one collision</li>
            <li style="color:#FF8800;">Double Points: Score x2</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Tips and tricks
        st.markdown('<div style="background-color:#333; padding:10px; border-radius:5px; margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin:0; color:#4CAF50;">Tips & Tricks</h3>', unsafe_allow_html=True)
        st.markdown("""
        <ul style="margin:5px 0; padding-left:20px;">
            <li>Plan your path ahead</li>
            <li>Golden apples are worth 3 points!</li>
            <li>Power-ups appear randomly</li>
            <li>Higher difficulty = faster snake</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p>Snake Game Pro | Created by Asadullah | Enhanced with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

    # Handle keyboard input (JavaScript injection)
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            document.querySelector('[data-testid="stButton"] button[kind="secondary"]:nth-of-type(1)').click();
        } else if (e.key === 'ArrowLeft') {
            document.querySelector('[data-testid="stButton"] button[kind="secondary"]:nth-of-type(2)').click();
        } else if (e.key === 'ArrowRight') {
            document.querySelector('[data-testid="stButton"] button[kind="secondary"]:nth-of-type(4)').click();
        } else if (e.key === 'ArrowDown') {
            document.querySelector('[data-testid="stButton"] button[kind="secondary"]:nth-of-type(5)').click();
        } else if (e.key === 'p' || e.key === 'P') {
            document.querySelector('[data-testid="stButton"] button[kind="secondary"]:nth-of-type(3)').click();
        }
    });
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()