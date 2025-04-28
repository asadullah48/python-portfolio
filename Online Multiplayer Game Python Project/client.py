import socket
import pygame
import json
import sys
import os
import random
import math
import time
import argparse
from pygame import gfxdraw

# Parse command line arguments
parser = argparse.ArgumentParser(description='Pong Multiplayer Client')
parser.add_argument('--server', default='localhost', help='Server IP address')
parser.add_argument('--port', type=int, default=5555, help='Server port')
parser.add_argument('--name', default='Player 1', help='Player name')
parser.add_argument('--color', default='#3498db', help='Paddle color (hex)')
parser.add_argument('--sound', action='store_true', help='Enable sound effects')
parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
args = parser.parse_args()

# 🎮 Game configuration
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# 🎨 Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
BLUE = (50, 153, 213)
RED = (213, 50, 80)
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Convert hex color to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Use the color from command line args
PLAYER_COLOR = hex_to_rgb(args.color)

# ⚙️ Network configuration
SERVER = args.server
PORT = args.port
BUFFER_SIZE = 1024
DELIMITER = "\n"

# 🎵 Sound configuration
SOUND_ENABLED = args.sound

# Create sounds directory if it doesn't exist
os.makedirs('sounds', exist_ok=True)

# Function to create placeholder sound files if they don't exist
def create_placeholder_sounds():
    # List of sound files to create
    sound_files = {
        'paddle_hit.wav': b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00',
        'wall_hit.wav': b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00',
        'score.wav': b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00',
        'game_start.wav': b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00',
        'game_over.wav': b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00',
    }

    for filename, content in sound_files.items():
        filepath = os.path.join('sounds', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(content)

# Create placeholder sound files
create_placeholder_sounds()

class Particle:
    """Class for creating visual particle effects."""
    def __init__(self, x, y, color, speed=3, size=3, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)

    def update(self):
        """Update particle position and lifetime."""
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        # Shrink particle as it ages
        self.size = max(0, self.size * (self.lifetime / self.max_lifetime))
        return self.lifetime > 0

    def draw(self, screen):
        """Draw the particle on screen."""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.size), color_with_alpha)

class PowerUp:
    """Class for power-up items that can appear during gameplay."""
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type_id = type_id
        self.rect = pygame.Rect(x, y, 30, 30)
        self.active = True
        self.lifetime = 300  # 5 seconds at 60 FPS

        # Define power-up types
        self.types = {
            0: {"name": "Speed Up", "color": YELLOW, "effect": "speed"},
            1: {"name": "Paddle Size", "color": GREEN, "effect": "size"},
            2: {"name": "Slow Down", "color": PURPLE, "effect": "slow"}
        }

    def update(self):
        """Update power-up state."""
        self.lifetime -= 1
        return self.lifetime > 0 and self.active

    def draw(self, screen):
        """Draw the power-up on screen."""
        # Draw power-up with pulsing effect
        pulse = abs(math.sin(time.time() * 5)) * 0.3 + 0.7
        color = tuple(int(c * pulse) for c in self.types[self.type_id]["color"])

        # Draw power-up background
        pygame.draw.circle(screen, color, (self.x + 15, self.y + 15), 15)

        # Draw power-up icon
        if self.type_id == 0:  # Speed Up
            pygame.draw.polygon(screen, WHITE, [(self.x + 10, self.y + 20), (self.x + 20, self.y + 10), (self.x + 20, self.y + 20)])
        elif self.type_id == 1:  # Paddle Size
            pygame.draw.rect(screen, WHITE, (self.x + 8, self.y + 12, 14, 6))
        elif self.type_id == 2:  # Slow Down
            pygame.draw.circle(screen, WHITE, (self.x + 15, self.y + 15), 5)

class PongClient:
    def __init__(self):
        """Initialize the Pong client with game components and network connection."""
        # 🖥️ Initialize Pygame
        pygame.init()

        # Set up display
        if args.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            self.width, self.height = WIDTH, HEIGHT
            self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(f"Pong - Multiplayer - {args.name}")

        # Load icon
        try:
            icon = pygame.Surface((32, 32))
            icon.fill(BLACK)
            pygame.draw.rect(icon, PLAYER_COLOR, (5, 8, 5, 16))
            pygame.draw.rect(icon, RED, (22, 8, 5, 16))
            pygame.draw.circle(icon, WHITE, (16, 16), 4)
            pygame.display.set_icon(icon)
        except:
            pass  # Skip icon if there's an error

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Load sounds
        self.sounds = {}
        if SOUND_ENABLED:
            try:
                self.sounds['paddle_hit'] = pygame.mixer.Sound(os.path.join('sounds', 'paddle_hit.wav'))
                self.sounds['wall_hit'] = pygame.mixer.Sound(os.path.join('sounds', 'wall_hit.wav'))
                self.sounds['score'] = pygame.mixer.Sound(os.path.join('sounds', 'score.wav'))
                self.sounds['game_start'] = pygame.mixer.Sound(os.path.join('sounds', 'game_start.wav'))
                self.sounds['game_over'] = pygame.mixer.Sound(os.path.join('sounds', 'game_over.wav'))
            except:
                print("⚠️ Warning: Could not load sound files")

        # 🏓 Game elements
        paddle_y = self.height // 2 - PADDLE_HEIGHT // 2
        self.player1_rect = pygame.Rect(30, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.player2_rect = pygame.Rect(self.width - 50, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball_rect = pygame.Rect(self.width // 2 - BALL_SIZE // 2, self.height // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.ball_speed = [5, 5]

        # 🏆 Score tracking
        self.player1_score = 0
        self.player2_score = 0

        # 🔌 Network setup
        self.client_socket = None
        self.player_id = None
        self.connected = False

        # 🎮 Game state
        self.game_state = "connecting"  # connecting, playing, game_over
        self.last_score_time = 0
        self.score_animation = 0
        self.winner = None
        self.particles = []
        self.power_ups = []
        self.active_effects = {}
        self.effect_end_time = {}
        self.message = ""
        self.message_time = 0

        # Player info
        self.player_name = args.name
        self.opponent_name = "Opponent"

    def connect_to_server(self):
        """Establish connection with the game server."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER, PORT))
            self.client_socket.setblocking(False)  # Non-blocking socket
            self.connected = True
            print("✅ Connected to server")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to server: {e}")
            return False

    def send_data(self, data):
        """Send data to the server with proper formatting."""
        if not self.connected:
            return

        try:
            message = json.dumps(data) + DELIMITER
            self.client_socket.sendall(message.encode())
        except Exception as e:
            print(f"❌ Error sending data: {e}")
            self.connected = False

    def receive_data(self):
        """Receive and parse data from the server."""
        if not self.connected:
            return None

        try:
            data = self.client_socket.recv(BUFFER_SIZE).decode()
            if not data:  # Connection closed by server
                print("❌ Server disconnected")
                self.connected = False
                return None

            try:
                # Parse JSON data
                game_state = json.loads(data)
                return game_state
            except json.JSONDecodeError:
                print("❌ Invalid data received from server")
                return None

        except BlockingIOError:
            # No data available (non-blocking socket)
            return None
        except Exception as e:
            print(f"❌ Error receiving data: {e}")
            self.connected = False
            return None

    def handle_input(self):
        """Process keyboard input for paddle movement."""
        keys = pygame.key.get_pressed()
        movement = 0

        # Move paddle based on key presses
        if keys[pygame.K_w] and self.player1_rect.top > 0:
            movement = -5
        elif keys[pygame.K_s] and self.player1_rect.bottom < HEIGHT:
            movement = 5

        return movement

    def update_game_state(self, game_state):
        """Update local game state based on server data."""
        if not game_state:
            return

        # Update paddle positions
        self.player1_rect.y = game_state["player1_y"]
        self.player2_rect.y = game_state["player2_y"]

        # Update ball position and speed
        self.ball_rect.x = game_state["ball_x"]
        self.ball_rect.y = game_state["ball_y"]
        self.ball_speed = game_state["ball_speed"]

        # Update scores
        self.player1_score = game_state["player1_score"]
        self.player2_score = game_state["player2_score"]

    def play_sound(self, sound_name):
        """Play a sound effect if sound is enabled."""
        if SOUND_ENABLED and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass

    def add_particles(self, x, y, color, count=20, speed=3, size=3, lifetime=30):
        """Add particle effects at the specified position."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed, size, lifetime))

    def show_message(self, message, duration=180):
        """Show a temporary message on screen."""
        self.message = message
        self.message_time = duration

    def render(self):
        """Render the game graphics on screen with enhanced visuals."""
        # Clear screen with a gradient background
        self.screen.fill(BLACK)

        # Draw a subtle grid pattern for the court
        for x in range(0, self.width, 40):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 40):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.width, y), 1)

        # Draw court boundaries
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, 0, self.width, self.height), 2)

        # Draw center line with dashed effect
        for y in range(0, self.height, 20):
            pygame.draw.line(self.screen, WHITE, (self.width//2, y), (self.width//2, y+10), 2)

        # Draw center circle
        pygame.draw.circle(self.screen, LIGHT_GRAY, (self.width//2, self.height//2), 50, 1)

        # Draw paddles with custom colors and highlights
        # Player 1 paddle (left)
        pygame.draw.rect(self.screen, PLAYER_COLOR, self.player1_rect)
        # Add highlight to paddle
        highlight_rect = pygame.Rect(self.player1_rect.x, self.player1_rect.y, 3, self.player1_rect.height)
        pygame.draw.rect(self.screen, (*PLAYER_COLOR, 128), highlight_rect.inflate(2, 2))

        # Player 2 paddle (right)
        pygame.draw.rect(self.screen, RED, self.player2_rect)
        # Add highlight to paddle
        highlight_rect = pygame.Rect(self.player2_rect.x + self.player2_rect.width - 3,
                                    self.player2_rect.y, 3, self.player2_rect.height)
        pygame.draw.rect(self.screen, (*RED, 128), highlight_rect.inflate(2, 2))

        # Draw ball with glow effect
        # Outer glow
        for radius in range(4, 0, -1):
            alpha = 100 - radius * 20
            gfxdraw.aacircle(self.screen,
                           int(self.ball_rect.centerx),
                           int(self.ball_rect.centery),
                           BALL_SIZE//2 + radius,
                           (*WHITE, alpha))

        # Main ball
        pygame.draw.ellipse(self.screen, WHITE, self.ball_rect)
        # Ball highlight
        highlight_pos = (self.ball_rect.centerx - 2, self.ball_rect.centery - 2)
        gfxdraw.filled_circle(self.screen, int(highlight_pos[0]), int(highlight_pos[1]), 2, WHITE)

        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw scores with enhanced styling
        score_font = pygame.font.Font(None, 72)
        score_text1 = score_font.render(str(self.player1_score), True, WHITE)
        score_text2 = score_font.render(str(self.player2_score), True, WHITE)

        # Add score animation effect when scoring
        if time.time() - self.last_score_time < 1.0:
            scale = 1.0 + 0.5 * (1.0 - (time.time() - self.last_score_time))
            if self.score_animation == 1:  # Player 1 scored
                score_text1 = pygame.transform.scale(score_text1,
                                                  (int(score_text1.get_width() * scale),
                                                   int(score_text1.get_height() * scale)))
            elif self.score_animation == 2:  # Player 2 scored
                score_text2 = pygame.transform.scale(score_text2,
                                                  (int(score_text2.get_width() * scale),
                                                   int(score_text2.get_height() * scale)))

        # Draw scores
        self.screen.blit(score_text1, (self.width//4 - score_text1.get_width()//2, 20))
        self.screen.blit(score_text2, (3*self.width//4 - score_text2.get_width()//2, 20))

        # Draw player names
        name_text1 = self.small_font.render(self.player_name, True, PLAYER_COLOR)
        name_text2 = self.small_font.render(self.opponent_name, True, RED)
        self.screen.blit(name_text1, (self.width//4 - name_text1.get_width()//2, 80))
        self.screen.blit(name_text2, (3*self.width//4 - name_text2.get_width()//2, 80))

        # Draw active effects
        effect_y = 120
        for effect, end_time in self.effect_end_time.items():
            remaining = end_time - time.time()
            if remaining > 0:
                effect_text = self.small_font.render(f"{effect}: {int(remaining)}s", True, YELLOW)
                self.screen.blit(effect_text, (10, effect_y))
                effect_y += 25

        # Draw temporary message
        if self.message and self.message_time > 0:
            self.message_time -= 1
            message_text = self.font.render(self.message, True, WHITE)
            message_bg = pygame.Surface((message_text.get_width() + 20, message_text.get_height() + 10))
            message_bg.fill(BLACK)
            message_bg.set_alpha(200)
            self.screen.blit(message_bg, (self.width//2 - message_bg.get_width()//2, self.height//4))
            self.screen.blit(message_text, (self.width//2 - message_text.get_width()//2, self.height//4 + 5))

        # Draw game state specific elements
        if self.game_state == "connecting":
            # Draw connecting message
            connecting_text = self.font.render("Connecting to server...", True, WHITE)
            self.screen.blit(connecting_text, (self.width//2 - connecting_text.get_width()//2, self.height//2))

            # Draw animated loading dots
            dots = "." * (int(time.time() * 2) % 4)
            dots_text = self.font.render(dots, True, WHITE)
            self.screen.blit(dots_text, (self.width//2 + connecting_text.get_width()//2, self.height//2))

        elif self.game_state == "game_over":
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            self.screen.blit(overlay, (0, 0))

            # Draw game over message
            game_over_text = pygame.font.Font(None, 72).render("GAME OVER", True, WHITE)
            self.screen.blit(game_over_text, (self.width//2 - game_over_text.get_width()//2, self.height//2 - 50))

            # Draw winner message
            if self.winner:
                winner_text = self.font.render(f"{self.winner} wins!", True, GREEN)
                self.screen.blit(winner_text, (self.width//2 - winner_text.get_width()//2, self.height//2 + 20))

            # Draw restart instructions
            restart_text = self.font.render("Press R to play again", True, WHITE)
            self.screen.blit(restart_text, (self.width//2 - restart_text.get_width()//2, self.height//2 + 70))

        # If not connected, show message
        if not self.connected and self.game_state != "game_over":
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            self.screen.blit(overlay, (0, 0))

            # Draw disconnected message
            disconnected_text = self.font.render("Disconnected from server", True, RED)
            self.screen.blit(disconnected_text, (self.width//2 - disconnected_text.get_width()//2, self.height//2 - 20))

            # Draw reconnect instructions
            reconnect_text = self.font.render("Press R to reconnect", True, WHITE)
            self.screen.blit(reconnect_text, (self.width//2 - reconnect_text.get_width()//2, self.height//2 + 20))

        # Draw FPS counter in corner
        fps_text = self.small_font.render(f"FPS: {int(self.clock.get_fps())}", True, LIGHT_GRAY)
        self.screen.blit(fps_text, (self.width - fps_text.get_width() - 10, self.height - fps_text.get_height() - 10))

        # Update the display
        pygame.display.flip()

    def handle_input(self):
        """Process keyboard input for paddle movement with improved controls."""
        keys = pygame.key.get_pressed()
        movement = 0
        speed = 5  # Base speed

        # Apply speed effects if active
        if "Speed Up" in self.active_effects:
            speed = 8
        elif "Slow Down" in self.active_effects:
            speed = 3

        # Move paddle based on key presses
        if keys[pygame.K_w] and self.player1_rect.top > 0:
            movement = -speed
        elif keys[pygame.K_s] and self.player1_rect.bottom < self.height:
            movement = speed

        return movement

    def update_game_state(self, game_state):
        """Update local game state based on server data with enhanced features."""
        if not game_state:
            return

        # Store previous positions for effect detection
        prev_ball_x = self.ball_rect.x
        prev_ball_y = self.ball_rect.y
        prev_player1_score = self.player1_score
        prev_player2_score = self.player2_score

        # Update paddle positions
        self.player1_rect.y = game_state["player1_y"]
        self.player2_rect.y = game_state["player2_y"]

        # Update ball position and speed
        self.ball_rect.x = game_state["ball_x"]
        self.ball_rect.y = game_state["ball_y"]
        self.ball_speed = game_state["ball_speed"]

        # Update scores
        self.player1_score = game_state["player1_score"]
        self.player2_score = game_state["player2_score"]

        # Check for scoring events
        if self.player1_score > prev_player1_score:
            self.last_score_time = time.time()
            self.score_animation = 1
            self.play_sound("score")
            self.add_particles(self.width - 30, self.ball_rect.centery, PLAYER_COLOR, 30, 5, 4, 60)
            self.show_message(f"{self.player_name} scores!")

        elif self.player2_score > prev_player2_score:
            self.last_score_time = time.time()
            self.score_animation = 2
            self.play_sound("score")
            self.add_particles(30, self.ball_rect.centery, RED, 30, 5, 4, 60)
            self.show_message(f"{self.opponent_name} scores!")

        # Check for paddle hits
        if (prev_ball_x > self.ball_rect.x and self.ball_rect.colliderect(self.player1_rect)) or \
           (prev_ball_x < self.ball_rect.x and self.ball_rect.colliderect(self.player2_rect)):
            self.play_sound("paddle_hit")

            # Add particles at collision point
            if self.ball_rect.colliderect(self.player1_rect):
                self.add_particles(self.player1_rect.right, self.ball_rect.centery, WHITE)
            else:
                self.add_particles(self.player2_rect.left, self.ball_rect.centery, WHITE)

        # Check for wall hits
        if (prev_ball_y < 0 and self.ball_rect.y > 0) or \
           (prev_ball_y > self.height - BALL_SIZE and self.ball_rect.y < self.height - BALL_SIZE):
            self.play_sound("wall_hit")
            self.add_particles(self.ball_rect.centerx,
                             0 if prev_ball_y < 0 else self.height,
                             WHITE, 10, 3, 2, 20)

        # Update game state if provided
        if "game_state" in game_state:
            self.game_state = game_state["game_state"]

            # Handle game over state
            if self.game_state == "game_over":
                self.play_sound("game_over")
                self.winner = self.player_name if self.player1_score > self.player2_score else self.opponent_name

        # Update player info if provided
        if "player_name" in game_state:
            self.player_name = game_state["player_name"]
        if "opponent_name" in game_state:
            self.opponent_name = game_state["opponent_name"]

        # Handle power-ups if provided
        if "power_ups" in game_state:
            self.power_ups = []
            for pu in game_state["power_ups"]:
                self.power_ups.append(PowerUp(pu["x"], pu["y"], pu["type"]))

        # Handle active effects if provided
        if "active_effects" in game_state:
            self.active_effects = game_state["active_effects"]

            # Set end times for effects
            for effect, duration in game_state["active_effects"].items():
                if effect not in self.effect_end_time:
                    self.effect_end_time[effect] = time.time() + duration
                    self.show_message(f"Power-up: {effect} activated!")

    def game_loop(self):
        """Main game loop with enhanced features and game flow."""
        # Set initial game state
        self.game_state = "connecting"

        # Try to connect to server
        if not self.connect_to_server():
            print("❌ Failed to start game. Server connection failed.")
            self.show_message("Failed to connect to server. Check your network settings.")
        else:
            # Play start sound on successful connection
            self.play_sound("game_start")
            self.game_state = "playing"
            self.show_message("Connected to server! Game starting...")

            # Send player info to server
            self.send_data({
                "player_name": self.player_name,
                "paddle_color": args.color
            })

        # Main game loop
        running = True
        last_time = time.time()

        while running:
            # Calculate delta time for smooth animations
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle reconnection
                    if event.key == pygame.K_r and (not self.connected or self.game_state == "game_over"):
                        if self.game_state == "game_over":
                            # Reset game state for new game
                            self.player1_score = 0
                            self.player2_score = 0
                            self.game_state = "connecting"
                            self.winner = None
                            self.active_effects = {}
                            self.effect_end_time = {}
                            self.power_ups = []

                        # Try to reconnect
                        if self.connect_to_server():
                            self.play_sound("game_start")
                            self.game_state = "playing"
                            self.show_message("Connected to server! Game starting...")

                            # Send player info to server
                            self.send_data({
                                "player_name": self.player_name,
                                "paddle_color": args.color
                            })

                    # Toggle fullscreen with F11
                    elif event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

                    # Escape key to quit
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # Process game logic if connected
            if self.connected and self.game_state == "playing":
                # Handle player input
                movement = self.handle_input()

                # Send player movement to server
                self.send_data({
                    "movement": movement,
                    "player_name": self.player_name
                })

                # Get updated game state from server
                game_state = self.receive_data()
                self.update_game_state(game_state)

            # Update particles
            self.particles = [p for p in self.particles if p.update()]

            # Update power-ups
            self.power_ups = [p for p in self.power_ups if p.update()]

            # Clean up expired effects
            current_effects = list(self.effect_end_time.keys())
            for effect in current_effects:
                if self.effect_end_time[effect] <= current_time:
                    del self.effect_end_time[effect]
                    if effect in self.active_effects:
                        self.show_message(f"{effect} effect expired")

            # Render the game
            self.render()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Clean up resources
        if self.client_socket:
            self.client_socket.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    client = PongClient()
    client.game_loop()