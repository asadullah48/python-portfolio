import streamlit as st
import math
import random
import time

# Set page config
st.set_page_config(
    page_title="Advanced Tic Tac Toe",
    page_icon="🎮",
    layout="centered",
)

# Define constants
BOARD_ROWS = 3
BOARD_COLS = 3

# Initialize session state variables if they don't exist
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'ai_score' not in st.session_state:
    st.session_state.ai_score = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Hard"
if 'player_mark' not in st.session_state:
    st.session_state.player_mark = "X"
if 'ai_mark' not in st.session_state:
    st.session_state.ai_mark = "O"
if 'moves_count' not in st.session_state:
    st.session_state.moves_count = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# Game logic functions
def available_moves(board):
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == ""]

def is_winner(board, player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_COLS)):
        return True
    if all(board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_COLS)):
        return True
    return False

def is_board_full(board):
    return all(board[row][col] != "" for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    player_mark = st.session_state.player_mark
    ai_mark = st.session_state.ai_mark
    
    # Terminal conditions
    if is_winner(board, ai_mark):
        return {"score": 10 - depth}
    elif is_winner(board, player_mark):
        return {"score": depth - 10}
    elif is_board_full(board):
        return {"score": 0}
    
    # Depth limit for easier difficulties
    if st.session_state.difficulty == "Easy" and depth >= 1:
        return {"score": 0}
    elif st.session_state.difficulty == "Medium" and depth >= 3:
        return {"score": 0}
    
    if is_maximizing:
        best = {"score": -math.inf}
        for (r, c) in available_moves(board):
            board[r][c] = ai_mark
            score = minimax(board, depth + 1, False, alpha, beta)
            board[r][c] = ""
            score["move"] = (r, c)
            
            if score["score"] > best["score"]:
                best = score
            
            alpha = max(alpha, best["score"])
            if beta <= alpha:
                break
                
        return best
    else:
        best = {"score": math.inf}
        for (r, c) in available_moves(board):
            board[r][c] = player_mark
            score = minimax(board, depth + 1, True, alpha, beta)
            board[r][c] = ""
            score["move"] = (r, c)
            
            if score["score"] < best["score"]:
                best = score
                
            beta = min(beta, best["score"])
            if beta <= alpha:
                break
                
        return best

def make_ai_move():
    if st.session_state.game_over:
        return

    if st.session_state.difficulty == "Easy" and random.random() < 0.3:
        # 30% chance of making a random move in easy mode
        moves = available_moves(st.session_state.board)
        if moves:
            r, c = random.choice(moves)
    else:
        # Use minimax with different depths based on difficulty
        result = minimax(st.session_state.board, 0, True)
        r, c = result["move"]
    
    st.session_state.board[r][c] = st.session_state.ai_mark
    st.session_state.moves_count += 1
    st.session_state.history.append((r, c, st.session_state.ai_mark))
    
    check_game_status(st.session_state.ai_mark)

def check_game_status(player):
    if is_winner(st.session_state.board, player):
        st.session_state.game_over = True
        st.session_state.winner = player
        if player == st.session_state.player_mark:
            st.session_state.player_score += 1
        else:
            st.session_state.ai_score += 1
    elif is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        st.session_state.draws += 1

def handle_click(r, c):
    # If cell is already filled or game is over, do nothing
    if st.session_state.board[r][c] != "" or st.session_state.game_over:
        return
    
    # Player's move
    st.session_state.board[r][c] = st.session_state.player_mark
    st.session_state.moves_count += 1
    st.session_state.history.append((r, c, st.session_state.player_mark))
    
    check_game_status(st.session_state.player_mark)
    
    # AI's move
    if not st.session_state.game_over:
        with st.spinner("AI is thinking..."):
            # Small delay to make it feel more natural
            time.sleep(0.5)
            make_ai_move()

def restart_game():
    st.session_state.board = [["" for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.moves_count = 0
    st.session_state.history = []

def reset_scores():
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draws = 0
    restart_game()

def switch_marks():
    st.session_state.player_mark, st.session_state.ai_mark = st.session_state.ai_mark, st.session_state.player_mark
    restart_game()

# UI Code
st.title("🎮 Advanced Tic Tac Toe")
st.markdown("Play against an unbeatable AI opponent!")

# Sidebar for game settings
with st.sidebar:
    st.header("Game Settings")
    new_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], 
                             index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty))
    
    if new_difficulty != st.session_state.difficulty:
        st.session_state.difficulty = new_difficulty
        restart_game()
    
    st.button("Switch X/O", on_click=switch_marks)
    st.button("Reset Scores", on_click=reset_scores)
    
    st.subheader("Scoreboard")
    st.markdown(f"**You ({st.session_state.player_mark}):** {st.session_state.player_score}")
    st.markdown(f"**AI ({st.session_state.ai_mark}):** {st.session_state.ai_score}")
    st.markdown(f"**Draws:** {st.session_state.draws}")
    
    st.subheader("Game Statistics")
    st.markdown(f"**Moves in this game:** {st.session_state.moves_count}")
    
    st.subheader("Move History")
    history_text = ""
    for i, (r, c, player) in enumerate(st.session_state.history):
        history_text += f"{i+1}. {player} at row {r+1}, col {c+1}\n"
    st.text_area("", history_text, height=150, disabled=True)

# Game status display
if st.session_state.game_over:
    if st.session_state.winner == st.session_state.player_mark:
        st.success("🎉 Congratulations! You won!")
    elif st.session_state.winner == st.session_state.ai_mark:
        st.error("💔 AI wins this round!")
    else:
        st.info("🤝 It's a draw!")
    
    if st.button("Play Again"):
        restart_game()

# Game board UI
st.markdown("### Game Board")
col1, col2 = st.columns([3, 1])

with col1:
    # Create a 3x3 grid of buttons for the game board
    for r in range(BOARD_ROWS):
        cols = st.columns(3)
        for c in range(BOARD_COLS):
            cell_value = st.session_state.board[r][c]
            cell_style = ""
            
            if cell_value == st.session_state.player_mark:
                cell_style = "color: blue; font-weight: bold;"
            elif cell_value == st.session_state.ai_mark:
                cell_style = "color: red; font-weight: bold;"
            
            if cell_value:
                cols[c].markdown(f"<h1 style='text-align: center; {cell_style}'>{cell_value}</h1>", unsafe_allow_html=True)
            else:
                if cols[c].button(" ", key=f"{r}{c}", on_click=handle_click, args=(r, c)):
                    pass
                    
with col2:
    st.markdown(f"**Your mark:** {st.session_state.player_mark}")
    st.markdown(f"**AI mark:** {st.session_state.ai_mark}")
    st.markdown(f"**Difficulty:** {st.session_state.difficulty}")
    
    if st.button("Restart Game"):
        restart_game()

# Instructions
with st.expander("How to Play"):
    st.markdown("""
    ### Rules:
    1. The game is played on a 3x3 grid.
    2. You are X, and the AI is O (or vice versa if you switch).
    3. Players take turns putting their marks in empty squares.
    4. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins.
    5. If all squares are filled and no one has 3 in a row, the game is a draw.
    
    ### Difficulty Levels:
    - **Easy**: The AI occasionally makes random moves and limits its look-ahead.
    - **Medium**: The AI uses strategy but doesn't look too far ahead.
    - **Hard**: The AI is unbeatable and uses the minimax algorithm to find the best move.
    """)

# Footer
st.markdown("---")
st.markdown("Created by Asadullah48 | GitHub: [asadullah48](https://github.com/asadullah48)")