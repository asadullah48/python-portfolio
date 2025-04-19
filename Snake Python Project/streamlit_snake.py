import streamlit as st
import pygame
import numpy as np
import time
from PIL import Image
import io
import random
import json

# Set up the page configuration
st.set_page_config(
    page_title="Snake Game by Asadullah",
    layout="centered",
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

def reset_game():
    st.session_state.game_active = True
    st.session_state.snake_positions = [(GRID_WIDTH // 4, GRID_HEIGHT // 2), 
                                      (GRID_WIDTH // 4 - 1, GRID_HEIGHT // 2), 
                                      (GRID_WIDTH // 4 - 2, GRID_HEIGHT // 2)]
    st.session_state.direction = 'RIGHT'
    place_food()
    st.session_state.score = 0
    st.session_state.game_over = False

def place_food():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in st.session_state.snake_positions:
            st.session_state.food_position = (x, y)
            st.session_state.special_food = random.random() < 0.2  # 20% chance for special food
            break

def move_snake():
    if st.session_state.game_over:
        return
    
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
    if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
        new_head in st.session_state.snake_positions):
        st.session_state.game_over = True
        
        # Update high score if needed
        if st.session_state.score > st.session_state.high_scores[st.session_state.difficulty]:
            st.session_state.high_scores[st.session_state.difficulty] = st.session_state.score
        
        return
    
    # Add new head
    st.session_state.snake_positions.insert(0, new_head)
    
    # Check for food collision
    if new_head == st.session_state.food_position:
        if st.session_state.special_food:
            st.session_state.score += 3
        else:
            st.session_state.score += 1
        place_food()
    else:
        # Remove tail if no food was eaten
        st.session_state.snake_positions.pop()

def render_game(pygame_surface):
    # Fill background
    pygame_surface.fill(BLACK)
    
    # Draw grid
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(pygame_surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(pygame_surface, GRAY, (0, y), (WIDTH, y))
    
    # Draw snake
    for i, position in enumerate(st.session_state.snake_positions):
        x, y = position
        if i == 0:  # Head
            pygame.draw.rect(pygame_surface, DARK_GREEN, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(pygame_surface, GREEN, (x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
        else:  # Body
            pygame.draw.rect(pygame_surface, GREEN, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(pygame_surface, DARK_GREEN, (x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
    
    # Draw food (red or yellow for special)
    food_color = YELLOW if st.session_state.special_food else RED
    food_x, food_y = st.session_state.food_position
    pygame.draw.rect(pygame_surface, food_color, (food_x * BLOCK_SIZE, food_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw score
    font = pygame.font.SysFont("Sans", 23)
    score_text = font.render(f"Score: {st.session_state.score}", True, WHITE)
    pygame_surface.blit(score_text, (10, 10))
    
    return pygame_surface

def pygame_to_image(pygame_surface):
    # Convert Pygame surface to PIL Image
    raw_str = pygame.image.tostring(pygame_surface, 'RGB')
    return Image.frombytes('RGB', pygame_surface.get_size(), raw_str)

def main():
    # Title and description
    st.title("🐍 Snake Game by Asadullah")
    
    # Instructions
    with st.expander("How to Play"):
        st.write("""
        - Use the direction buttons to control the snake.
        - Eat food (red blocks) to grow longer and earn points.
        - Yellow food gives 3 points! (Special food)
        - Avoid hitting the walls or yourself.
        - Select difficulty level to change the game speed.
        """)
    
    # Sidebar
    with st.sidebar:
        st.header("Game Controls")
        
        # Difficulty selection
        st.session_state.difficulty = st.selectbox("Select Difficulty", 
                                                 ["Easy", "Medium", "Hard"],
                                                 index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty))
        
        # Start/Reset button
        if st.button("Start/Reset Game"):
            reset_game()
        
        # High scores
        st.header("High Scores")
        for diff, score in st.session_state.high_scores.items():
            st.write(f"{diff}: {score}")
    
    # Game area
    col1, col2, col3 = st.columns([1, 3, 1])
    
    # Control buttons
    with col1:
        st.write("## Controls")
        
        if st.button("⬆️", key="up"):
            if st.session_state.direction != 'DOWN':
                st.session_state.direction = 'UP'
        
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            if st.button("⬅️", key="left"):
                if st.session_state.direction != 'RIGHT':
                    st.session_state.direction = 'LEFT'
        with col1_3:
            if st.button("➡️", key="right"):
                if st.session_state.direction != 'LEFT':
                    st.session_state.direction = 'RIGHT'
        
        if st.button("⬇️", key="down"):
            if st.session_state.direction != 'UP':
                st.session_state.direction = 'DOWN'
    
    # Game display
    with col2:
        # Initialize Pygame if game is active
        if st.session_state.game_active and not st.session_state.game_over:
            pygame.init()
            surface = pygame.Surface((WIDTH, HEIGHT))
            
            # Move snake and render
            move_snake()
            surface = render_game(surface)
            
            # Display the game
            st.image(pygame_to_image(surface), use_container_width=True)
            
            # Rerun to update
            fps = FPS_OPTIONS[st.session_state.difficulty]
            time.sleep(1.0 / fps)
            st.rerun()
        
        elif st.session_state.game_over:
            # Game over display
            pygame.init()
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface = render_game(surface)
            st.image(pygame_to_image(surface), use_container_width=True)
            
            st.error(f"Game Over! Your Score: {st.session_state.score}")
            if st.session_state.score == st.session_state.high_scores[st.session_state.difficulty]:
                st.balloons()
                st.success("New High Score! 🏆")
        
        else:
            # Default empty game board
            pygame.init()
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface.fill(BLACK)
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))
            st.image(pygame_to_image(surface), use_container_width=True)
            
            st.info("Press 'Start/Reset Game' to begin playing!")
    
    # Score display
    with col3:
        st.write(f"## Score: {st.session_state.score}")
        st.write(f"Difficulty: {st.session_state.difficulty}")
        
        if st.session_state.game_active:
            st.write("Game Status: Active")
        else:
            st.write("Game Status: Waiting to start")

if __name__ == "__main__":
    main()