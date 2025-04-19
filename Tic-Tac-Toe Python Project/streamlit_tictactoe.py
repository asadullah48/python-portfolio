import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E6B5A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
    }
    .board-row {
        display: flex;
        justify-content: center;
    }
    .board-cell {
        width: 100px;
        height: 100px;
        border: 3px solid #1E6B5A;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        cursor: pointer;
        margin: 4px;
        border-radius: 8px;
        background-color: #e0f7f3;
        color: #333;
    }
    .board-cell:hover {
        background-color: #b0e0d6;
    }
    .score-panel {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 10px;
    }
    .score-card {
        text-align: center;
        padding: 10px 20px;
        border-radius: 8px;
        min-width: 100px;
    }
    .score-x {
        background-color: #dcedc8;
    }
    .score-o {
        background-color: #ffecb3;
    }
    .score-ties {
        background-color: #e0e0e0;
    }
    .game-message {
        text-align: center;
        font-size: 1.5rem;
        margin: 1.5rem 0;
        padding: 8px;
        border-radius: 8px;
    }
    .win {
        background-color: #a5d6a7;
        color: #2e7d32;
    }
    .draw {
        background-color: #e0e0e0;
        color: #616161;
    }
    .button-row {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
    }
    .difficulty-selector {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    <div class="header">Tic Tac Toe 🎮</div>
    <div class="subheader">A classic game of X's and O's</div>
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
    
    if winner == 'Tie':
        st.session_state.scores['Ties'] += 1
    else:
        st.session_state.scores[winner] += 1

def reset_game():
    """Reset the game board but keep scores"""
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.turn = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def reset_all():
    """Reset everything including scores"""
    reset_game()
    st.session_state.scores = {'X': 0, 'O': 0, 'Ties': 0}

# Game mode selection
col1, col2 = st.columns(2)
with col1:
    if st.button('😎 Player vs Computer' if not st.session_state.vs_computer else '😎 Player vs Computer ✓', 
                 use_container_width=True, 
                 type="primary" if st.session_state.vs_computer else "secondary"):
        st.session_state.vs_computer = True
        reset_game()

with col2:
    if st.button('👥 Player vs Player' if st.session_state.vs_computer else '👥 Player vs Player ✓', 
                 use_container_width=True, 
                 type="primary" if not st.session_state.vs_computer else "secondary"):
        st.session_state.vs_computer = False
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

# Display scores
st.markdown(f"""
    <div class="score-panel">
        <div class="score-card score-x">
            <div style="font-weight: bold;">Player X</div>
            <div style="font-size: 1.5rem;">{st.session_state.scores['X']}</div>
        </div>
        <div class="score-card score-ties">
            <div style="font-weight: bold;">Ties</div>
            <div style="font-size: 1.5rem;">{st.session_state.scores['Ties']}</div>
        </div>
        <div class="score-card score-o">
            <div style="font-weight: bold;">Player O</div>
            <div style="font-size: 1.5rem;">{st.session_state.scores['O']}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Game status message
if st.session_state.game_over:
    if st.session_state.winner == 'Tie':
        st.markdown(f"""
            <div class="game-message draw">
                Game Over: It's a Draw!
            </div>
        """, unsafe_allow_html=True)
    else:
        winner_name = f"Player {st.session_state.winner}" if not st.session_state.vs_computer or st.session_state.winner == 'X' else "Computer"
        st.markdown(f"""
            <div class="game-message win">
                Game Over: {winner_name} Wins! 🎉
            </div>
        """, unsafe_allow_html=True)
else:
    current_player = "Your turn (X)" if st.session_state.turn == 'X' else "Player O's turn" if not st.session_state.vs_computer else "Computer's turn (O)"
    st.markdown(f"""
        <div class="game-message">
            {current_player}
        </div>
    """, unsafe_allow_html=True)

# Game board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        cell_idx = row * 3 + col
        cell_value = st.session_state.board[cell_idx]
        
        # Custom styling for X and O
        if cell_value == 'X':
            symbol = "❌"
        elif cell_value == 'O':
            symbol = "⭕"
        else:
            symbol = " "
        
        # Render the cell button with the current value
        with cols[col]:
            st.markdown(f"""
                <div class="board-cell" id="cell-{cell_idx}" onclick="handleCellClick({cell_idx})">
                    {symbol}
                </div>
            """, unsafe_allow_html=True)
    
    # Add JavaScript for handling clicks
    st.markdown("""
        <script>
        function handleCellClick(idx) {
            // Use Streamlit's component communication
            const data = { cellIndex: idx };
            window.parent.postMessage(
                {type: "streamlit:cellClick", data: data}, "*"
            );
        }
        </script>
    """, unsafe_allow_html=True)

# Custom component for cell clicks
from streamlit.components.v1 import html

cell_click_html = """
<script>
window.addEventListener("message", function(event) {
    if (event.data.type === "streamlit:cellClick") {
        const cellIndex = event.data.data.cellIndex;
        window.parent.postMessage({
            type: "streamlit:setValue",
            target: "clicked_cell",
            value: cellIndex
        }, "*");
    }
});
</script>
"""

# Invisible component to capture clicks
html(cell_click_html, height=0)

# Handle cell clicks
if "clicked_cell" in st.session_state:
    make_move(st.session_state.clicked_cell)
    del st.session_state.clicked_cell

# Buttons for game control
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 New Game", use_container_width=True):
        reset_game()
with col2:
    if st.button("🗑️ Reset Scores", use_container_width=True):
        reset_all()

# Footer
st.markdown("""
    <div class="footer">
        <p>Created by Asadullah48 | © 2025</p>
        <p>Play on desktop for the best experience</p>
    </div>
""", unsafe_allow_html=True)    