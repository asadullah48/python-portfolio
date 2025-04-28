import streamlit as st
import math
import random
import time
import pandas as pd
from datetime import datetime
import sqlite3
import os

# Set page config
st.set_page_config(
    page_title="Advanced Tic Tac Toe",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define constants
BOARD_ROWS = 3
BOARD_COLS = 3

# Define themes
THEMES = {
    "Classic": {
        "bg_color": "#f0f2f6",
        "player_color": "#1E88E5",
        "ai_color": "#E53935",
        "board_bg": "#FFFFFF",
        "board_lines": "#2C3E50",
        "hover_color": "#E3F2FD",
    },
    "Dark": {
        "bg_color": "#121212",
        "player_color": "#64B5F6",
        "ai_color": "#FF8A65",
        "board_bg": "#1E1E1E",
        "board_lines": "#BBBBBB",
        "hover_color": "#263238",
    },
    "Neon": {
        "bg_color": "#0a0a0a",
        "player_color": "#00FFFF",
        "ai_color": "#FF00FF",
        "board_bg": "#000000",
        "board_lines": "#39FF14",
        "hover_color": "#1F2833",
    },
    "Pastel": {
        "bg_color": "#F5F5F5",
        "player_color": "#95E1D3",
        "ai_color": "#F38181",
        "board_bg": "#FFFFFF",
        "board_lines": "#A8D8EA",
        "hover_color": "#E3FDFD",
    }
}

# Initialize database
def init_db():
    if not os.path.exists('tictactoe.db'):
        conn = sqlite3.connect('tictactoe.db')
        c = conn.cursor()

        # Create game history table
        c.execute('''
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            difficulty TEXT,
            winner TEXT,
            moves INTEGER,
            duration REAL
        )
        ''')

        # Create achievements table
        c.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            icon TEXT
        )
        ''')

        # Insert default achievements
        achievements = [
            ('First Win', 'Win your first game against the AI', '🏆'),
            ('Master Strategist', 'Win a game on Hard difficulty', '🧠'),
            ('Speed Demon', 'Win a game in less than 10 seconds', '⚡'),
            ('Hat Trick', 'Win 3 games in a row', '🎩'),
            ('Persistence', 'Play 10 games', '🔄')
        ]
        c.executemany('INSERT INTO achievements (name, description, icon) VALUES (?, ?, ?)', achievements)

        # Create player achievements table
        c.execute('''
        CREATE TABLE IF NOT EXISTS player_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            achievement_id INTEGER,
            date_earned TEXT,
            FOREIGN KEY (achievement_id) REFERENCES achievements (id)
        )
        ''')

        conn.commit()
        conn.close()

# Call init_db to ensure database exists
init_db()

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
if 'game_start_time' not in st.session_state:
    st.session_state.game_start_time = time.time()
if 'theme' not in st.session_state:
    st.session_state.theme = "Classic"
if 'sound_effects' not in st.session_state:
    st.session_state.sound_effects = True
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'win_streak' not in st.session_state:
    st.session_state.win_streak = 0

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

def check_achievements():
    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()

    # Get all achievements
    c.execute('SELECT id, name, description, icon FROM achievements')
    all_achievements = c.fetchall()

    # Get player's earned achievements
    c.execute('SELECT achievement_id FROM player_achievements')
    earned_ids = [row[0] for row in c.fetchall()]

    new_achievements = []

    # Check for first win
    if st.session_state.winner == st.session_state.player_mark and 1 not in earned_ids:
        c.execute('INSERT INTO player_achievements (achievement_id, date_earned) VALUES (?, ?)',
                 (1, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        new_achievements.append(all_achievements[0])

    # Check for win on hard difficulty
    if (st.session_state.winner == st.session_state.player_mark and
        st.session_state.difficulty == "Hard" and 2 not in earned_ids):
        c.execute('INSERT INTO player_achievements (achievement_id, date_earned) VALUES (?, ?)',
                 (2, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        new_achievements.append(all_achievements[1])

    # Check for speed win (less than 10 seconds)
    game_duration = time.time() - st.session_state.game_start_time
    if (st.session_state.winner == st.session_state.player_mark and
        game_duration < 10 and 3 not in earned_ids):
        c.execute('INSERT INTO player_achievements (achievement_id, date_earned) VALUES (?, ?)',
                 (3, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        new_achievements.append(all_achievements[2])

    # Check for 3 wins in a row
    if st.session_state.win_streak >= 3 and 4 not in earned_ids:
        c.execute('INSERT INTO player_achievements (achievement_id, date_earned) VALUES (?, ?)',
                 (4, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        new_achievements.append(all_achievements[3])

    # Check for 10 games played
    if st.session_state.games_played >= 10 and 5 not in earned_ids:
        c.execute('INSERT INTO player_achievements (achievement_id, date_earned) VALUES (?, ?)',
                 (5, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        new_achievements.append(all_achievements[4])

    conn.commit()
    conn.close()

    return new_achievements

def save_game_history():
    game_duration = time.time() - st.session_state.game_start_time
    winner = "Player" if st.session_state.winner == st.session_state.player_mark else (
        "AI" if st.session_state.winner == st.session_state.ai_mark else "Draw")

    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO game_history (date, difficulty, winner, moves, duration)
    VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          st.session_state.difficulty,
          winner,
          st.session_state.moves_count,
          game_duration))
    conn.commit()
    conn.close()

def check_game_status(player):
    if is_winner(st.session_state.board, player):
        st.session_state.game_over = True
        st.session_state.winner = player
        if player == st.session_state.player_mark:
            st.session_state.player_score += 1
            st.session_state.win_streak += 1
        else:
            st.session_state.ai_score += 1
            st.session_state.win_streak = 0

        # Save game history
        save_game_history()

        # Check for achievements
        st.session_state.new_achievements = check_achievements()

    elif is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        st.session_state.draws += 1
        st.session_state.win_streak = 0

        # Save game history
        save_game_history()

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
    st.session_state.game_start_time = time.time()
    st.session_state.games_played += 1
    if 'new_achievements' in st.session_state:
        st.session_state.new_achievements = []

def reset_scores():
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draws = 0
    st.session_state.win_streak = 0
    restart_game()

def switch_marks():
    st.session_state.player_mark, st.session_state.ai_mark = st.session_state.ai_mark, st.session_state.player_mark
    restart_game()

def change_theme(new_theme):
    st.session_state.theme = new_theme

def toggle_sound():
    st.session_state.sound_effects = not st.session_state.sound_effects

def get_game_stats():
    conn = sqlite3.connect('tictactoe.db')
    df = pd.read_sql_query("SELECT * FROM game_history", conn)
    conn.close()

    if len(df) == 0:
        return None

    stats = {
        "total_games": len(df),
        "wins": len(df[df['winner'] == 'Player']),
        "losses": len(df[df['winner'] == 'AI']),
        "draws": len(df[df['winner'] == 'Draw']),
        "avg_moves": df['moves'].mean(),
        "avg_duration": df['duration'].mean(),
        "win_rate": len(df[df['winner'] == 'Player']) / len(df) * 100 if len(df) > 0 else 0,
        "by_difficulty": df.groupby('difficulty')['winner'].value_counts().unstack().fillna(0).to_dict()
    }

    return stats

def get_achievements():
    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()

    # Get all achievements with earned status
    c.execute('''
    SELECT a.id, a.name, a.description, a.icon,
           CASE WHEN pa.id IS NULL THEN 0 ELSE 1 END as earned,
           pa.date_earned
    FROM achievements a
    LEFT JOIN player_achievements pa ON a.id = pa.achievement_id
    ORDER BY a.id
    ''')

    achievements = []
    for row in c.fetchall():
        achievements.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "icon": row[3],
            "earned": bool(row[4]),
            "date_earned": row[5]
        })

    conn.close()
    return achievements

# Apply custom CSS based on the selected theme
theme = THEMES[st.session_state.theme]

# Custom CSS for styling
st.markdown(f"""
<style>
    /* Main background */
    .stApp {{
        background: {theme["bg_color"]};
    }}

    /* Game board styling */
    .game-board {{
        background-color: {theme["board_bg"]};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
    }}

    /* Cell styling */
    .board-cell {{
        width: 100%;
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        border: 2px solid {theme["board_lines"]};
        transition: all 0.3s ease;
    }}

    /* Player mark styling */
    .player-mark {{
        color: {theme["player_color"]};
    }}

    /* AI mark styling */
    .ai-mark {{
        color: {theme["ai_color"]};
    }}

    /* Hover effect for empty cells */
    .board-cell:hover {{
        background-color: {theme["hover_color"]};
        cursor: pointer;
    }}

    /* Achievement card styling */
    .achievement-card {{
        background-color: {theme["board_bg"]};
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        border-left: 4px solid {theme["player_color"]};
        transition: transform 0.2s ease;
    }}

    .achievement-card:hover {{
        transform: translateY(-2px);
    }}

    .achievement-locked {{
        opacity: 0.5;
        border-left: 4px solid gray;
    }}

    /* Stats card styling */
    .stats-card {{
        background-color: {theme["board_bg"]};
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    /* Custom button styling */
    .custom-button {{
        background-color: {theme["player_color"]};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }}

    .custom-button:hover {{
        opacity: 0.9;
        transform: translateY(-2px);
    }}

    /* Scoreboard styling */
    .scoreboard {{
        display: flex;
        justify-content: space-between;
        background-color: {theme["board_bg"]};
        border-radius: 8px;
        padding: 10px 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    .score-item {{
        text-align: center;
        padding: 10px;
    }}

    .score-value {{
        font-size: 1.8rem;
        font-weight: bold;
    }}

    .score-label {{
        font-size: 0.9rem;
        opacity: 0.8;
    }}

    /* Winner announcement styling */
    .winner-announcement {{
        text-align: center;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        font-size: 1.5rem;
        font-weight: bold;
    }}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: {theme["board_bg"]};
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {theme["player_color"]};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

# UI Code
st.title("🎮 Advanced Tic Tac Toe")
st.markdown("Play against an AI opponent with adjustable difficulty levels!")

# Main layout
main_col1, main_col2 = st.columns([2, 1])

# Game board and controls in the left column
with main_col1:
    # Game status display
    if st.session_state.game_over:
        if st.session_state.winner == st.session_state.player_mark:
            st.markdown(f"""
            <div class="winner-announcement" style="background-color: rgba(0, 200, 81, 0.2);">
                🎉 Congratulations! You won!
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.winner == st.session_state.ai_mark:
            st.markdown(f"""
            <div class="winner-announcement" style="background-color: rgba(255, 76, 76, 0.2);">
                💔 AI wins this round!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="winner-announcement" style="background-color: rgba(100, 149, 237, 0.2);">
                🤝 It's a draw!
            </div>
            """, unsafe_allow_html=True)

        # Show new achievements if any
        if 'new_achievements' in st.session_state and st.session_state.new_achievements:
            st.markdown("### 🏆 New Achievements Unlocked!")
            for achievement in st.session_state.new_achievements:
                st.markdown(f"""
                <div class="achievement-card">
                    <h3>{achievement[3]} {achievement[1]}</h3>
                    <p>{achievement[2]}</p>
                </div>
                """, unsafe_allow_html=True)

    # Scoreboard
    st.markdown(f"""
    <div class="scoreboard">
        <div class="score-item">
            <div class="score-value" style="color: {theme['player_color']};">{st.session_state.player_score}</div>
            <div class="score-label">You ({st.session_state.player_mark})</div>
        </div>
        <div class="score-item">
            <div class="score-value">{st.session_state.draws}</div>
            <div class="score-label">Draws</div>
        </div>
        <div class="score-item">
            <div class="score-value" style="color: {theme['ai_color']};">{st.session_state.ai_score}</div>
            <div class="score-label">AI ({st.session_state.ai_mark})</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Game board
    st.markdown('<div class="game-board">', unsafe_allow_html=True)

    # Create a 3x3 grid for the game board
    for r in range(BOARD_ROWS):
        cols = st.columns(3)
        for c in range(BOARD_COLS):
            cell_value = st.session_state.board[r][c]

            with cols[c]:
                if cell_value == st.session_state.player_mark:
                    st.markdown(f"""
                    <div class="board-cell">
                        <span class="player-mark">{cell_value}</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif cell_value == st.session_state.ai_mark:
                    st.markdown(f"""
                    <div class="board-cell">
                        <span class="ai-mark">{cell_value}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button(" ", key=f"{r}{c}", on_click=handle_click, args=(r, c)):
                        pass

    st.markdown('</div>', unsafe_allow_html=True)

    # Game controls
    controls_col1, controls_col2, controls_col3 = st.columns(3)

    with controls_col1:
        if st.button("🔄 New Game", key="new_game"):
            restart_game()

    with controls_col2:
        if st.button("🔀 Switch X/O", key="switch"):
            switch_marks()

    with controls_col3:
        if st.button("🧹 Reset Scores", key="reset"):
            reset_scores()

# Sidebar for game settings and statistics
with main_col2:
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["⚙️ Settings", "📊 Statistics", "🏆 Achievements"])

    with tab1:
        st.subheader("Game Settings")

        # Difficulty selection
        new_difficulty = st.select_slider(
            "AI Difficulty",
            options=["Easy", "Medium", "Hard"],
            value=st.session_state.difficulty
        )

        if new_difficulty != st.session_state.difficulty:
            st.session_state.difficulty = new_difficulty
            restart_game()

        # Theme selection
        new_theme = st.selectbox(
            "Theme",
            options=list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.theme)
        )

        if new_theme != st.session_state.theme:
            change_theme(new_theme)
            st.experimental_rerun()

        # Sound effects toggle
        sound_enabled = st.toggle("Sound Effects", value=st.session_state.sound_effects)
        if sound_enabled != st.session_state.sound_effects:
            toggle_sound()

        # Game information
        st.subheader("Current Game")
        st.markdown(f"**Moves made:** {st.session_state.moves_count}")

        game_duration = time.time() - st.session_state.game_start_time
        minutes, seconds = divmod(int(game_duration), 60)
        st.markdown(f"**Game duration:** {minutes:02d}:{seconds:02d}")

        # Move history
        st.subheader("Move History")
        if st.session_state.history:
            for i, (r, c, player) in enumerate(st.session_state.history):
                st.markdown(f"**{i+1}.** {player} at row {r+1}, col {c+1}")
        else:
            st.markdown("No moves yet.")

    with tab2:
        st.subheader("Game Statistics")

        # Get game stats from database
        stats = get_game_stats()

        if stats:
            # Display overall stats
            st.markdown(f"""
            <div class="stats-card">
                <h4>Overall Performance</h4>
                <p>Total Games: {stats['total_games']}</p>
                <p>Win Rate: {stats['win_rate']:.1f}%</p>
                <p>Average Moves per Game: {stats['avg_moves']:.1f}</p>
                <p>Average Game Duration: {stats['avg_duration']:.1f} seconds</p>
            </div>
            """, unsafe_allow_html=True)

            # Create win/loss/draw chart
            win_loss_data = pd.DataFrame({
                'Result': ['Wins', 'Losses', 'Draws'],
                'Count': [stats['wins'], stats['losses'], stats['draws']]
            })

            st.subheader("Win/Loss Distribution")
            st.bar_chart(win_loss_data.set_index('Result'))

            # Display difficulty breakdown if available
            if stats['by_difficulty']:
                st.subheader("Performance by Difficulty")
                for difficulty, results in stats['by_difficulty'].items():
                    st.markdown(f"**{difficulty}:** {results}")
        else:
            st.info("Play some games to see your statistics!")

    with tab3:
        st.subheader("Achievements")

        # Get achievements from database
        achievements = get_achievements()

        for achievement in achievements:
            if achievement['earned']:
                st.markdown(f"""
                <div class="achievement-card">
                    <h4>{achievement['icon']} {achievement['name']}</h4>
                    <p>{achievement['description']}</p>
                    <small>Earned on: {achievement['date_earned']}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="achievement-card achievement-locked">
                    <h4>🔒 {achievement['name']}</h4>
                    <p>{achievement['description']}</p>
                </div>
                """, unsafe_allow_html=True)

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

    ### Achievements:
    Complete special challenges to unlock achievements and track your progress!
    """)

# Footer
st.markdown("---")
st.markdown("Created by Asadullah48 | GitHub: [asadullah48](https://github.com/asadullah48)")