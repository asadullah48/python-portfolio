import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# Game constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Load sounds
try:
    click_sound = pygame.mixer.Sound(os.path.join("sounds", "click.wav"))
    win_sound = pygame.mixer.Sound(os.path.join("sounds", "win.wav"))
    draw_sound = pygame.mixer.Sound(os.path.join("sounds", "draw.wav"))
except:
    # Create dummy sound objects if files not found
    click_sound = pygame.mixer.Sound(pygame.sndarray.array([0] * 44100))
    win_sound = pygame.mixer.Sound(pygame.sndarray.array([0] * 44100))
    draw_sound = pygame.mixer.Sound(pygame.sndarray.array([0] * 44100))

# Game state
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = 1  # 1 for X, 2 for O
game_over = False
vs_computer = False
difficulty = "easy"  # easy, medium, hard
scores = {"X": 0, "O": 0, "Ties": 0}
show_menu = True

def draw_menu():
    """Draw the main menu"""
    screen.fill(BG_COLOR)
    
    # Title
    title = FONT.render("TIC TAC TOE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # PvP button
    pvp_button = pygame.Rect(WIDTH//2 - 100, 200, 200, 50)
    pygame.draw.rect(screen, LINE_COLOR, pvp_button)
    pvp_text = SMALL_FONT.render("Player vs Player", True, WHITE)
    screen.blit(pvp_text, (pvp_button.centerx - pvp_text.get_width()//2, pvp_button.centery - pvp_text.get_height()//2))
    
    # PvC button
    pvc_button = pygame.Rect(WIDTH//2 - 100, 270, 200, 50)
    pygame.draw.rect(screen, LINE_COLOR, pvc_button)
    pvc_text = SMALL_FONT.render("Player vs Computer", True, WHITE)
    screen.blit(pvc_text, (pvc_button.centerx - pvc_text.get_width()//2, pvc_button.centery - pvc_text.get_height()//2))
    
    # Difficulty buttons (only shown when PvC is selected)
    if vs_computer:
        diff_text = SMALL_FONT.render("Difficulty:", True, WHITE)
        screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 340))
        
        # Easy button
        easy_button = pygame.Rect(WIDTH//2 - 160, 380, 100, 40)
        pygame.draw.rect(screen, LINE_COLOR if difficulty == "easy" else LINE_COLOR, easy_button, 0 if difficulty == "easy" else 2)
        easy_text = SMALL_FONT.render("Easy", True, WHITE)
        screen.blit(easy_text, (easy_button.centerx - easy_text.get_width()//2, easy_button.centery - easy_text.get_height()//2))
        
        # Medium button
        medium_button = pygame.Rect(WIDTH//2 - 50, 380, 100, 40)
        pygame.draw.rect(screen, LINE_COLOR if difficulty == "medium" else LINE_COLOR, medium_button, 0 if difficulty == "medium" else 2)
        medium_text = SMALL_FONT.render("Medium", True, WHITE)
        screen.blit(medium_text, (medium_button.centerx - medium_text.get_width()//2, medium_button.centery - medium_text.get_height()//2))
        
        # Hard button
        hard_button = pygame.Rect(WIDTH//2 + 60, 380, 100, 40)
        pygame.draw.rect(screen, LINE_COLOR if difficulty == "hard" else LINE_COLOR, hard_button, 0 if difficulty == "hard" else 2)
        hard_text = SMALL_FONT.render("Hard", True, WHITE)
        screen.blit(hard_text, (hard_button.centerx - hard_text.get_width()//2, hard_button.centery - hard_text.get_height()//2))
    
    # Start button
    start_button = pygame.Rect(WIDTH//2 - 100, 450, 200, 50)
    pygame.draw.rect(screen, LINE_COLOR, start_button)
    start_text = SMALL_FONT.render("Start Game", True, WHITE)
    screen.blit(start_text, (start_button.centerx - start_text.get_width()//2, start_button.centery - start_text.get_height()//2))
    
    # Credits
    credits = SMALL_FONT.render("by Asadullah48", True, WHITE)
    screen.blit(credits, (WIDTH//2 - credits.get_width()//2, HEIGHT - 50))
    
    return {
        "pvp_button": pvp_button,
        "pvc_button": pvc_button,
        "easy_button": easy_button if vs_computer else None,
        "medium_button": medium_button if vs_computer else None,
        "hard_button": hard_button if vs_computer else None,
        "start_button": start_button
    }

def handle_menu_click(buttons, pos):
    """Handle clicks on menu buttons"""
    global vs_computer, difficulty, show_menu
    
    if buttons["pvp_button"].collidepoint(pos):
        vs_computer = False
    
    elif buttons["pvc_button"].collidepoint(pos):
        vs_computer = True
    
    elif vs_computer and buttons["easy_button"] and buttons["easy_button"].collidepoint(pos):
        difficulty = "easy"
    
    elif vs_computer and buttons["medium_button"] and buttons["medium_button"].collidepoint(pos):
        difficulty = "medium"
    
    elif vs_computer and buttons["hard_button"] and buttons["hard_button"].collidepoint(pos):
        difficulty = "hard"
    
    elif buttons["start_button"].collidepoint(pos):
        show_menu = False
        restart()

def draw_lines():
    """Draw the grid lines"""
    screen.fill(BG_COLOR)
    
    # Draw score
    score_text = SMALL_FONT.render(f"X: {scores['X']}  |  O: {scores['O']}  |  Ties: {scores['Ties']}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))
    
    # Draw mode
    mode_text = SMALL_FONT.render("Player vs " + ("Computer" if vs_computer else "Player"), True, WHITE)
    screen.blit(mode_text, (WIDTH//2 - mode_text.get_width()//2, 40))
    
    if vs_computer:
        diff_text = SMALL_FONT.render(f"Difficulty: {difficulty.title()}", True, WHITE)
        screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 70))
    
    # Horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE + 100), (WIDTH, i * SQUARE_SIZE + 100), LINE_WIDTH)
    
    # Vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 100), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw X's and O's on the board"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + 100  # +100 for scoreboard space
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            
            if board[row][col] == 1:
                # Draw X
                start_desc = (center_x - SQUARE_SIZE//2 + SPACE, center_y - SQUARE_SIZE//2 + SPACE)
                end_desc = (center_x + SQUARE_SIZE//2 - SPACE, center_y + SQUARE_SIZE//2 - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                
                start_asc = (center_x - SQUARE_SIZE//2 + SPACE, center_y + SQUARE_SIZE//2 - SPACE)
                end_asc = (center_x + SQUARE_SIZE//2 - SPACE, center_y - SQUARE_SIZE//2 + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
                
            elif board[row][col] == 2:
                # Draw O
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_game_over():
    """Draw game over message"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    if check_win(1):
        text = FONT.render("X WINS!", True, WHITE)
    elif check_win(2):
        text = FONT.render("O WINS!", True, WHITE)
    else:
        text = FONT.render("DRAW!", True, WHITE)
    
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    restart_text = SMALL_FONT.render("Press R to Restart | M for Menu", True, WHITE)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

def mark_square(row, col, player):
    """Mark a square with the player's symbol"""
    board[row][col] = player

def is_available(row, col):
    """Check if a square is available"""
    return board[row][col] == 0

def is_board_full():
    """Check if the board is full"""
    for row in board:
        if 0 in row:
            return False
    return True

def check_win(player):
    """Check if a player has won"""
    # Check rows
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]):
            return True
    
    # Check columns
    for i in range(3):
        if all([board[j][i] == player for j in range(3)]):
            return True
    
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    
    return False

def draw_win_line(player):
    """Draw a line through the winning combination"""
    # Rows
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]):
            y = i * SQUARE_SIZE + SQUARE_SIZE // 2 + 100  # +100 for scoreboard space
            pygame.draw.line(screen, RED, (20, y), (WIDTH - 20, y), 10)
            return
    
    # Columns
    for i in range(3):
        if all([board[j][i] == player for j in range(3)]):
            x = i * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, RED, (x, 120), (x, HEIGHT - 20), 10)
            return
    
    # Diagonals
    if all([board[i][i] == player for i in range(3)]):
        pygame.draw.line(screen, RED, (20, 120), (WIDTH - 20, HEIGHT - 20), 10)
    elif all([board[i][2 - i] == player for i in range(3)]):
        pygame.draw.line(screen, RED, (WIDTH - 20, 120), (20, HEIGHT - 20), 10)

def restart():
    """Restart the game"""
    global board, player, game_over
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = 1
    game_over = False
    draw_lines()

def minimax(board, depth, is_maximizing):
    """Minimax algorithm for AI moves"""
    # Check terminal states
    if check_win(1):  # AI loses
        return -10 + depth
    
    if check_win(2):  # AI wins
        return 10 - depth
    
    if is_board_full():  # Draw
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = 2  # AI is player 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = 1  # Human is player 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0  # Undo move
                    best_score = min(score, best_score)
        return best_score

def get_best_move():
    """Get the best move for the AI based on difficulty"""
    if difficulty == "easy":
        # Random move
        empty_squares = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
        if empty_squares:
            return random.choice(empty_squares)
        return None
    
    elif difficulty == "medium":
        # 50% chance of optimal move, 50% random
        if random.random() > 0.5:
            return get_best_move_minimax()
        else:
            empty_squares = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
            if empty_squares:
                return random.choice(empty_squares)
            return None
    
    else:  # Hard
        return get_best_move_minimax()

def get_best_move_minimax():
    """Get the best move using minimax algorithm"""
    best_score = -float('inf')
    best_move = None
    
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                board[row][col] = 2  # AI is player 2
                score = minimax(board, 0, False)
                board[row][col] = 0  # Undo move
                
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    
    return best_move

def computer_move():
    """Make a move for the computer"""
    move = get_best_move()
    
    if move:
        pygame.time.delay(400)  # Small delay to make it feel more natural
        mark_square(move[0], move[1], 2)
        click_sound.play()
        
        if check_win(2):
            scores["O"] += 1
            win_sound.play()
            return True
        
        if is_board_full():
            scores["Ties"] += 1
            draw_sound.play()
            return True
    
    return False

# Main game loop
running = True
while running:
    if show_menu:
        buttons = draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_menu_click(buttons, event.pos)
    else:
        if not game_over:
            draw_lines()
            draw_figures()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                elif event.key == pygame.K_m:
                    show_menu = True
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    mouseX = event.pos[0]
                    mouseY = event.pos[1] - 100  # Adjust for scoreboard space
                    
                    if 0 <= mouseY < HEIGHT - 100:  # Check if click is within board area
                        clicked_row = mouseY // SQUARE_SIZE
                        clicked_col = mouseX // SQUARE_SIZE
                        
                        if is_available(clicked_row, clicked_col):
                            mark_square(clicked_row, clicked_col, player)
                            
                            if check_win(player):
                                if player == 1:
                                    scores["X"] += 1
                                else:
                                    scores["O"] += 1
                                draw_win_line(player)
                                win_sound.play()
                                game_over = True
                            elif is_board_full():
                                scores["Ties"] += 1
                                draw_sound.play()
                                game_over = True
                            else:
                                player = 2 if player == 1 else 1
                                
                                # Computer's turn
                                if vs_computer and player == 2 and not game_over:
                                    if computer_move():
                                        draw_win_line(2)
                                        game_over = True
                                    else:
                                        player = 1
        
        if game_over:
            draw_game_over()
    
    pygame.display.update()

pygame.quit()
sys.exit()
