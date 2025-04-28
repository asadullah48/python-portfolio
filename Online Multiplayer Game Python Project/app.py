import streamlit as st
import base64
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# Function to add background image
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            z-index: -1;
        }}
        .main {{
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }}
        .css-18e3th9 {{
            padding-top: 0;
        }}
        .css-1d391kg {{
            padding-top: 3.5rem;
        }}
        h1, h2, h3, h4, h5, h6, p, li {{
            color: white !important;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(50, 50, 50, 0.8);
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            color: white;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: rgba(100, 100, 255, 0.8) !important;
        }}
        .stButton>button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 4px;
            transition-duration: 0.4s;
        }}
        .stButton>button:hover {{
            background-color: #45a049;
        }}
        .download-btn {{
            background-color: #3498db !important;
        }}
        .download-btn:hover {{
            background-color: #2980b9 !important;
        }}
        .stDownloadButton>button {{
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 4px;
            transition-duration: 0.4s;
        }}
        .stDownloadButton>button:hover {{
            background-color: #2980b9;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('pong_game.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player1_name TEXT DEFAULT 'Player 1',
        player2_name TEXT DEFAULT 'Player 2',
        player1_score INTEGER DEFAULT 0,
        player2_score INTEGER DEFAULT 0,
        winner INTEGER,
        duration_seconds INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        condition_type TEXT NOT NULL,
        condition_value INTEGER NOT NULL,
        icon TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        achievement_id INTEGER NOT NULL,
        unlocked_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (achievement_id) REFERENCES achievements (id)
    )
    ''')

    # Insert default achievements if they don't exist
    cursor.execute('SELECT COUNT(*) FROM achievements')
    if cursor.fetchone()[0] == 0:
        achievements = [
            ('First Victory', 'Win your first game', 'wins', 1, '🏆'),
            ('Hat Trick', 'Win 3 games in a row', 'streak', 3, '🎩'),
            ('Sharpshooter', 'Score 10 points in a single game', 'score', 10, '🎯'),
            ('Marathon', 'Play for more than 5 minutes', 'time', 300, '⏱️'),
            ('Comeback King', 'Win after being down by 5 points', 'comeback', 5, '👑')
        ]
        cursor.executemany(
            'INSERT INTO achievements (name, description, condition_type, condition_value, icon) VALUES (?, ?, ?, ?, ?)',
            achievements
        )

    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Set page config
st.set_page_config(
    page_title="Multiplayer Pong Game",
    page_icon="🏓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply background
add_bg_from_url()

# Custom CSS for the title
st.markdown("""
<style>
.title {
    font-size: 3.5rem !important;
    color: white !important;
    text-align: center;
    text-shadow: 0 0 10px #00f, 0 0 20px #00f, 0 0 30px #00f;
    margin-bottom: 1rem;
}
.subtitle {
    font-size: 1.5rem !important;
    color: #ccc !important;
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Page title and description with custom styling
st.markdown('<h1 class="title">🏓 MULTIPLAYER PONG GAME</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">A real-time multiplayer implementation of the classic Pong game using Python, Pygame, and socket programming.</p>', unsafe_allow_html=True)

# Sidebar with enhanced options
st.sidebar.title("🎮 Game Options")

# Player customization section
st.sidebar.markdown("## 🎨 Player Customization")
player_name = st.sidebar.text_input("Your Name", value="Player 1")
paddle_color = st.sidebar.color_picker("Paddle Color", value="#3498db")
game_difficulty = st.sidebar.select_slider(
    "Game Difficulty",
    options=["Easy", "Normal", "Hard", "Expert"],
    value="Normal"
)

# Game settings
st.sidebar.markdown("## ⚙️ Game Settings")
ball_speed = st.sidebar.slider("Ball Speed", min_value=1, max_value=10, value=5)
enable_sound = st.sidebar.checkbox("Enable Sound Effects", value=True)
enable_powerups = st.sidebar.checkbox("Enable Power-ups", value=False)
game_mode = st.sidebar.radio(
    "Game Mode",
    options=["Classic", "Time Attack", "First to 10"],
    index=0
)

# Server settings
st.sidebar.markdown("## 🌐 Server Settings")
server_ip = st.sidebar.text_input("Server IP", value="localhost")
server_port = st.sidebar.number_input("Server Port", min_value=1000, max_value=9999, value=5555)

# Instructions
st.sidebar.markdown("## 📋 Instructions")
st.sidebar.markdown("""
1. Configure your game settings above
2. Download the game files using the links below
3. Install the requirements
4. First run the server, then run the client(s)
""")

# Create tabs with additional features
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 About", "🎮 Demo", "📊 Statistics", "🏆 Leaderboard", "🔧 Installation"])

# About tab
with tab1:
    col1, col2 = st.columns([3, 2])

    # Game description
    with col1:
        st.markdown("""
        ## About the Game

        This multiplayer Pong game is a modern implementation of the classic Atari game. It features:

        - 🌐 Real-time multiplayer over network
        - 🎮 Smooth gameplay with Pygame
        - 🏆 Score tracking
        - 🎯 Physics-based ball movement
        - 🖥️ Client-server architecture

        ## How to Play

        ### Controls:
        - **Player 1**:
            - W: Move paddle up
            - S: Move paddle down
        - **Player 2**:
            - Up Arrow: Move paddle up
            - Down Arrow: Move paddle down
        - **General**:
            - R: Reconnect if disconnected
            - ESC: Quit the game

        ## Technical Details

        The game uses:
        - Python 3.7+
        - Pygame for graphics
        - Socket programming for network communication
        - Threading for handling multiple connections
        - JSON for data serialization
        """)

    # Create a simple Pong game illustration
    with col2:
        fig, ax = plt.subplots(figsize=(6, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 15)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

        # Draw the court
        ax.add_patch(plt.Rectangle((0, 0), 10, 15, fill=True, color='black'))
        ax.plot([5, 5], [0, 15], 'w--', alpha=0.5)

        # Draw the paddles
        ax.add_patch(plt.Rectangle((0.5, 6), 0.5, 3, fill=True, color='blue'))
        ax.add_patch(plt.Rectangle((9, 8), 0.5, 3, fill=True, color='red'))

        # Draw the ball
        ax.add_patch(plt.Circle((6, 7.5), 0.5, fill=True, color='white'))

        # Add scores
        ax.text(2.5, 14, '3', color='white', fontsize=24, ha='center')
        ax.text(7.5, 14, '2', color='white', fontsize=24, ha='center')

        st.pyplot(fig)

        # Add a download section
        st.markdown("""
        ### Download Game Files
        """)

        st.download_button(
            label="⬇️ Download Client",
            data="# This would be the actual client.py file content in a real scenario",
            file_name="client.py",
            mime="text/plain",
        )

        st.download_button(
            label="⬇️ Download Server",
            data="# This would be the actual server.py file content in a real scenario",
            file_name="server.py",
            mime="text/plain",
        )

# Demo tab with enhanced interactive features
with tab2:
    st.markdown("## 🎮 Interactive Game Demo")

    # Create columns for the demo
    demo_col1, demo_col2 = st.columns([3, 2])

    with demo_col1:
        # Create a simple animated "GIF" of Pong gameplay with matplotlib
        frames = []
        ball_x, ball_y = 5, 7.5
        ball_dx, ball_dy = 0.4, 0.3
        paddle1_y, paddle2_y = 6, 8
        paddle1_dy, paddle2_dy = 0.2, -0.2

        # Use the selected paddle color from sidebar
        paddle_color_rgb = tuple(int(paddle_color.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))

        # Adjust ball speed based on selected difficulty
        speed_multiplier = {
            "Easy": 0.7,
            "Normal": 1.0,
            "Hard": 1.3,
            "Expert": 1.6
        }[game_difficulty]

        ball_dx *= speed_multiplier * (ball_speed / 5)
        ball_dy *= speed_multiplier * (ball_speed / 5)

        for i in range(30):  # Increased frame count for smoother animation
            fig, ax = plt.subplots(figsize=(6, 8))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 15)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])

            # Draw the court with a more professional look
            ax.add_patch(plt.Rectangle((0, 0), 10, 15, fill=True, color='#111111'))
            ax.plot([5, 5], [0, 15], 'w--', alpha=0.5)

            # Add court markings
            ax.add_patch(plt.Circle((5, 7.5), 2, fill=False, color='white', alpha=0.2))

            # Update paddle positions
            paddle1_y += paddle1_dy
            if paddle1_y <= 0 or paddle1_y >= 12:
                paddle1_dy = -paddle1_dy

            paddle2_y += paddle2_dy
            if paddle2_y <= 0 or paddle2_y >= 12:
                paddle2_dy = -paddle2_dy

            # Draw the paddles - use custom color for player 1
            ax.add_patch(plt.Rectangle((0.5, paddle1_y), 0.5, 3, fill=True, color=paddle_color_rgb))
            ax.add_patch(plt.Rectangle((9, paddle2_y), 0.5, 3, fill=True, color='red'))

            # Update ball position
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collisions
            if ball_y <= 0.5 or ball_y >= 14.5:
                ball_dy = -ball_dy

            # Paddle collisions with improved physics
            if (ball_x <= 1.5 and paddle1_y <= ball_y <= paddle1_y + 3):
                ball_dx = -ball_dx
                # Add angle based on where the ball hits the paddle
                ball_dy += (ball_y - (paddle1_y + 1.5)) * 0.1
            elif (ball_x >= 8.5 and paddle2_y <= ball_y <= paddle2_y + 3):
                ball_dx = -ball_dx
                # Add angle based on where the ball hits the paddle
                ball_dy += (ball_y - (paddle2_y + 1.5)) * 0.1

            # If ball goes out of bounds, reset
            if ball_x < 0 or ball_x > 10:
                # Flash effect for scoring
                if i > 0:  # Skip the first frame
                    ax.add_patch(plt.Rectangle((0, 0), 10, 15, fill=True, color='#333333'))
                ball_x, ball_y = 5, 7.5
                ball_dx = -ball_dx

            # Draw the ball with a slight glow effect
            ball_glow = plt.Circle((ball_x, ball_y), 0.7, fill=True, color='#444444', alpha=0.5)
            ball = plt.Circle((ball_x, ball_y), 0.5, fill=True, color='white')
            ax.add_patch(ball_glow)
            ax.add_patch(ball)

            # Add scores
            ax.text(2.5, 14, '3', color='white', fontsize=24, ha='center')
            ax.text(7.5, 14, '2', color='white', fontsize=24, ha='center')

            # Add player names
            ax.text(2.5, 0.5, player_name, color='white', fontsize=12, ha='center')
            ax.text(7.5, 0.5, "Computer", color='white', fontsize=12, ha='center')

            # Convert to image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)
            img = Image.open(buf)
            frames.append(np.array(img))
            plt.close(fig)

        # Display frames as an animation
        st.image(frames, width=600)

    with demo_col2:
        st.markdown("### Game Controls")

        # Interactive controls demo
        st.markdown("""
        Try the controls below to see how they would work in the game:
        """)

        # Simulated paddle movement
        st.markdown("#### Move Your Paddle")
        col_up, col_down = st.columns(2)
        with col_up:
            if st.button("↑ UP (W)"):
                st.session_state.paddle_pos = max(0, st.session_state.get('paddle_pos', 5) - 1)
        with col_down:
            if st.button("↓ DOWN (S)"):
                st.session_state.paddle_pos = min(10, st.session_state.get('paddle_pos', 5) + 1)

        # Display paddle position
        paddle_pos = st.session_state.get('paddle_pos', 5)
        st.progress(paddle_pos / 10)

        st.markdown("### Game Features")
        st.markdown(f"""
        - **Current Mode**: {game_mode}
        - **Difficulty**: {game_difficulty}
        - **Ball Speed**: {ball_speed}/10
        - **Sound Effects**: {"Enabled" if enable_sound else "Disabled"}
        - **Power-ups**: {"Enabled" if enable_powerups else "Disabled"}
        """)

        st.markdown("### Live Demo")
        st.markdown("""
        Experience the game for yourself! Download the files and follow the installation instructions.
        """)

        # Quick start button
        if st.button("🚀 Quick Start Game", key="quick_start"):
            st.success("Game settings saved! Download the files below to start playing.")

        # Download buttons with custom styling
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #3498db;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

        # Download buttons in columns
        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                label="⬇️ Download Client",
                data="# This would be the actual client.py file content in a real scenario",
                file_name="client.py",
                mime="text/plain",
            )
        with dl_col2:
            st.download_button(
                label="⬇️ Download Server",
                data="# This would be the actual server.py file content in a real scenario",
                file_name="server.py",
                mime="text/plain",
            )

# Statistics tab
with tab3:
    st.markdown("## 📊 Game Statistics Dashboard")

    # Create mock data for demonstration
    def generate_mock_stats():
        if 'stats_generated' not in st.session_state:
            # Generate some mock game statistics
            conn = get_db_connection()
            cursor = conn.cursor()

            # Clear existing data for demo purposes
            cursor.execute('DELETE FROM game_stats')

            # Insert mock data
            mock_games = [
                ('Player 1', 'Computer', 11, 5, 1, 180, '2023-06-01 12:30:45'),
                ('Player 1', 'Friend', 7, 11, 2, 240, '2023-06-02 14:20:10'),
                ('Champion', 'Player 1', 11, 9, 1, 300, '2023-06-03 18:15:22'),
                ('Player 1', 'Computer', 11, 3, 1, 150, '2023-06-04 20:45:30'),
                ('Player 1', 'Friend', 5, 11, 2, 210, '2023-06-05 19:10:15'),
                ('Player 1', 'Computer', 11, 8, 1, 270, '2023-06-06 21:30:00'),
                ('Pro Gamer', 'Player 1', 11, 7, 1, 240, '2023-06-07 17:45:20'),
                ('Player 1', 'Computer', 9, 11, 2, 330, '2023-06-08 16:20:10'),
                ('Player 1', 'Friend', 11, 10, 1, 360, '2023-06-09 22:05:45'),
                ('Player 1', 'Computer', 11, 6, 1, 210, '2023-06-10 15:30:25')
            ]

            for game in mock_games:
                cursor.execute('''
                INSERT INTO game_stats
                (player1_name, player2_name, player1_score, player2_score, winner, duration_seconds, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', game)

            conn.commit()
            conn.close()
            st.session_state.stats_generated = True

    # Generate mock data
    generate_mock_stats()

    # Create tabs within the Statistics tab
    stats_tab1, stats_tab2, stats_tab3 = st.tabs(["Overview", "Performance", "History"])

    with stats_tab1:
        # Get statistics from database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get total games
        cursor.execute('SELECT COUNT(*) FROM game_stats')
        total_games = cursor.fetchone()[0]

        # Get wins and losses for Player 1
        cursor.execute('''
        SELECT
            SUM(CASE WHEN (player1_name = 'Player 1' AND winner = 1) OR (player2_name = 'Player 1' AND winner = 2) THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN (player1_name = 'Player 1' AND winner = 2) OR (player2_name = 'Player 1' AND winner = 1) THEN 1 ELSE 0 END) as losses
        FROM game_stats
        WHERE player1_name = 'Player 1' OR player2_name = 'Player 1'
        ''')
        result = cursor.fetchone()
        wins = result[0]
        losses = result[1]

        # Get average points per game
        cursor.execute('''
        SELECT
            AVG(CASE WHEN player1_name = 'Player 1' THEN player1_score ELSE player2_score END) as avg_score
        FROM game_stats
        WHERE player1_name = 'Player 1' OR player2_name = 'Player 1'
        ''')
        avg_score = cursor.fetchone()[0]

        # Get average game duration
        cursor.execute('SELECT AVG(duration_seconds) FROM game_stats')
        avg_duration = cursor.fetchone()[0]

        conn.close()

        # Display statistics in a nice layout
        st.subheader("Player Statistics")

        # Create metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Games", f"{total_games}")
        with col2:
            st.metric("Wins", f"{wins}", f"{wins/total_games*100:.1f}%")
        with col3:
            st.metric("Losses", f"{losses}", f"{losses/total_games*100:.1f}%")
        with col4:
            st.metric("Win Rate", f"{wins/total_games*100:.1f}%")

        # More detailed stats
        st.subheader("Game Performance")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Avg. Score", f"{avg_score:.1f} points")
            st.metric("Avg. Game Duration", f"{avg_duration/60:.1f} minutes")

        with col2:
            # Create a pie chart for win/loss ratio
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie([wins, losses], labels=['Wins', 'Losses'], autopct='%1.1f%%',
                   colors=['#4CAF50', '#F44336'], startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

    with stats_tab2:
        # Get game history data
        conn = get_db_connection()
        df = pd.read_sql_query('''
        SELECT
            timestamp,
            CASE WHEN player1_name = 'Player 1' THEN player1_score ELSE player2_score END as player_score,
            CASE WHEN player1_name = 'Player 1' THEN player2_score ELSE player1_score END as opponent_score,
            CASE
                WHEN (player1_name = 'Player 1' AND winner = 1) OR (player2_name = 'Player 1' AND winner = 2) THEN 'Win'
                ELSE 'Loss'
            END as result,
            duration_seconds
        FROM game_stats
        WHERE player1_name = 'Player 1' OR player2_name = 'Player 1'
        ORDER BY timestamp
        ''', conn)
        conn.close()

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date

        # Create performance charts
        st.subheader("Score History")

        # Line chart for scores over time
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df['player_score'], 'b-', label='Your Score')
        ax.plot(df.index, df['opponent_score'], 'r-', label='Opponent Score')
        ax.set_xlabel('Game Number')
        ax.set_ylabel('Score')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        # Bar chart comparing average scores by result
        st.subheader("Average Score by Outcome")
        avg_by_result = df.groupby('result')[['player_score', 'opponent_score']].mean()

        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(avg_by_result.index))
        width = 0.35

        ax.bar(x - width/2, avg_by_result['player_score'], width, label='Your Score', color='#3498db')
        ax.bar(x + width/2, avg_by_result['opponent_score'], width, label='Opponent Score', color='#e74c3c')

        ax.set_xticks(x)
        ax.set_xticklabels(avg_by_result.index)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        st.pyplot(fig)

        # Game duration analysis
        st.subheader("Game Duration Analysis")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(df.index, df['duration_seconds']/60, c=['green' if r == 'Win' else 'red' for r in df['result']])
        ax.set_xlabel('Game Number')
        ax.set_ylabel('Duration (minutes)')
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    with stats_tab3:
        # Display full game history
        st.subheader("Game History")

        # Get game history from database
        conn = get_db_connection()
        history_df = pd.read_sql_query('''
        SELECT
            timestamp,
            CASE
                WHEN player1_name = 'Player 1' THEN player1_name
                ELSE player2_name
            END as player,
            CASE
                WHEN player1_name = 'Player 1' THEN player2_name
                ELSE player1_name
            END as opponent,
            CASE
                WHEN player1_name = 'Player 1' THEN player1_score
                ELSE player2_score
            END as player_score,
            CASE
                WHEN player1_name = 'Player 1' THEN player2_score
                ELSE player1_score
            END as opponent_score,
            CASE
                WHEN (player1_name = 'Player 1' AND winner = 1) OR (player2_name = 'Player 1' AND winner = 2) THEN 'Win'
                ELSE 'Loss'
            END as result,
            duration_seconds
        FROM game_stats
        WHERE player1_name = 'Player 1' OR player2_name = 'Player 1'
        ORDER BY timestamp DESC
        ''', conn)
        conn.close()

        # Format the dataframe for display
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
        history_df['date'] = history_df['timestamp'].dt.strftime('%Y-%m-%d')
        history_df['time'] = history_df['timestamp'].dt.strftime('%H:%M')
        history_df['duration'] = history_df['duration_seconds'].apply(lambda x: f"{x//60}:{x%60:02d}")
        history_df['score'] = history_df.apply(lambda row: f"{row['player_score']} - {row['opponent_score']}", axis=1)

        # Display table with colored results
        display_df = history_df[['date', 'time', 'opponent', 'score', 'result', 'duration']]

        # Apply color formatting
        def color_result(val):
            color = 'green' if val == 'Win' else 'red'
            return f'background-color: {color}; color: white'

        # Display the styled dataframe
        st.dataframe(display_df.style.applymap(color_result, subset=['result']), use_container_width=True)

        # Export button
        csv = history_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Game History",
            data=csv,
            file_name="pong_game_history.csv",
            mime="text/csv",
        )

# Leaderboard tab
with tab4:
    st.markdown("## 🏆 Global Leaderboard")

    # Create mock leaderboard data
    leaderboard_data = {
        'Player': ['Champion123', 'PongMaster', player_name, 'ProGamer99', 'PaddleKing', 'BallChaser', 'RetroGamer', 'PongLegend', 'SpeedDemon', 'SlowButSteady'],
        'Wins': [124, 98, 76, 65, 54, 48, 42, 39, 35, 32],
        'Losses': [12, 23, 24, 18, 22, 26, 19, 21, 25, 18],
        'Win Rate': [91.2, 81.0, 76.0, 78.3, 71.1, 64.9, 68.9, 65.0, 58.3, 64.0],
        'Avg Score': [10.8, 9.7, 9.2, 9.5, 8.9, 8.7, 8.5, 8.3, 8.1, 7.9],
        'Rank': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }

    leaderboard_df = pd.DataFrame(leaderboard_data)

    # Display leaderboard with styling
    st.markdown("""
    <style>
    .leaderboard-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: gold !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="leaderboard-header">🏆 Top 10 Players Worldwide 🏆</p>', unsafe_allow_html=True)

    # Create columns for the leaderboard
    lb_col1, lb_col2 = st.columns([3, 2])

    with lb_col1:
        # Function to highlight the current player
        def highlight_player(row):
            if row['Player'] == player_name:
                return ['background-color: rgba(52, 152, 219, 0.3)'] * len(row)
            return [''] * len(row)

        # Display the styled dataframe
        st.dataframe(
            leaderboard_df.style.apply(highlight_player, axis=1)
                              .format({'Win Rate': '{:.1f}%', 'Avg Score': '{:.1f}'}),
            use_container_width=True,
            height=400
        )

    with lb_col2:
        # Create a bar chart of top players by wins
        fig, ax = plt.subplots(figsize=(8, 10))

        # Sort by wins
        sorted_df = leaderboard_df.sort_values('Wins', ascending=True)

        # Create horizontal bar chart
        bars = ax.barh(sorted_df['Player'], sorted_df['Wins'], color='#3498db')

        # Highlight the current player's bar
        for i, bar in enumerate(bars):
            if sorted_df.iloc[i]['Player'] == player_name:
                bar.set_color('#e74c3c')

        ax.set_xlabel('Total Wins')
        ax.set_title('Top Players by Wins')
        ax.grid(True, alpha=0.3, axis='x')

        # Add win count labels to the bars
        for i, v in enumerate(sorted_df['Wins']):
            ax.text(v + 1, i, str(v), va='center')

        st.pyplot(fig)

        # Add achievement section
        st.subheader("🏅 Your Achievements")

        # Get achievements from database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get all achievements
        cursor.execute('SELECT id, name, description, icon FROM achievements')
        all_achievements = cursor.fetchall()

        # Get player's unlocked achievements
        cursor.execute('''
        SELECT achievement_id FROM player_achievements
        WHERE player_name = ?
        ''', (player_name,))
        unlocked_ids = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Display achievements
        for ach in all_achievements:
            ach_id, ach_name, ach_desc, ach_icon = ach
            is_unlocked = ach_id in unlocked_ids

            # Create a styled achievement card
            st.markdown(f"""
            <div style="
                background-color: {'rgba(76, 175, 80, 0.2)' if is_unlocked else 'rgba(120, 120, 120, 0.2)'};
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                border-left: 5px solid {'#4CAF50' if is_unlocked else '#777'};
            ">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 2rem; margin-right: 10px;">{ach_icon}</div>
                    <div>
                        <div style="font-weight: bold; color: {'white' if is_unlocked else '#aaa'};">{ach_name}</div>
                        <div style="font-size: 0.8rem; color: {'#ddd' if is_unlocked else '#999'};">{ach_desc}</div>
                    </div>
                    <div style="margin-left: auto; font-size: 0.8rem; color: {'#4CAF50' if is_unlocked else '#777'};">
                        {'UNLOCKED' if is_unlocked else 'LOCKED'}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Installation tab
with tab5:
    st.markdown("""
    ## Installation Instructions

    Follow these steps to get the game running on your computer:

    ### 1. Prerequisites

    Make sure you have Python 3.7+ installed on your system. You can check your Python version with:
    ```
    python --version
    ```

    ### 2. Download Game Files

    Download the game files from the links provided or clone the repository:
    ```
    git clone https://github.com/asadullah48/multiplayer-pong.git
    cd multiplayer-pong
    ```

    ### 3. Install Required Packages

    Install the necessary Python packages:
    ```
    pip install pygame matplotlib
    ```

    ### 4. Start the Server

    Open a terminal window and run:
    ```
    python server.py
    ```

    You should see a message indicating that the server has started.

    ### 5. Launch the Client(s)

    In another terminal window, run:
    ```
    python client.py
    ```

    For a multiplayer experience, run the client on another computer connected to the same network, or open a second terminal and run another instance of the client.

    ### 6. Enjoy the Game!

    Use the controls to play:
    - Player 1: W (up) and S (down)
    - Player 2: Up Arrow (up) and Down Arrow (down)

    ### Troubleshooting

    If you encounter connection issues:

    1. Make sure the server is running before starting the clients
    2. Check your firewall settings
    3. If playing over a network, ensure you use the correct IP address in the client configuration
    4. Press 'R' to reconnect if the client disconnects
    """)

    st.markdown("## Deploy with Streamlit")
    st.code("""
# Install Streamlit
pip install streamlit

# Run the Streamlit app
streamlit run app.py
    """, language="bash")

    # Add requirements.txt download button with enhanced dependencies
    requirements = """
pygame==2.5.0
matplotlib==3.7.1
numpy==1.24.3
streamlit==1.22.0
pillow==9.5.0
pandas==2.0.0
sqlite3-api==0.1.0
pygame-gui==0.6.9
pygame-menu==4.4.0
pygame-widgets==1.0.0
simpleaudio==1.0.4
"""

    st.download_button(
        label="⬇️ Download requirements.txt",
        data=requirements,
        file_name="requirements.txt",
        mime="text/plain",
    )

    # Add a "Start Game" button at the bottom
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 START GAME NOW", key="start_game_button", use_container_width=True):
            st.balloons()
            st.success("Game settings saved! Starting the game with your configuration...")

            # Display a countdown
            progress_text = "Initializing game..."
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <h3 style="color: #4CAF50;">Game Started!</h3>
                <p>Enjoy playing Multiplayer Pong with your custom settings.</p>
            </div>
            """, unsafe_allow_html=True)