import streamlit as st
import numpy as np
import time
import random
import pandas as pd
from copy import deepcopy
import base64
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Sudoku Solver Pro",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Function to add background image
def add_bg_from_base64(base64_string):
    return f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """

# Light blue gradient background
@st.cache_data
def get_base64_gradient():
    gradient = """
    iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==
    """
    return gradient

# Apply background and custom CSS
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}

    .main {{
        padding: 2rem;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.85);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        margin: 1rem;
    }}

    .stSidebar {{
        background-color: rgba(255, 255, 255, 0.9);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}

    .st-emotion-cache-1kyxreq {{
        justify-content: center;
    }}

    h1, h2, h3 {{
        color: #1E3A8A;
        font-weight: 600;
    }}

    .sudoku-grid {{
        border: 3px solid #1E3A8A;
        margin: 0 auto;
        border-radius: 5px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        background-color: white;
    }}

    .sudoku-grid td {{
        width: 45px;
        height: 45px;
        text-align: center;
        font-size: 22px;
        border: 1px solid #ddd;
        transition: all 0.2s ease;
    }}

    .sudoku-grid td:nth-child(3n) {{
        border-right: 2px solid #1E3A8A;
    }}

    .sudoku-grid tr:nth-child(3n) td {{
        border-bottom: 2px solid #1E3A8A;
    }}

    .original {{
        font-weight: bold;
        color: #1E3A8A;
    }}

    .user-input {{
        color: #3B82F6;
        font-weight: 500;
    }}

    .selected {{
        background-color: #DBEAFE;
        transform: scale(1.05);
        box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
    }}

    .invalid {{
        background-color: #FEE2E2;
        color: #DC2626;
    }}

    .hint {{
        background-color: #D1FAE5;
        color: #059669;
    }}

    .same-row-col-box {{
        background-color: #F3F4F6;
    }}

    .stMetric {{
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}

    .stExpander {{
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}

    /* Custom number buttons */
    .number-button {{
        display: inline-block;
        width: 40px;
        height: 40px;
        line-height: 40px;
        text-align: center;
        margin: 5px;
        background-color: #3B82F6;
        color: white;
        border-radius: 50%;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    .number-button:hover {{
        transform: scale(1.1);
        background-color: #2563EB;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}

    /* Footer styling */
    .footer {{
        text-align: center;
        padding: 20px;
        color: #6B7280;
        font-size: 14px;
    }}

    /* Success message styling */
    .success-message {{
        background-color: #D1FAE5;
        border-left: 5px solid #059669;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(5, 150, 105, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(5, 150, 105, 0); }}
    }}

    /* Dark mode toggle */
    .dark-mode-toggle {{
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }}
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
# New features
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'notes_mode' not in st.session_state:
    st.session_state.notes_mode = False
if 'notes' not in st.session_state:
    st.session_state.notes = np.empty((9, 9), dtype=object)
    for i in range(9):
        for j in range(9):
            st.session_state.notes[i, j] = set()
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = True
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'highlight_related' not in st.session_state:
    st.session_state.highlight_related = True
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "blue"

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

def get_related_cells(row, col):
    """Get all cells in the same row, column, and box as the selected cell."""
    related_cells = []

    # Same row
    for j in range(9):
        if j != col:
            related_cells.append((row, j))

    # Same column
    for i in range(9):
        if i != row:
            related_cells.append((i, col))

    # Same box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i != row or j != col) and (i, j) not in related_cells:
                related_cells.append((i, j))

    return related_cells

def toggle_note(row, col, num):
    """Toggle a note in the selected cell."""
    if num in st.session_state.notes[row, col]:
        st.session_state.notes[row, col].remove(num)
    else:
        st.session_state.notes[row, col].add(num)

def clear_notes_for_cell(row, col):
    """Clear all notes for a cell."""
    st.session_state.notes[row, col] = set()

def auto_notes():
    """Automatically fill in notes for all empty cells."""
    for i in range(9):
        for j in range(9):
            if st.session_state.board[i, j] == 0:
                st.session_state.notes[i, j] = set()
                for num in range(1, 10):
                    if is_valid(st.session_state.board, i, j, num):
                        st.session_state.notes[i, j].add(num)

def save_game_stats():
    """Save the current game statistics to history."""
    if st.session_state.game_active and st.session_state.game_completed:
        elapsed_time = st.session_state.elapsed_time if 'elapsed_time' in st.session_state else 0
        game_stats = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'difficulty': st.session_state.difficulty,
            'time': elapsed_time,
            'hints': st.session_state.hints_used,
            'mistakes': st.session_state.mistakes,
            'completed': check_win(st.session_state.board)
        }
        st.session_state.game_history.append(game_stats)

def apply_theme(theme_name):
    """Apply a color theme to the game."""
    st.session_state.current_theme = theme_name

    # Theme colors will be applied via CSS classes

# Sidebar
with st.sidebar:
    st.title("🧩 Sudoku Pro")
    st.markdown("---")

    # Game controls section
    st.subheader("Game Controls")

    # Difficulty selection
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard", "Expert"],
        index=["Easy", "Medium", "Hard", "Expert"].index(st.session_state.difficulty)
    )

    # New Game button
    if st.button("New Game 🎮", key="new_game_btn"):
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
        # Reset notes
        st.session_state.notes = np.empty((9, 9), dtype=object)
        for i in range(9):
            for j in range(9):
                st.session_state.notes[i, j] = set()

    # Game action buttons
    col1, col2 = st.columns(2)

    # Hint button
    if col1.button("Hint 💡", key="hint_btn"):
        if st.session_state.game_active and not st.session_state.game_completed:
            hint = get_hint()
            if hint:
                i, j, value = hint
                st.session_state.board[i][j] = value
                st.session_state.hints_used += 1
                clear_notes_for_cell(i, j)

                # Check if the game is won after using the hint
                if check_win(st.session_state.board):
                    st.session_state.game_completed = True
                    save_game_stats()

    # Reset button
    if col2.button("Reset 🔄", key="reset_btn"):
        if st.session_state.game_active:
            st.session_state.board = st.session_state.original_board.copy()
            st.session_state.hints_used = 0
            st.session_state.mistakes = 0
            st.session_state.start_time = time.time()
            st.session_state.game_completed = False
            # Reset notes
            st.session_state.notes = np.empty((9, 9), dtype=object)
            for i in range(9):
                for j in range(9):
                    st.session_state.notes[i, j] = set()

    # Solve button
    if st.button("Solve Puzzle 🔍", key="solve_btn"):
        if st.session_state.game_active and not st.session_state.game_completed:
            st.session_state.board = st.session_state.solution.copy()
            st.session_state.game_completed = True
            save_game_stats()

    # Notes features
    st.markdown("---")
    st.subheader("Notes Features")

    # Notes mode toggle
    notes_mode = st.toggle("Notes Mode 📝", st.session_state.notes_mode)
    if notes_mode != st.session_state.notes_mode:
        st.session_state.notes_mode = notes_mode

    # Auto-notes button
    if st.button("Auto Notes 🤖", key="auto_notes_btn"):
        if st.session_state.game_active and not st.session_state.game_completed:
            auto_notes()

    # Clear all notes button
    if st.button("Clear All Notes 🧹", key="clear_notes_btn"):
        if st.session_state.game_active:
            for i in range(9):
                for j in range(9):
                    st.session_state.notes[i, j] = set()

    # Settings section
    st.markdown("---")
    st.subheader("Settings")

    # Theme selection
    theme = st.selectbox(
        "Theme",
        ["Blue", "Green", "Purple", "Dark"],
        index=["Blue", "Green", "Purple", "Dark"].index(st.session_state.current_theme.capitalize())
    )
    if theme.lower() != st.session_state.current_theme:
        apply_theme(theme.lower())

    # Highlight related cells toggle
    highlight = st.toggle("Highlight Related Cells", st.session_state.highlight_related)
    if highlight != st.session_state.highlight_related:
        st.session_state.highlight_related = highlight

    # Timer toggle
    timer = st.toggle("Timer Active", st.session_state.timer_active)
    if timer != st.session_state.timer_active:
        st.session_state.timer_active = timer

    # Game stats
    if st.session_state.game_active:
        st.markdown("---")
        st.subheader("Game Stats")

        # Timer
        if not st.session_state.game_completed and st.session_state.timer_active:
            elapsed_time = time.time() - st.session_state.start_time
        else:
            elapsed_time = st.session_state.elapsed_time if 'elapsed_time' in st.session_state else 0

        st.metric("Time", format_time(elapsed_time))

        # Hints and mistakes
        col1, col2 = st.columns(2)
        col1.metric("Hints Used", st.session_state.hints_used)
        col2.metric("Mistakes", st.session_state.mistakes)

    # Game history
    if st.session_state.game_history:
        st.markdown("---")
        with st.expander("Game History 📊"):
            history_df = pd.DataFrame(st.session_state.game_history)
            if not history_df.empty:
                history_df['time'] = history_df['time'].apply(format_time)
                st.dataframe(history_df, use_container_width=True)

# Main game area
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.title("Sudoku Solver Pro 🧩")

# Dark/Light mode toggle in the top right
col1, col2 = st.columns([6, 1])
with col2:
    dark_mode = st.toggle("🌙", st.session_state.dark_mode, key="dark_mode_toggle")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        # Apply dark mode CSS dynamically
        if dark_mode:
            st.markdown("""
            <style>
                .stApp {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                }
                .main {
                    background-color: rgba(30, 30, 50, 0.85);
                }
                .stSidebar {
                    background-color: rgba(30, 30, 50, 0.9);
                }
                h1, h2, h3 {
                    color: #e2e8f0;
                }
                .sudoku-grid {
                    border: 3px solid #4f46e5;
                    background-color: #1e293b;
                }
                .sudoku-grid td {
                    border: 1px solid #334155;
                }
                .sudoku-grid td:nth-child(3n) {
                    border-right: 2px solid #4f46e5;
                }
                .sudoku-grid tr:nth-child(3n) td {
                    border-bottom: 2px solid #4f46e5;
                }
                .original {
                    color: #e2e8f0;
                }
                .user-input {
                    color: #60a5fa;
                }
                .selected {
                    background-color: #1e40af;
                }
                .same-row-col-box {
                    background-color: #1e293b;
                }
                .stMetric {
                    background-color: #1e293b;
                }
            </style>
            """, unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown("""
    <div style='text-align: center; padding: 20px; margin: 20px 0; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px;'>
        <h2>👋 Welcome to Sudoku Solver Pro!</h2>
        <p style='font-size: 18px;'>Select a difficulty level and click 'New Game' to start playing.</p>
    </div>
    """, unsafe_allow_html=True)

    # Features showcase
    st.markdown("## ✨ Features")
    feature_cols = st.columns(3)

    with feature_cols[0]:
        st.markdown("""
        ### 🎮 Game Features
        - Four difficulty levels
        - Real-time validation
        - Game timer with pause
        - Hint system
        - Game history tracking
        """)

    with feature_cols[1]:
        st.markdown("""
        ### 📝 Notes System
        - Manual notes mode
        - Auto-notes feature
        - Clear notes option
        - Visual note display
        """)

    with feature_cols[2]:
        st.markdown("""
        ### 🎨 UI Features
        - Dark/Light mode
        - Multiple color themes
        - Highlight related cells
        - Responsive design
        """)

    # How to play
    with st.expander("How to Play"):
        st.markdown("""
        ### Basic Rules
        1. Fill the 9×9 grid with digits 1-9
        2. Each row must contain all digits 1-9 without repetition
        3. Each column must contain all digits 1-9 without repetition
        4. Each 3×3 box must contain all digits 1-9 without repetition

        ### Controls
        - Click on a cell to select it
        - Use number buttons to fill the selected cell
        - Toggle "Notes Mode" to add small notes in cells
        - Use "Hint" when you're stuck (counts against your score)
        - "Auto Notes" will fill in all possible candidates
        """)

    # Sample board display
    st.markdown("## Sample Puzzle")
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
    # Game header with difficulty and status
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
        <h3>Difficulty: {st.session_state.difficulty}</h3>
        <div style='background-color: {"#D1FAE5" if not st.session_state.game_completed else "#FEF3C7"};
                    padding: 5px 15px;
                    border-radius: 20px;
                    color: {"#059669" if not st.session_state.game_completed else "#D97706"};
                    font-weight: bold;'>
            {"In Progress" if not st.session_state.game_completed else "Completed"}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Check if game is completed
    if st.session_state.game_completed:
        if 'elapsed_time' not in st.session_state:
            st.session_state.elapsed_time = time.time() - st.session_state.start_time

        if check_win(st.session_state.board):
            st.markdown(f"""
            <div class='success-message'>
                <h3>🎉 Congratulations!</h3>
                <p>You solved the puzzle in {format_time(st.session_state.elapsed_time)} with {st.session_state.hints_used} hints used and {st.session_state.mistakes} mistakes made.</p>
            </div>
            """, unsafe_allow_html=True)
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

            # Highlight related cells if enabled
            if st.session_state.highlight_related and st.session_state.selected_cell:
                selected_row, selected_col = st.session_state.selected_cell
                if (i == selected_row or j == selected_col or
                    (i // 3 == selected_row // 3 and j // 3 == selected_col // 3)) and (i, j) != (selected_row, selected_col):
                    cell_class += " same-row-col-box"

            # Add cell content (value or notes)
            cell_content = ""
            if current_value != 0:
                cell_content = current_value
            elif len(st.session_state.notes[i, j]) > 0:
                # Display notes in a 3x3 grid
                notes_grid = "<div class='notes-container'>"
                for num in range(1, 10):
                    note_class = "note-value" if num in st.session_state.notes[i, j] else "note-empty"
                    notes_grid += f"<div class='note {note_class}'>{num if num in st.session_state.notes[i, j] else ''}</div>"
                notes_grid += "</div>"
                cell_content = notes_grid

            # Add cell with appropriate value and class
            table_html += f"<td id='cell-{i}-{j}' class='{cell_class}'>{cell_content}</td>"

        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Game controls
    if not st.session_state.game_completed:
        # Number input buttons with improved styling
        st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)

        # Mode indicator
        mode_text = "Notes Mode" if st.session_state.notes_mode else "Number Mode"
        mode_color = "#059669" if st.session_state.notes_mode else "#2563EB"
        st.markdown(f"""
        <div style='margin-bottom: 15px; background-color: {mode_color}; color: white;
                    display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold;'>
            {mode_text}
        </div>
        """, unsafe_allow_html=True)

        # Number buttons
        st.markdown("<div style='display: flex; justify-content: center; flex-wrap: wrap;'>", unsafe_allow_html=True)
        for i in range(9):
            if st.button(str(i + 1), key=f"num_{i+1}", use_container_width=False):
                if st.session_state.selected_cell:
                    row, col = st.session_state.selected_cell
                    if st.session_state.original_board[row][col] == 0:  # Only modify non-original cells
                        if st.session_state.notes_mode:
                            # Toggle note for the selected number
                            toggle_note(row, col, i + 1)
                        else:
                            # Clear notes for this cell
                            clear_notes_for_cell(row, col)

                            # Update the board and check for mistakes
                            st.session_state.board[row][col] = i + 1

                            if st.session_state.solution[row][col] != i + 1:
                                st.session_state.mistakes += 1

                            # Check if the game is won
                            if check_win(st.session_state.board):
                                st.session_state.game_completed = True
                                st.session_state.elapsed_time = time.time() - st.session_state.start_time
                                save_game_stats()
        st.markdown("</div>", unsafe_allow_html=True)

        # Cell selection and clear buttons
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            row_input = st.selectbox("Row", list(range(1, 10)), key="row_select")

        with col2:
            col_input = st.selectbox("Column", list(range(1, 10)), key="col_select")

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Select", key="select_cell_btn"):
                st.session_state.selected_cell = (row_input - 1, col_input - 1)

        # Clear and keyboard shortcuts
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Clear Cell", key="clear_cell_btn"):
                if st.session_state.selected_cell:
                    row, col = st.session_state.selected_cell
                    if st.session_state.original_board[row][col] == 0:  # Only clear non-original cells
                        st.session_state.board[row][col] = 0
                        clear_notes_for_cell(row, col)

        with col2:
            if st.button("Clear Notes", key="clear_cell_notes_btn"):
                if st.session_state.selected_cell:
                    row, col = st.session_state.selected_cell
                    clear_notes_for_cell(row, col)

        # Keyboard shortcuts info
        with st.expander("Keyboard Shortcuts"):
            st.markdown("""
            - Use number keys (1-9) to enter numbers
            - Press 'Delete' or '0' to clear a cell
            - Press 'N' to toggle notes mode
            - Press arrow keys to navigate the grid
            """)

    # Add a message about using the sidebar for more options
    st.markdown("""
    <div style='text-align: center; margin-top: 30px; padding: 10px;
              background-color: rgba(59, 130, 246, 0.1); border-radius: 5px;'>
        <p>💡 Use the sidebar for more game options and settings!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Add CSS for notes display
st.markdown("""
<style>
    .notes-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        width: 100%;
        height: 100%;
        font-size: 10px;
    }

    .note {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

    .note-value {
        color: #6B7280;
        font-size: 10px;
    }

    .note-empty {
        color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>📱 Made with ❤️ by Asadullah48</p>
    <p>Enhanced with professional UI/UX and new features</p>
    <p>© 2025 Sudoku Solver Pro</p>
</div>
""", unsafe_allow_html=True)