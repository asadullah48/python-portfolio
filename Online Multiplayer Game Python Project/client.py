import socket
import pygame
import json
import sys

# 🎮 Game configuration
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# 🎨 Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)
RED = (213, 50, 80)

# ⚙️ Network configuration
SERVER = 'localhost'
PORT = 5555
BUFFER_SIZE = 1024
DELIMITER = "\n"

class PongClient:
    def __init__(self):
        """Initialize the Pong client with game components and network connection."""
        # 🖥️ Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong - Multiplayer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 🏓 Game elements
        self.player1_rect = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.player2_rect = pygame.Rect(WIDTH - 50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball_rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.ball_speed = [5, 5]
        
        # 🏆 Score tracking
        self.player1_score = 0
        self.player2_score = 0
        
        # 🔌 Network setup
        self.client_socket = None
        self.player_id = None
        self.connected = False
    
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
    
    def render(self):
        """Render the game graphics on screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw center line
        pygame.draw.aaline(self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        
        # Draw paddles
        pygame.draw.rect(self.screen, BLUE, self.player1_rect)
        pygame.draw.rect(self.screen, RED, self.player2_rect)
        
        # Draw ball
        pygame.draw.ellipse(self.screen, WHITE, self.ball_rect)
        
        # Draw scores
        score_text1 = self.font.render(str(self.player1_score), True, WHITE)
        score_text2 = self.font.render(str(self.player2_score), True, WHITE)
        self.screen.blit(score_text1, (WIDTH//4, 20))
        self.screen.blit(score_text2, (3*WIDTH//4, 20))
        
        # If not connected, show message
        if not self.connected:
            reconnect_text = self.font.render("Disconnected. Press R to reconnect", True, WHITE)
            self.screen.blit(reconnect_text, (WIDTH//2 - reconnect_text.get_width()//2, HEIGHT//2))
        
        # Update the display
        pygame.display.flip()
    
    def game_loop(self):
        """Main game loop."""
        if not self.connect_to_server():
            print("❌ Failed to start game. Server connection failed.")
            return
            
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and not self.connected:
                        self.connect_to_server()
            
            # Process game logic if connected
            if self.connected:
                # Handle player input
                movement = self.handle_input()
                
                # Send player movement to server
                self.send_data({"movement": movement})
                
                # Get updated game state from server
                game_state = self.receive_data()
                self.update_game_state(game_state)
            
            # Render the game
            self.render()
            self.clock.tick(FPS)
        
        # Clean up resources
        if self.client_socket:
            self.client_socket.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    client = PongClient()
    client.game_loop()