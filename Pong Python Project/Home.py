import streamlit as st
import base64
from PIL import Image
import io
import sqlite3
import os

# Initialize database if it doesn't exist
def init_db():
    conn = sqlite3.connect('pong_game.db')
    c = conn.cursor()

    # Create game_stats table if it doesn't exist
    c.execute('''
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

    # Create achievements table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        condition_type TEXT NOT NULL,
        condition_value INTEGER NOT NULL,
        icon TEXT NOT NULL
    )
    ''')

    # Create player_achievements table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS player_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        achievement_id INTEGER NOT NULL,
        earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (achievement_id) REFERENCES achievements (id)
    )
    ''')

    # Insert default achievements if they don't exist
    c.execute("SELECT COUNT(*) FROM achievements")
    if c.fetchone()[0] == 0:
        achievements = [
            ('First Victory', 'Win your first game', 'wins', 1, '🏆'),
            ('Hat Trick', 'Win 3 games in a row', 'streak', 3, '🎩'),
            ('Speed Demon', 'Win a game in under 60 seconds', 'time', 60, '⚡'),
            ('Comeback King', 'Win after being down by 3 points', 'comeback', 3, '👑'),
            ('Perfect Game', 'Win a game 5-0', 'perfect', 5, '🌟')
        ]
        c.executemany('''
        INSERT INTO achievements (name, description, condition_type, condition_value, icon)
        VALUES (?, ?, ?, ?, ?)
        ''', achievements)

    conn.commit()
    conn.close()

# Set up page configuration
def set_page_config():
    st.set_page_config(
        page_title="Enhanced Pong Game",
        page_icon="🏓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Add custom CSS
def add_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        color: #333333;
    }
    .stApp {
        background-color: #ffffff;
    }
    .css-18e3th9 {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    .highlight {
        background-color: rgba(255, 75, 75, 0.1);
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #ff4b4b;
    }
    .game-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        border: 1px solid #e9ecef;
    }
    .game-card:hover {
        transform: translateY(-5px);
    }
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #f8f9fa;
    }
    /* Improve text contrast */
    p, li, .caption {
        color: #333333;
    }
    /* Make links more visible */
    a {
        color: #0066cc !important;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# Add animated background (disabled for better contrast)
def add_animated_background():
    # This function is now disabled to provide a cleaner background with better contrast
    pass

# Main function
def main():
    # Initialize database
    init_db()

    # Set up page configuration
    set_page_config()

    # Add custom CSS and animated background
    add_custom_css()
    add_animated_background()

    # Create sidebar
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/asadullah48/pong-game/main/screenshot.png", width=200)
        st.title("🏓 Pong Game")
        st.markdown("---")

        # Navigation
        st.subheader("Navigation")
        pages = {
            "Home": "Home",
            "Play Game": "pages/1_Play_Game"
            # Commented out pages that don't exist yet
            # "Leaderboard": "pages/2_Leaderboard",
            # "Achievements": "pages/3_Achievements",
            # "Settings": "pages/4_Settings",
            # "About": "pages/5_About"
        }

        # Get current page path
        current_page = os.path.basename(__file__)

        for page_name, page_path in pages.items():
            page_filename = os.path.basename(page_path + ".py")
            if current_page == page_filename:
                st.markdown(f"**➡️ {page_name}**")
            else:
                st.page_link(page_path + ".py", label=page_name)

        st.markdown("---")
        st.caption("© 2023 Pong Game | v2.0")

    # Main content
    st.title("🏓 Enhanced Pong Game")
    st.markdown("""
    <div class="highlight">
    Welcome to the enhanced version of the classic Pong arcade game! This application offers a modern take on the nostalgic Pong experience with improved graphics, additional features, and player statistics.
    </div>
    """, unsafe_allow_html=True)

    # Game preview
    st.header("Game Preview")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("https://raw.githubusercontent.com/asadullah48/pong-game/main/screenshot.png",
                caption="Enhanced Pong Game", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="game-card">
        <h3>New Features</h3>
        <ul>
            <li>Multiple difficulty levels</li>
            <li>Customizable paddles and ball</li>
            <li>Player statistics and achievements</li>
            <li>Leaderboard system</li>
            <li>Sound effects and music</li>
            <li>Power-ups and special effects</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.button("Play Now!", use_container_width=True, key="play_button")

    # Quick start guide
    st.header("Quick Start Guide")

    tab1, tab2, tab3 = st.tabs(["Controls", "Game Modes", "Tips & Tricks"])

    with tab1:
        st.subheader("Game Controls")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="game-card">
            <h4>Player A (Left)</h4>
            <ul>
                <li><strong>W key</strong>: Move paddle up</li>
                <li><strong>S key</strong>: Move paddle down</li>
                <li><strong>Color</strong>: Deep Pink</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="game-card">
            <h4>Player B (Right)</h4>
            <ul>
                <li><strong>↑ (Up Arrow)</strong>: Move paddle up</li>
                <li><strong>↓ (Down Arrow)</strong>: Move paddle down</li>
                <li><strong>Color</strong>: Cyan</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="game-card">
        <h4>Game Controls</h4>
        <ul>
            <li><strong>P key</strong>: Pause/Resume game</li>
            <li><strong>R key</strong>: Reset game</li>
            <li><strong>M key</strong>: Toggle sound</li>
            <li><strong>ESC key</strong>: Exit game</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Game Modes")

        modes = [
            {
                "name": "Classic Mode",
                "description": "The original Pong experience. First to 5 points wins.",
                "icon": "🏆"
            },
            {
                "name": "Time Attack",
                "description": "Score as many points as possible in 60 seconds.",
                "icon": "⏱️"
            },
            {
                "name": "Power-up Mode",
                "description": "Special power-ups appear randomly to change gameplay dynamics.",
                "icon": "⚡"
            }
        ]

        for mode in modes:
            st.markdown(f"""
            <div class="game-card">
            <h4>{mode['icon']} {mode['name']}</h4>
            <p>{mode['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("Tips & Tricks")

        tips = [
            "Hit the ball with the edge of your paddle to increase its speed",
            "The ball's angle changes based on where it hits the paddle",
            "Use the pause feature (P key) to take a strategic break",
            "In Power-up Mode, prioritize collecting speed boosts and paddle extensions",
            "Practice timing your paddle movements to anticipate the ball's trajectory"
        ]

        for i, tip in enumerate(tips, 1):
            st.markdown(f"""
            <div class="game-card">
            <h4>Tip #{i}</h4>
            <p>{tip}</p>
            </div>
            """, unsafe_allow_html=True)

    # Recent updates
    st.header("Recent Updates")

    updates = [
        {
            "version": "2.0",
            "date": "2023-06-15",
            "changes": [
                "Complete UI overhaul with modern design",
                "Added player statistics and leaderboard",
                "Implemented achievements system",
                "Added power-ups and special effects",
                "Improved ball physics and paddle responsiveness"
            ]
        },
        {
            "version": "1.5",
            "date": "2023-03-10",
            "changes": [
                "Added sound effects and background music",
                "Implemented pause and reset functionality",
                "Fixed ball collision detection issues",
                "Added game difficulty options"
            ]
        }
    ]

    for update in updates:
        with st.expander(f"Version {update['version']} - {update['date']}"):
            for change in update['changes']:
                st.markdown(f"- {change}")

if __name__ == "__main__":
    main()
