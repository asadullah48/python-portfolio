# app.py
import streamlit as st
import subprocess
import os
import base64
from PIL import Image
import io

def main():
    st.set_page_config(page_title="Classic Pong Game", layout="wide")
    
    # Title and description
    st.title("🏓 Classic Pong Game")
    st.markdown("""
    ### A nostalgic recreation of the classic Pong arcade game!
    
    This application runs the classic Pong game built with Python's Turtle graphics. 
    Enjoy this retro gaming experience right from your desktop!
    """)

    # Game screenshot (placeholder - you would replace this with an actual screenshot)
    st.image("https://raw.githubusercontent.com/asadullah48/pong-game/main/screenshot.png", 
         caption="Classic Pong Game Screenshot", use_container_width=True)
    
    # Game Instructions
    st.header("🎮 How to Play")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Player A (Left)")
        st.markdown("""
        - **W key**: Move paddle up
        - **S key**: Move paddle down
        - Color: Deep Pink
        """)
    
    with col2:
        st.subheader("Player B (Right)")
        st.markdown("""
        - **↑ (Up Arrow)**: Move paddle up
        - **↓ (Down Arrow)**: Move paddle down
        - Color: Cyan
        """)
    
    st.markdown("""
    ### Game Controls
    - **P key**: Pause/Resume game
    - **R key**: Reset game
    
    ### Game Rules
    - First player to score 5 points wins
    - The ball speeds up slightly after each paddle hit
    - Ball direction changes based on where it hits the paddle
    """)
    
    # Download and Play section
    st.header("⬇️ Download and Play")
    
    st.markdown("""
    Since this game uses Turtle graphics, it needs to run on your local machine.
    Follow these steps to play:
    
    1. Download the Python script using the button below
    2. Make sure you have Python installed on your computer
    3. Open a terminal or command prompt
    4. Run the command: `python pong_game.py`
    """)
    
    # Generate the Python script for download
    with open("pong_game.py", "r") as file:
        code_content = file.read()
        
    st.download_button(
        label="Download Pong Game",
        data=code_content,
        file_name="pong_game.py",
        mime="text/plain",
        key="download-game"
    )
    
    # About section
    st.header("ℹ️ About")
    st.markdown("""
    This classic Pong game was originally created by Saira and enhanced with additional features.
    
    Visit the [GitHub repository](https://github.com/asadullah48/pong-game) for more information and to contribute to the project.
    
    Made with ❤️ using Python and Turtle Graphics.
    """)

if __name__ == "__main__":
    main()