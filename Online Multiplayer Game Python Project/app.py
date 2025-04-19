import streamlit as st
import base64
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
import os

# Set page config
st.set_page_config(
    page_title="Multiplayer Pong Game",
    page_icon="🏓",
    layout="wide"
)

# Page title and description
st.title("🏓 Multiplayer Pong Game")
st.markdown("""
A real-time multiplayer implementation of the classic Pong game using Python, Pygame, and socket programming.
""")

# Sidebar
st.sidebar.title("Game Options")
st.sidebar.markdown("## Instructions")
st.sidebar.markdown("""
1. Download the game files using the links below
2. Install the requirements
3. First run the server, then run the client(s)
""")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📚 About", "🎮 Demo", "🔧 Installation"])

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

# Demo tab with animated GIF
with tab2:
    st.markdown("## Game Demo")
    
    # Create a simple animated "GIF" of Pong gameplay with matplotlib
    frames = []
    ball_x, ball_y = 5, 7.5
    ball_dx, ball_dy = 0.4, 0.3
    paddle1_y, paddle2_y = 6, 8
    paddle1_dy, paddle2_dy = 0.2, -0.2
    
    for i in range(20):
        fig, ax = plt.subplots(figsize=(6, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 15)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Draw the court
        ax.add_patch(plt.Rectangle((0, 0), 10, 15, fill=True, color='black'))
        ax.plot([5, 5], [0, 15], 'w--', alpha=0.5)
        
        # Update paddle positions
        paddle1_y += paddle1_dy
        if paddle1_y <= 0 or paddle1_y >= 12:
            paddle1_dy = -paddle1_dy
        
        paddle2_y += paddle2_dy
        if paddle2_y <= 0 or paddle2_y >= 12:
            paddle2_dy = -paddle2_dy
        
        # Draw the paddles
        ax.add_patch(plt.Rectangle((0.5, paddle1_y), 0.5, 3, fill=True, color='blue'))
        ax.add_patch(plt.Rectangle((9, paddle2_y), 0.5, 3, fill=True, color='red'))
        
        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Ball collisions
        if ball_y <= 0.5 or ball_y >= 14.5:
            ball_dy = -ball_dy
        
        # Paddle collisions
        if (ball_x <= 1.5 and paddle1_y <= ball_y <= paddle1_y + 3) or \
           (ball_x >= 8.5 and paddle2_y <= ball_y <= paddle2_y + 3):
            ball_dx = -ball_dx
        
        # If ball goes out of bounds, reset
        if ball_x < 0 or ball_x > 10:
            ball_x, ball_y = 5, 7.5
            ball_dx = -ball_dx
        
        # Draw the ball
        ax.add_patch(plt.Circle((ball_x, ball_y), 0.5, fill=True, color='white'))
        
        # Add scores
        ax.text(2.5, 14, '3', color='white', fontsize=24, ha='center')
        ax.text(7.5, 14, '2', color='white', fontsize=24, ha='center')
        
        # Convert to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        img = Image.open(buf)
        frames.append(np.array(img))
        plt.close(fig)
    
    # Display frames as an animation
    st.image(frames, width=600)
    
    st.markdown("""
    ### Live Demo
    
    Experience the game for yourself! Download the files and follow the installation instructions.
    """)

# Installation tab
with tab3:
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
    
    # Add requirements.txt download button
    requirements = """
pygame==2.5.0
matplotlib==3.7.1
numpy==1.24.3
streamlit==1.22.0
pillow==9.5.0
"""
    
    st.download_button(
        label="⬇️ Download requirements.txt",
        data=requirements,
        file_name="requirements.txt",
        mime="text/plain",
    )