import streamlit as st
import random
import time
import datetime
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Add background image and custom CSS for better appearance
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }}

        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .main-container {{
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin: 20px;
        }}

        .header {{
            font-size: 3.5rem;
            font-weight: 800;
            color: #1E1E2F;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            background: linear-gradient(90deg, #1E1E2F, #4A4A8F);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subheader {{
            font-size: 1.5rem;
            color: #333;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }}

        .board-row {{
            display: flex;
            justify-content: center;
        }}

        .board-cell {{
            width: 100px;
            height: 100px;
            border: 3px solid #1E1E2F;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: bold;
            cursor: pointer;
            margin: 4px;
            border-radius: 12px;
            background-color: rgba(255, 255, 255, 0.8);
            color: #333;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}

        .board-cell:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            background-color: rgba(255, 255, 255, 0.95);
        }}

        .score-panel {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 1.5rem 0;
            padding: 15px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        .score-card {{
            text-align: center;
            padding: 12px 24px;
            border-radius: 12px;
            min-width: 100px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}

        .score-card:hover {{
            transform: translateY(-5px);
        }}

        .score-x {{
            background: linear-gradient(135deg, #43cea2, #185a9d);
            color: white;
        }}

        .score-o {{
            background: linear-gradient(135deg, #ff9966, #ff5e62);
            color: white;
        }}

        .score-ties {{
            background: linear-gradient(135deg, #8e9eab, #eef2f3);
            color: #333;
        }}

        .game-message {{
            text-align: center;
            font-size: 1.5rem;
            margin: 1.5rem 0;
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}

        .win {{
            background: linear-gradient(135deg, #56ab2f, #a8e063);
            color: white;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}

        .draw {{
            background: linear-gradient(135deg, #bdc3c7, #2c3e50);
            color: white;
        }}

        .button-row {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 1.5rem 0;
        }}

        .footer {{
            text-align: center;
            margin-top: 2rem;
            color: white;
            padding: 10px;
            border-radius: 10px;
            background-color: rgba(0, 0, 0, 0.5);
        }}

        .difficulty-selector {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1.5rem 0;
        }}

        /* Styling for Streamlit components */
        div.stButton > button {{
            border-radius: 10px;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}

        div.stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }}

        /* Game cell button styling */
        [data-testid="stHorizontalBlock"] div.stButton > button {{
            height: 100px;
            font-size: 2.5rem;
            background-color: rgba(255, 255, 255, 0.8);
            border: 3px solid #1E1E2F;
            border-radius: 12px;
        }}

        [data-testid="stHorizontalBlock"] div.stButton > button:hover:not([disabled]) {{
            background-color: rgba(255, 255, 255, 0.95);
            transform: translateY(-5px);
        }}

        /* Winning cell styling */
        .winning-highlight {{
            padding: 0;
            margin: 0;
            border-radius: 12px;
            animation: winner-pulse 1.5s infinite;
        }}

        .winning-highlight button {{
            background-color: rgba(144, 238, 144, 0.8) !important;
            border-color: #2e7d32 !important;
        }}

        @keyframes winner-pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(50, 205, 50, 0.7); }}
            70% {{ box-shadow: 0 0 0 15px rgba(50, 205, 50, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(50, 205, 50, 0); }}
        }}

        /* Game history section */
        .history-panel {{
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 15px;
            padding: 15px;
            margin-top: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        .history-title {{
            font-size: 1.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
            color: #1E1E2F;
        }}

        .history-item {{
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        /* Timer styling */
        .timer {{
            text-align: center;
            font-size: 1.2rem;
            margin: 1rem 0;
            padding: 8px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.7);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}

        /* Move counter styling */
        .move-counter {{
            text-align: center;
            font-size: 1rem;
            margin: 0.5rem 0;
            color: #333;
        }}

        /* Mode toggle styling */
        .mode-toggle {{
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }}

        /* Player name input styling */
        .player-name-input {{
            margin: 1rem 0;
            padding: 10px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.7);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}

        /* Hover effect for cells */
        .board-cell:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            background-color: rgba(255, 255, 255, 0.95);
        }}

        /* Responsive design for mobile */
        @media (max-width: 768px) {{
            .board-cell {{
                width: 80px;
                height: 80px;
                font-size: 2rem;
            }}

            .header {{
                font-size: 2.5rem;
            }}

            .score-panel {{
                flex-direction: column;
                gap: 0.5rem;
            }}

            .button-row {{
                flex-direction: column;
                gap: 0.5rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background and container styling
add_bg_from_url()

# Create a container for the main content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Add game title and description
st.markdown("""
    <div class="header">Tic Tac Toe</div>
    <div class="subheader">A modern take on the classic game of X's and O's</div>
""", unsafe_allow_html=True)

# Initialize session state if it doesn't exist
if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
if 'turn' not in st.session_state:
    st.session_state.turn = 'X'
if 'scores' not in st.session_state:
    st.session_state.scores = {'X': 0, 'O': 0, 'Ties': 0}
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'vs_computer' not in st.session_state:
    st.session_state.vs_computer = True
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'medium'
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'game_start_time' not in st.session_state:
    st.session_state.game_start_time = time.time()
if 'move_count' not in st.session_state:
    st.session_state.move_count = 0
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'player_x_name' not in st.session_state:
    st.session_state.player_x_name = "Player X"
if 'player_o_name' not in st.session_state:
    st.session_state.player_o_name = "Computer" if st.session_state.vs_computer else "Player O"
if 'winning_combo' not in st.session_state:
    st.session_state.winning_combo = []

# Game functions
def check_winner(board):
    """Check if there's a winner or a tie"""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] != ' ' and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            st.session_state.winning_combo = combo  # Store the winning combination
            return board[combo[0]]

    if ' ' not in board:
        return 'Tie'

    return None

def minimax(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    """Minimax algorithm with alpha-beta pruning for AI moves"""
    winner = check_winner(board)

    if winner == 'O':  # AI wins
        return 10 - depth
    elif winner == 'X':  # AI loses
        return depth - 10
    elif winner == 'Tie':  # Draw
        return 0

    if is_maximizing:  # AI's turn (O)
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:  # Player's turn (X)
        min_eval = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def get_best_move(board, difficulty):
    """Get the best move for the AI based on difficulty"""
    empty_cells = [i for i, cell in enumerate(board) if cell == ' ']

    if not empty_cells:
        return None

    if difficulty == 'easy':
        # Random move
        return random.choice(empty_cells)

    elif difficulty == 'medium':
        # 60% chance of optimal move, 40% random
        if random.random() > 0.4:
            return get_best_move_minimax(board)
        else:
            return random.choice(empty_cells)

    else:  # Hard
        return get_best_move_minimax(board)

def get_best_move_minimax(board):
    """Get the best move using minimax algorithm"""
    best_score = -float('inf')
    best_move = None

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                best_move = i

    return best_move

def make_move(cell_idx):
    """Handle making a move on the board"""
    if st.session_state.board[cell_idx] == ' ' and not st.session_state.game_over:
        # Increment move counter
        st.session_state.move_count += 1

        # Make the move
        st.session_state.board[cell_idx] = st.session_state.turn

        # Check for winner after player move
        winner = check_winner(st.session_state.board)
        if winner is not None:
            handle_game_over(winner)
            return

        # Switch turns
        st.session_state.turn = 'O' if st.session_state.turn == 'X' else 'X'

        # Computer's turn
        if st.session_state.turn == 'O' and st.session_state.vs_computer and not st.session_state.game_over:
            # Add a small delay to simulate computer thinking
            time.sleep(0.5)

            computer_move = get_best_move(st.session_state.board, st.session_state.difficulty)
            if computer_move is not None:
                # Increment move counter for computer's move
                st.session_state.move_count += 1

                # Make the computer's move
                st.session_state.board[computer_move] = 'O'

                # Check for winner after computer move
                winner = check_winner(st.session_state.board)
                if winner is not None:
                    handle_game_over(winner)
                    return

                # Switch back to player
                st.session_state.turn = 'X'

def handle_game_over(winner):
    """Handle game over state and update scores"""
    st.session_state.game_over = True
    st.session_state.winner = winner

    # Calculate game duration
    game_duration = time.time() - st.session_state.game_start_time
    minutes, seconds = divmod(int(game_duration), 60)
    time_str = f"{minutes:02d}:{seconds:02d}"

    # Determine winner name for history
    if winner == 'Tie':
        winner_name = "Tie"
        st.session_state.scores['Ties'] += 1
    else:
        if winner == 'X':
            winner_name = st.session_state.player_x_name
        else:  # winner == 'O'
            winner_name = st.session_state.player_o_name
        st.session_state.scores[winner] += 1

    # Add game to history
    game_record = {
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'winner': winner_name,
        'moves': st.session_state.move_count,
        'duration': time_str,
        'mode': "vs Computer" if st.session_state.vs_computer else "vs Player",
        'difficulty': st.session_state.difficulty if st.session_state.vs_computer else "N/A"
    }

    # Add to history (limit to last 10 games)
    st.session_state.game_history.insert(0, game_record)
    if len(st.session_state.game_history) > 10:
        st.session_state.game_history = st.session_state.game_history[:10]

def reset_game():
    """Reset the game board but keep scores"""
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.turn = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.move_count = 0
    st.session_state.game_start_time = time.time()
    st.session_state.winning_combo = []

    # Update player names based on game mode
    if st.session_state.vs_computer:
        st.session_state.player_o_name = "Computer"

def reset_all():
    """Reset everything including scores"""
    reset_game()
    st.session_state.scores = {'X': 0, 'O': 0, 'Ties': 0}
    st.session_state.game_history = []

# Dark/Light mode toggle
mode_col1, mode_col2 = st.columns([4, 1])
with mode_col2:
    if st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle"):
        st.session_state.dark_mode = True
        # Apply dark mode CSS (would be implemented in a real app)
    else:
        st.session_state.dark_mode = False

# Player name customization
with st.expander("⚙️ Game Settings", expanded=False):
    name_col1, name_col2 = st.columns(2)
    with name_col1:
        new_player_x_name = st.text_input("Player X Name:", value=st.session_state.player_x_name, key="player_x_name_input")
        if new_player_x_name != st.session_state.player_x_name:
            st.session_state.player_x_name = new_player_x_name

    with name_col2:
        if not st.session_state.vs_computer:
            new_player_o_name = st.text_input("Player O Name:", value=st.session_state.player_o_name, key="player_o_name_input")
            if new_player_o_name != st.session_state.player_o_name:
                st.session_state.player_o_name = new_player_o_name

# Game mode selection
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button('😎 Player vs Computer' if not st.session_state.vs_computer else '😎 Player vs Computer ✓',
                 use_container_width=True,
                 type="primary" if st.session_state.vs_computer else "secondary"):
        st.session_state.vs_computer = True
        st.session_state.player_o_name = "Computer"
        reset_game()

with col2:
    if st.button('👥 Player vs Player' if st.session_state.vs_computer else '👥 Player vs Player ✓',
                 use_container_width=True,
                 type="primary" if not st.session_state.vs_computer else "secondary"):
        st.session_state.vs_computer = False
        st.session_state.player_o_name = "Player O"
        reset_game()

# Difficulty selection (only shown when playing against computer)
if st.session_state.vs_computer:
    st.markdown("<div class='difficulty-selector'></div>", unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        if st.button('🟢 Easy' if st.session_state.difficulty != 'easy' else '🟢 Easy ✓',
                     use_container_width=True,
                     type="primary" if st.session_state.difficulty == 'easy' else "secondary"):
            st.session_state.difficulty = 'easy'
            reset_game()

    with cols[1]:
        if st.button('🟡 Medium' if st.session_state.difficulty != 'medium' else '🟡 Medium ✓',
                     use_container_width=True,
                     type="primary" if st.session_state.difficulty == 'medium' else "secondary"):
            st.session_state.difficulty = 'medium'
            reset_game()

    with cols[2]:
        if st.button('🔴 Hard' if st.session_state.difficulty != 'hard' else '🔴 Hard ✓',
                     use_container_width=True,
                     type="primary" if st.session_state.difficulty == 'hard' else "secondary"):
            st.session_state.difficulty = 'hard'
            reset_game()

# Display scores with player names
st.markdown(f"""
    <div class="score-panel">
        <div class="score-card score-x">
            <div style="font-weight: bold;">{st.session_state.player_x_name}</div>
            <div style="font-size: 1.5rem;">{st.session_state.scores['X']}</div>
        </div>
        <div class="score-card score-ties">
            <div style="font-weight: bold;">Ties</div>
            <div style="font-size: 1.5rem;">{st.session_state.scores['Ties']}</div>
        </div>
        <div class="score-card score-o">
            <div style="font-weight: bold;">{st.session_state.player_o_name}</div>
            <div style="font-size: 1.5rem;">{st.session_state.scores['O']}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Display game timer and move counter
if not st.session_state.game_over:
    # Calculate current game time
    current_time = time.time() - st.session_state.game_start_time
    minutes, seconds = divmod(int(current_time), 60)
    time_str = f"{minutes:02d}:{seconds:02d}"

    timer_col, move_col = st.columns(2)
    with timer_col:
        st.markdown(f"""
            <div class="timer">
                ⏱️ Game Time: {time_str}
            </div>
        """, unsafe_allow_html=True)

    with move_col:
        st.markdown(f"""
            <div class="timer">
                🔢 Moves: {st.session_state.move_count}
            </div>
        """, unsafe_allow_html=True)

# Game status message
if st.session_state.game_over:
    if st.session_state.winner == 'Tie':
        st.markdown(f"""
            <div class="game-message draw">
                🏁 Game Over: It's a Draw! 🤝
            </div>
        """, unsafe_allow_html=True)
    else:
        winner_name = st.session_state.player_x_name if st.session_state.winner == 'X' else st.session_state.player_o_name
        st.markdown(f"""
            <div class="game-message win">
                🏆 Game Over: {winner_name} Wins! 🎉
            </div>
        """, unsafe_allow_html=True)

        # Show confetti effect for wins (simulated with CSS animation)
        st.markdown("""
            <style>
            @keyframes confetti {
                0% { background-position: 0 0; }
                100% { background-position: 100% 100%; }
            }
            .win {
                background-image: linear-gradient(135deg, #56ab2f, #a8e063, #56ab2f);
                background-size: 200% 200%;
                animation: pulse 2s infinite, confetti 3s infinite;
            }
            </style>
        """, unsafe_allow_html=True)
else:
    current_player = f"{st.session_state.player_x_name}'s turn (X)" if st.session_state.turn == 'X' else f"{st.session_state.player_o_name}'s turn (O)"

    # Add a pulsing effect to indicate whose turn it is
    st.markdown(f"""
        <div class="game-message" style="background-color: {('#e0f7f3' if st.session_state.turn == 'X' else '#ffecb3')};">
            🎲 {current_player}
        </div>
    """, unsafe_allow_html=True)

    # Add instruction text
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px; color: #555; font-style: italic;">
            Click on any empty cell to place your mark
        </div>
    """, unsafe_allow_html=True)

# Game board with winning cell highlighting and button-based interaction
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        cell_idx = row * 3 + col
        cell_value = st.session_state.board[cell_idx]

        # Custom styling for X and O with modern symbols
        if cell_value == 'X':
            symbol = "❌"
        elif cell_value == 'O':
            symbol = "⭕"
        else:
            symbol = " "

        # Check if this cell is part of the winning combination
        is_winning_cell = cell_idx in st.session_state.winning_combo

        # Use Streamlit buttons for each cell
        with cols[col]:
            # Add a CSS class for winning cells
            if is_winning_cell:
                st.markdown(f'<div class="winning-highlight">', unsafe_allow_html=True)

            # Create a button with custom styling
            if cell_value == ' ' and not st.session_state.game_over:
                # Empty cell - clickable
                if st.button(
                    " ",
                    key=f"cell_{cell_idx}",
                    use_container_width=True,
                    help=f"Click to place {st.session_state.turn}"
                ):
                    make_move(cell_idx)
            else:
                # Cell with value or game over - display only
                st.button(
                    symbol,
                    key=f"cell_{cell_idx}",
                    use_container_width=True,
                    disabled=True
                )

            # Close the winning cell div if needed
            if is_winning_cell:
                st.markdown('</div>', unsafe_allow_html=True)

# Buttons for game control with improved styling
st.markdown("<div class='button-row'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 New Game", use_container_width=True):
        reset_game()
with col2:
    if st.button("🗑️ Reset Scores", use_container_width=True):
        reset_all()
with col3:
    # Add a hint button
    if st.button("💡 Hint", use_container_width=True, disabled=st.session_state.game_over or not st.session_state.vs_computer):
        # In a real implementation, this would show a hint
        pass
st.markdown("</div>", unsafe_allow_html=True)

# Game History Section
st.markdown("<div class='history-panel'>", unsafe_allow_html=True)
st.markdown("<div class='history-title'>📜 Game History</div>", unsafe_allow_html=True)

if not st.session_state.game_history:
    st.markdown("<p style='text-align: center; color: #666;'>No games played yet</p>", unsafe_allow_html=True)
else:
    # Create a table for game history
    history_cols = st.columns([2, 2, 1, 1, 2, 2])
    history_cols[0].markdown("<b>Date</b>", unsafe_allow_html=True)
    history_cols[1].markdown("<b>Winner</b>", unsafe_allow_html=True)
    history_cols[2].markdown("<b>Moves</b>", unsafe_allow_html=True)
    history_cols[3].markdown("<b>Time</b>", unsafe_allow_html=True)
    history_cols[4].markdown("<b>Mode</b>", unsafe_allow_html=True)
    history_cols[5].markdown("<b>Difficulty</b>", unsafe_allow_html=True)

    for game in st.session_state.game_history:
        cols = st.columns([2, 2, 1, 1, 2, 2])
        cols[0].markdown(f"{game['date']}")
        cols[1].markdown(f"{game['winner']}")
        cols[2].markdown(f"{game['moves']}")
        cols[3].markdown(f"{game['duration']}")
        cols[4].markdown(f"{game['mode']}")
        cols[5].markdown(f"{game['difficulty']}")

st.markdown("</div>", unsafe_allow_html=True)

# Close the main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>Created by Asadullah48 | © 2025</p>
        <p>Enhanced with modern UI/UX design</p>
        <p>Play on desktop for the best experience</p>
    </div>
""", unsafe_allow_html=True)