import pygame
import random
import sys
import json
import os

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS_OPTIONS = {"Easy": 8, "Medium": 12, "Hard": 16}
FPS = FPS_OPTIONS["Medium"]  # Default difficulty

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game by Asadullah')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Sans", 23, bold=True)
title_font = pygame.font.SysFont("Sans", 36, bold=True)

# High score file
HIGH_SCORE_FILE = "snake_high_scores.json"

def load_high_scores():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return {"Easy": 0, "Medium": 0, "Hard": 0}

def save_high_score(difficulty, score):
    high_scores = load_high_scores()
    if score > high_scores.get(difficulty, 0):
        high_scores[difficulty] = score
        with open(HIGH_SCORE_FILE, "w") as file:
            json.dump(high_scores, file)
        return True
    return False

class Snake:
    def __init__(self):
        self.body = [(100, 50), (80, 50), (60, 50)]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'  # Buffer for direction change
        self.grow_pending = False

    def set_direction(self, direction):
        # Only allow valid direction changes
        if direction == 'UP' and self.direction != 'DOWN':
            self.next_direction = 'UP'
        elif direction == 'DOWN' and self.direction != 'UP':
            self.next_direction = 'DOWN'
        elif direction == 'LEFT' and self.direction != 'RIGHT':
            self.next_direction = 'LEFT'
        elif direction == 'RIGHT' and self.direction != 'LEFT':
            self.next_direction = 'RIGHT'

    def move(self):
        # Apply the buffered direction change
        self.direction = self.next_direction
        
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            x += BLOCK_SIZE
        new_head = (x, y)
        self.body = [new_head] + self.body
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def draw(self, surface):
        # Draw head in different color
        head = self.body[0]
        pygame.draw.rect(surface, DARK_GREEN, (head[0], head[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, GREEN, (head[0]+2, head[1]+2, BLOCK_SIZE-4, BLOCK_SIZE-4))
        
        # Draw body
        for segment in self.body[1:]:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, DARK_GREEN, (segment[0]+2, segment[1]+2, BLOCK_SIZE-4, BLOCK_SIZE-4))

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:] or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        )

class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)
        self.color = RED
        self.special = random.random() < 0.2  # 20% chance for special food
        if self.special:
            self.color = YELLOW  # Special food is yellow

    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))
        # Add a little shine to the food
        pygame.draw.rect(surface, WHITE, (self.position[0]+5, self.position[1]+5, 3, 3))

def draw_grid(surface):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

def draw_button(surface, text, position, size, color=BLUE, hover=False):
    x, y, width, height = position[0], position[1], size[0], size[1]
    button_color = (color[0]-30, color[1]-30, color[2]-30) if hover else color
    
    # Draw button
    pygame.draw.rect(surface, button_color, (x, y, width, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)  # Border
    
    # Draw text
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surf, text_rect)
    
    return pygame.Rect(x, y, width, height)

def main_menu():
    high_scores = load_high_scores()
    difficulty = "Medium"  # Default difficulty
    
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        
        # Title
        title = title_font.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        # Difficulty buttons
        mouse_pos = pygame.mouse.get_pos()
        
        easy_hover = False
        medium_hover = False
        hard_hover = False
        
        easy_rect = draw_button(screen, "Easy", (WIDTH // 2 - 100, 150), (200, 40), BLUE, easy_hover)
        medium_rect = draw_button(screen, "Medium", (WIDTH // 2 - 100, 200), (200, 40), BLUE, medium_hover)
        hard_rect = draw_button(screen, "Hard", (WIDTH // 2 - 100, 250), (200, 40), BLUE, hard_hover)
        
        # Current difficulty indicator
        if difficulty == "Easy":
            pygame.draw.circle(screen, GREEN, (WIDTH // 2 - 120, 170), 10)
        elif difficulty == "Medium":
            pygame.draw.circle(screen, GREEN, (WIDTH // 2 - 120, 220), 10)
        elif difficulty == "Hard":
            pygame.draw.circle(screen, GREEN, (WIDTH // 2 - 120, 270), 10)
        
        # Start button
        start_hover = False
        start_rect = draw_button(screen, "START GAME", (WIDTH // 2 - 100, 320), (200, 50), GREEN, start_hover)
        
        # Show high scores
        score_text = font.render(f"High Score: {high_scores.get(difficulty, 0)}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 100))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                easy_hover = easy_rect.collidepoint(event.pos)
                medium_hover = medium_rect.collidepoint(event.pos)
                hard_hover = hard_rect.collidepoint(event.pos)
                start_hover = start_rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    difficulty = "Easy"
                elif medium_rect.collidepoint(event.pos):
                    difficulty = "Medium"
                elif hard_rect.collidepoint(event.pos):
                    difficulty = "Hard"
                elif start_rect.collidepoint(event.pos):
                    game_loop(difficulty)
        
        clock.tick(60)

def pause_screen():
    paused = True
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    pause_text = title_font.render("PAUSED", True, WHITE)
    continue_text = font.render("Press P to continue or Q to quit", True, WHITE)
    
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    return True  # Signal to quit the game
        clock.tick(15)
    
    return False  # Continue the game

def game_over_screen(score, difficulty):
    high_scores = load_high_scores()
    new_high_score = save_high_score(difficulty, score)
    
    screen.fill(BLACK)
    
    if new_high_score:
        congrats_text = title_font.render("NEW HIGH SCORE!", True, YELLOW)
        screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 80))
    
    text1 = font.render(f"Game Over! Your Score: {score}", True, WHITE)
    text2 = font.render("Press R to Restart or Q to Quit", True, WHITE)
    text3 = font.render(f"High Score: {high_scores.get(difficulty, 0)}", True, WHITE)
    
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 40))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Return to main menu
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop(difficulty):
    FPS = FPS_OPTIONS[difficulty]
    snake = Snake()
    food = Food(snake.body)
    score = 0
    paused = False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if pause_screen():
                        return  # Quit to main menu
                elif event.key == pygame.K_UP:
                    snake.set_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.set_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.set_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction('RIGHT')

        snake.move()

        # Food collision
        if snake.body[0] == food.position:
            snake.grow()
            if food.special:
                score += 3  # Special food gives 3 points
            else:
                score += 1  # Regular food gives 1 point
            food = Food(snake.body)

        # Check game over
        if snake.check_collision():
            game_over_screen(score, difficulty)
            return  # Return to main menu

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        # Display score and difficulty
        score_text = font.render(f"Score: {score}", True, WHITE)
        diff_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(diff_text, (WIDTH - diff_text.get_width() - 10, 10))

        pygame.display.update()

if __name__ == "__main__":
    main_menu()