import socket
import threading
import json
import random
import time

# 🎮 Game configuration
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
FPS = 60
DELIMITER = "\n"

class GameState:
    """Class to maintain the state of the game."""
    def __init__(self):
        # 🏓 Paddle positions
        self.player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        
        # ⚽ Ball position and speed
        self.ball_x = WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = HEIGHT // 2 - BALL_SIZE // 2
        self.ball_speed = [5 * random.choice([-1, 1]), 5 * random.choice([-1, 1])]
        
        # 🏆 Scores
        self.player1_score = 0
        self.player2_score = 0
        
        # ⏱️ Last update time
        self.last_update = time.time()
    
    def update(self):
        """Update the game state (ball position, collisions)."""
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Move the ball based on its speed
        self.ball_x += self.ball_speed[0]
        self.ball_y += self.ball_speed[1]
        
        # Check for collisions with the top and bottom walls
        if self.ball_y <= 0 or self.ball_y + BALL_SIZE >= HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]
        
        # Check for collisions with paddles
        player1_rect = pygame.Rect(30, self.player1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        player2_rect = pygame.Rect(WIDTH - 50, self.player2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE)
        
        if ball_rect.colliderect(player1_rect) or ball_rect.colliderect(player2_rect):
            self.ball_speed[0] = -self.ball_speed[0]
            # Add a slight random variation to the y speed
            self.ball_speed[1] += random.uniform(-0.5, 0.5)
        
        # Check for scoring
        if self.ball_x <= 0:
            # Player 2 scores
            self.player2_score += 1
            self.reset_ball()
        elif self.ball_x + BALL_SIZE >= WIDTH:
            # Player 1 scores
            self.player1_score += 1
            self.reset_ball()
    
    def reset_ball(self):
        """Reset the ball to the center after a score."""
        self.ball_x = WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = HEIGHT // 2 - BALL_SIZE // 2
        self.ball_speed = [5 * random.choice([-1, 1]), 5 * random.choice([-1, 1])]
    
    def to_json(self):
        """Convert the game state to a JSON object."""
        return {
            "player1_y": self.player1_y,
            "player2_y": self.player2_y,
            "ball_x": self.ball_x,
            "ball_y": self.ball_y,
            "ball_speed": self.ball_speed,
            "player1_score": self.player1_score,
            "player2_score": self.player2_score
        }

class PongServer:
    """Server class for the Pong multiplayer game."""
    def __init__(self, host='0.0.0.0', port=5555):
        # 🔌 Server configuration
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.game_state = GameState()
        self.running = False
        self.update_thread = None
    
    def start(self):
        """Start the server and listen for client connections."""
        try:
            # Create and bind the server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)  # Allow max 2 connections
            self.running = True
            
            print(f"🚀 Server started on {self.host}:{self.port}")
            
            # Start the game update thread
            self.update_thread = threading.Thread(target=self.update_game)
            self.update_thread.daemon = True
            self.update_thread.start()
            
            # Accept client connections
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"✅ New connection from {client_address}")
                    
                    # Start a thread to handle this client
                    client_thread = threading.Thread(target=self.handle_client, 
                                                   args=(client_socket, client_address))
                    client_thread.daemon = True
                    client_thread.start()
                    
                    # Add client to the list
                    self.clients.append(client_socket)
                    
                    # Limit to 2 players
                    if len(self.clients) >= 2:
                        print("⚠️ Maximum player count reached")
                        
                except Exception as e:
                    if self.running:  # Only print if not shutting down
                        print(f"❌ Error accepting connection: {e}")
            
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the server and clean up resources."""
        self.running = False
        
        # Close all client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        # Close the server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("🛑 Server stopped")
    
    def handle_client(self, client_socket, client_address):
        """Handle communication with a single client."""
        player_id = len(self.clients)  # 1 for first player, 2 for second
        
        try:
            # Send initial game state
            self.send_game_state(client_socket)
            
            # Handle client messages
            buffer = ""
            while self.running:
                # Receive data from client
                data = client_socket.recv(1024).decode()
                if not data:
                    break  # Client disconnected
                
                buffer += data
                
                # Process complete messages
                while DELIMITER in buffer:
                    message, buffer = buffer.split(DELIMITER, 1)
                    
                    try:
                        # Parse client message
                        client_data = json.loads(message)
                        
                        # Update player paddle position based on movement
                        if player_id == 1:
                            self.game_state.player1_y += client_data.get("movement", 0)
                            # Keep paddle within bounds
                            self.game_state.player1_y = max(0, min(HEIGHT - PADDLE_HEIGHT, 
                                                               self.game_state.player1_y))
                        elif player_id == 2:
                            self.game_state.player2_y += client_data.get("movement", 0)
                            # Keep paddle within bounds
                            self.game_state.player2_y = max(0, min(HEIGHT - PADDLE_HEIGHT, 
                                                               self.game_state.player2_y))
                    except json.JSONDecodeError:
                        print(f"❌ Invalid JSON from client: {message}")
                        
        except ConnectionResetError:
            print(f"❌ Connection reset by client {client_address}")
        except Exception as e:
            print(f"❌ Error handling client {client_address}: {e}")
        finally:
            # Clean up when client disconnects
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            try:
                client_socket.close()
            except:
                pass
            print(f"❌ Client {client_address} disconnected")
    
    def send_game_state(self, client_socket=None):
        """Send current game state to clients."""
        # Create JSON representation of game state
        game_state_json = json.dumps(self.game_state.to_json()) + DELIMITER
        
        if client_socket:  # Send to specific client
            try:
                client_socket.sendall(game_state_json.encode())
            except:
                pass
        else:  # Send to all clients
            for client in self.clients[:]:  # Copy list to avoid modification during iteration
                try:
                    client.sendall(game_state_json.encode())
                except:
                    # Remove disconnected clients
                    if client in self.clients:
                        self.clients.remove(client)
                    try:
                        client.close()
                    except:
                        pass
    
    def update_game(self):
        """Update the game state and broadcast to clients periodically."""
        clock = time.time()
        
        while self.running:
            # Control update rate
            current_time = time.time()
            if current_time - clock < 1.0 / FPS:
                time.sleep(0.001)  # Small sleep to prevent CPU hogging
                continue
                
            clock = current_time
            
            # Update game state
            self.game_state.update()
            
            # Send updated state to all clients
            self.send_game_state()

# For importing the pygame.Rect class without full pygame
class pygame:
    class Rect:
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
        
        def colliderect(self, other):
            """Return True if two rectangles overlap."""
            return (self.x < other.x + other.w and 
                    self.x + self.w > other.x and 
                    self.y < other.y + other.h and 
                    self.y + self.h > other.y)

if __name__ == "__main__":
    server = PongServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server interrupted by user")
    finally:
        server.stop()