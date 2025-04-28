import streamlit as st
import sqlite3
import time
from datetime import datetime

def init_game_state():
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'player1_score' not in st.session_state:
        st.session_state.player1_score = 0
    if 'player2_score' not in st.session_state:
        st.session_state.player2_score = 0

def save_game_stats(player1_name, player2_name, player1_score, player2_score, duration):
    conn = sqlite3.connect('pong_game.db')
    c = conn.cursor()

    winner = 1 if player1_score > player2_score else 2

    c.execute('''
    INSERT INTO game_stats
    (player1_name, player2_name, player1_score, player2_score, winner, duration_seconds)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (player1_name, player2_name, player1_score, player2_score, winner, duration))

    conn.commit()
    conn.close()

def check_achievements(player_name, score, opponent_score, duration):
    conn = sqlite3.connect('pong_game.db')
    c = conn.cursor()

    # Get all achievements
    c.execute("SELECT * FROM achievements")
    achievements = c.fetchall()

    earned_achievements = []

    for achievement in achievements:
        achievement_id = achievement[0]
        condition_type = achievement[3]
        condition_value = achievement[4]

        # Check if player already has this achievement
        c.execute("""
        SELECT COUNT(*) FROM player_achievements
        WHERE player_name = ? AND achievement_id = ?
        """, (player_name, achievement_id))

        if c.fetchone()[0] == 0:  # Player doesn't have this achievement yet
            # Check different achievement conditions
            if condition_type == 'wins' and score > opponent_score:
                earned_achievements.append(achievement)
            elif condition_type == 'perfect' and score == 5 and opponent_score == 0:
                earned_achievements.append(achievement)
            elif condition_type == 'time' and score > opponent_score and duration <= condition_value:
                earned_achievements.append(achievement)

    # Award new achievements
    for achievement in earned_achievements:
        c.execute("""
        INSERT INTO player_achievements (player_name, achievement_id)
        VALUES (?, ?)
        """, (player_name, achievement[0]))

    conn.commit()
    conn.close()

    return earned_achievements

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
    /* Container styling */
    .stContainer {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Play Pong", page_icon="🏓")

    # Add custom CSS for high contrast
    add_custom_css()

    # Initialize game state
    init_game_state()

    # Title and game setup section
    st.title("🏓 Play Pong")

    # Game setup form
    with st.form("game_setup"):
        col1, col2 = st.columns(2)

        with col1:
            player1_name = st.text_input("Player 1 Name", "Player 1")

        with col2:
            player2_name = st.text_input("Player 2 Name", "Player 2")

        start_button = st.form_submit_button("Start Game")

        if start_button:
            st.session_state.game_active = True
            st.session_state.start_time = time.time()
            st.session_state.player1_score = 0
            st.session_state.player2_score = 0
            st.rerun()

    # Active game section
    if st.session_state.game_active:
        # Game interface
        st.markdown("### Current Score")
        score_col1, score_col2 = st.columns(2)

        with score_col1:
            st.markdown(f"**{player1_name}**: {st.session_state.player1_score}")
            if st.button("Score Point (Player 1)"):
                st.session_state.player1_score += 1
                st.rerun()

        with score_col2:
            st.markdown(f"**{player2_name}**: {st.session_state.player2_score}")
            if st.button("Score Point (Player 2)"):
                st.session_state.player2_score += 1
                st.rerun()

        # Game progress bar
        progress = (max(st.session_state.player1_score, st.session_state.player2_score) / 5) * 100
        st.progress(progress)

        # Check for game end
        if st.session_state.player1_score >= 5 or st.session_state.player2_score >= 5:
            duration = int(time.time() - st.session_state.start_time)

            # Save game stats
            save_game_stats(
                player1_name,
                player2_name,
                st.session_state.player1_score,
                st.session_state.player2_score,
                duration
            )

            # Check achievements for both players
            p1_achievements = check_achievements(
                player1_name,
                st.session_state.player1_score,
                st.session_state.player2_score,
                duration
            )

            p2_achievements = check_achievements(
                player2_name,
                st.session_state.player2_score,
                st.session_state.player1_score,
                duration
            )

            # Display game results
            st.balloons()
            winner = player1_name if st.session_state.player1_score > st.session_state.player2_score else player2_name
            st.success(f"🏆 {winner} wins!")
            st.info(f"Game duration: {duration} seconds")

            # Display new achievements
            if p1_achievements:
                st.markdown(f"### 🌟 New Achievements for {player1_name}")
                for achievement in p1_achievements:
                    st.markdown(f"{achievement[4]} **{achievement[1]}**: {achievement[2]}")

            if p2_achievements:
                st.markdown(f"### 🌟 New Achievements for {player2_name}")
                for achievement in p2_achievements:
                    st.markdown(f"{achievement[4]} **{achievement[1]}**: {achievement[2]}")

            if st.button("Play Again"):
                st.session_state.game_active = False
                st.rerun()

        # Game controls help
        with st.expander("Game Controls"):
            st.markdown("""
            ### Player Controls
            - Use the "Score Point" buttons to update the score
            - First player to reach 5 points wins
            - Game statistics and achievements are automatically tracked
            """)

    # Game statistics
    if not st.session_state.game_active:
        st.markdown("### Recent Games")
        conn = sqlite3.connect('pong_game.db')
        recent_games = conn.execute("""
            SELECT
                player1_name, player2_name,
                player1_score, player2_score,
                duration_seconds,
                timestamp
            FROM game_stats
            ORDER BY timestamp DESC
            LIMIT 5
        """).fetchall()
        conn.close()

        if recent_games:
            for game in recent_games:
                with st.container():
                    st.markdown(f"""
                    🏓 **{game[0]}** ({game[2]}) vs **{game[1]}** ({game[3]})
                    ⏱️ Duration: {game[4]} seconds
                    🕒 {game[5]}
                    """)
                    st.divider()

if __name__ == "__main__":
    main()