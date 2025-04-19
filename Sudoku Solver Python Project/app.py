import streamlit as st
import numpy as np
import time
import random
import pandas as pd
from copy import deepcopy

# Set page configuration
st.set_page_config(
    page_title="Sudoku Solver",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Apply some custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .st-emotion-cache-1kyxreq {
        justify-content: center;
    }
    .sudoku-grid {
        border: 2px solid black;
        margin: 0 auto;
    }
    .sudoku-grid td {
        width: 40px;
        height: 40px;
        text-align: center;
        font-size: 20px;
        border: 1px solid #ddd;
    }
    .sudoku-grid td:nth-child(3n) {
        border-right: 2px solid black;
    }
    .sudoku-grid tr:nth-child(3n) td {
        border-bottom: 2px solid black;
    }
    .original {
        font-weight: bold;
        color: #000;
    }
    .user-input {
        color: #0068c9;
    }
    .selected {
        background-color: #f0f8ff;
    }
    .invalid {
        background-color: #ffcccc;
    }
    .hint {
        background-color: #d4edda;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)
if 'original_board' not in st.session_state:
    st.session_state.original_board = np.zeros((9, 9), dtype=int)
if 'selected_cell' not in st.session_state:
    st.session_state.selected_cell = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Medium"
if 'hints_used' not in st.session_state:
    st.session_state.hints_used = 0
if 'mistakes' not in st.session_state:
    st.session_state.mistakes = 0
if 'solution' not in st.session_state:
    st.session_state.solution = None
if 'game_completed' not in st.session_state:
    st.session_state.game_completed = False

# Sudoku solver functions
def is_valid(board, row, col, num):
    # Check row
    for x in range(9):
        if board[row][x] == num:
            return False
    
    # Check column
    for x in range(9):
        if board[x][col] == num:
            return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            # Backtrack if no solution found
            board[row][col] = 0
    
    return False

def generate_sudoku(difficulty):
    # Start with an empty board
    board = np.zeros((9, 9), dtype=int)
    
    # Solve the empty board to get a complete solution
    solution = board.copy()
    solve_sudoku(solution)
    
    # Make a copy of the solved board
    puzzle = solution.copy()
    
    # Define cells to remove based on difficulty
    if difficulty == "Easy":
        cells_to_remove = 40  # 41 filled cells
    elif difficulty == "Medium":
        cells_to_remove = 50  # 31 filled cells
    elif difficulty == "Hard":
        cells_to_remove = 60  # 21 filled cells
    else:  # Expert
        cells_to_remove = 65  # 16 filled cells
    
    # Randomly remove cells
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    for i, j in positions[:cells_to_remove]:
        puzzle[i][j] = 0
    
    return puzzle, solution

def check_win(board):
    # Check if the board is completely filled
    if 0 in board:
        return False
    
    # Check rows
    for row in range(9):
        if set(board[row]) != set(range(1, 10)):
            return False
    
    # Check columns
    for col in range(9):
        if set(board[:, col]) != set(range(1, 10)):
            return False
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    box.append(board[i][j])
            if set(box) != set(range(1, 10)):
                return False
    
    return True

def get_hint():
    if st.session_state.solution is None:
        return None
    
    # Find an empty cell or incorrect cell
    for i in range(9):
        for j in range(9):
            if st.session_state.board[i][j] == 0 or st.session_state.board[i][j] != st.session_state.solution[i][j]:
                return (i, j, st.session_state.solution[i][j])
    
    return None

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

# Sidebar
with st.sidebar:
    st.title("🧩 Sudoku Game")
    st.markdown("---")
    
    # Difficulty selection
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard", "Expert"],
        index=["Easy", "Medium", "Hard", "Expert"].index(st.session_state.difficulty)
    )
    
    # New Game button
    if st.button("New Game 🎮"):
        st.session_state.difficulty = difficulty
        puzzle, solution = generate_sudoku(difficulty)
        st.session_state.board = puzzle.copy()
        st.session_state.original_board = puzzle.copy()
        st.session_state.solution = solution
        st.session_state.start_time = time.time()
        st.session_state.game_active = True
        st.session_state.selected_cell = None
        st.session_state.hints_used = 0
        st.session_state.mistakes = 0
        st.session_state.game_completed = False
    
    # Hint button
    if st.button("Hint 💡"):
        if st.session_state.game_active and not st.session_state.game_completed:
            hint = get_hint()
            if hint:
                i, j, value = hint
                st.session_state.board[i][j] = value
                st.session_state.hints_used += 1
                
                # Check if the game is won after using the hint
                if check_win(st.session_state.board):
                    st.session_state.game_completed = True
    
    # Solve button
    if st.button("Solve Puzzle 🔍"):
        if st.session_state.game_active and not st.session_state.game_completed:
            st.session_state.board = st.session_state.solution.copy()
            st.session_state.game_completed = True
    
    # Reset button
    if st.button("Reset Puzzle 🔄"):
        if st.session_state.game_active:
            st.session_state.board = st.session_state.original_board.copy()
            st.session_state.hints_used = 0
            st.session_state.mistakes = 0
            st.session_state.start_time = time.time()
            st.session_state.game_completed = False
    
    # Game stats
    if st.session_state.game_active:
        st.markdown("---")
        st.subheader("Game Stats")
        
        # Timer
        if not st.session_state.game_completed:
            elapsed_time = time.time() - st.session_state.start_time
        else:
            elapsed_time = st.session_state.elapsed_time if 'elapsed_time' in st.session_state else 0
        
        st.metric("Time", format_time(elapsed_time))
        
        # Hints and mistakes
        col1, col2 = st.columns(2)
        col1.metric("Hints Used", st.session_state.hints_used)
        col2.metric("Mistakes", st.session_state.mistakes)

# Main game area
st.title("Sudoku Solver 🧩")

if not st.session_state.game_active:
    st.info("👋 Welcome to Sudoku Solver! Select a difficulty level and click 'New Game' to start playing.")
    
    # How to play
    with st.expander("How to Play"):
        st.write("""
        1. Click on a cell to select it
        2. Type a number (1-9) to fill the cell
        3. Press 'Delete' or '0' to clear a cell
        4. Use the 'Hint' button if you're stuck
        5. Complete the grid following these rules:
           - Each row must contain all numbers from 1-9 without repetition
           - Each column must contain all numbers from 1-9 without repetition
           - Each 3x3 box must contain all numbers from 1-9 without repetition
        """)
    
    # Sample board display
    sample_board = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    table_html = "<table class='sudoku-grid'>"
    for i in range(9):
        table_html += "<tr>"
        for j in range(9):
            value = sample_board[i, j]
            cell_class = "original" if value != 0 else ""
            table_html += f"<td class='{cell_class}'>{value if value != 0 else ''}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
else:
    # Check if game is completed
    if st.session_state.game_completed:
        if 'elapsed_time' not in st.session_state:
            st.session_state.elapsed_time = time.time() - st.session_state.start_time
        
        if check_win(st.session_state.board):
            st.success(f"🎉 Congratulations! You solved the puzzle in {format_time(st.session_state.elapsed_time)} with {st.session_state.hints_used} hints used and {st.session_state.mistakes} mistakes made.")
        else:
            st.info("Puzzle solved with assistance. Try again to solve it yourself!")
    
    # Display the current board
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    table_html = "<table class='sudoku-grid'>"
    for i in range(9):
        table_html += "<tr>"
        for j in range(9):
            original_value = st.session_state.original_board[i, j]
            current_value = st.session_state.board[i, j]
            
            # Determine cell class
            cell_class = "original" if original_value != 0 else "user-input"
            if st.session_state.selected_cell == (i, j):
                cell_class += " selected"
            
            # Add cell with appropriate value and class
            table_html += f"<td id='cell-{i}-{j}' class='{cell_class}'>{current_value if current_value != 0 else ''}</td>"
        
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Number input buttons
    if not st.session_state.game_completed:
        st.markdown("### Enter Number")
        cols = st.columns(9)
        for i in range(9):
            if cols[i].button(str(i + 1), key=f"num_{i+1}"):
                if st.session_state.selected_cell:
                    row, col = st.session_state.selected_cell
                    if st.session_state.original_board[row][col] == 0:  # Only modify non-original cells
                        # Check if the number is valid
                        temp_board = st.session_state.board.copy()
                        temp_board[row][col] = i + 1
                        
                        # Update the board and check for mistakes
                        st.session_state.board[row][col] = i + 1
                        
                        if st.session_state.solution[row][col] != i + 1:
                            st.session_state.mistakes += 1
                        
                        # Check if the game is won
                        if check_win(st.session_state.board):
                            st.session_state.game_completed = True
                            st.session_state.elapsed_time = time.time() - st.session_state.start_time
    
    # Interactive cell selection via text input (Streamlit workaround)
    st.markdown("### Select Cell")
    col1, col2 = st.columns(2)
    
    row_input = col1.selectbox("Row", list(range(1, 10)), key="row_select")
    col_input = col2.selectbox("Column", list(range(1, 10)), key="col_select")
    
    if st.button("Select Cell"):
        st.session_state.selected_cell = (row_input - 1, col_input - 1)
    
    if st.button("Clear Selected Cell"):
        if st.session_state.selected_cell:
            row, col = st.session_state.selected_cell
            if st.session_state.original_board[row][col] == 0:  # Only clear non-original cells
                st.session_state.board[row][col] = 0

# Footer
st.markdown("---")
st.markdown("📱 Made with ❤️ by Asadullah48")