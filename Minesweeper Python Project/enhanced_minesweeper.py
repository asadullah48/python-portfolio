import streamlit as st
import random
import time
import numpy as np
from minesweeper import Minesweeper
from PIL import Image
import base64
import os
import glob

# Set page configuration
st.set_page_config(
    page_title="Minesweeper Pro",
    page_icon="💣",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Define color scheme for numbers
NUMBER_COLORS = {
    "1": "#0000FF",  # Blue
    "2": "#008000",  # Green
    "3": "#FF0000",  # Red
    "4": "#000080",  # Navy
    "5": "#800000",  # Maroon
    "6": "#008080",  # Teal
    "7": "#000000",  # Black
    "8": "#808080",  # Gray
}

# Function to get base64 encoding of an image
def get_base64_of_image(image_path):
    """Get the base64 string of an image"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to add background image from URL
def add_bg_from_url(url):
    """Add a background image from a URL"""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to add background image from local file
def add_bg_from_local(image_path):
    """Add a background image from a local file"""
    try:
        base64_image = get_base64_of_image(image_path)
        image_extension = os.path.splitext(image_path)[1][1:]  # Get extension without dot
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/{image_extension};base64,{base64_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .block-container {{
                background-color: rgba(255, 255, 255, 0.85);
                padding: 2rem;
                border-radius: 10px;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        return True
    except Exception as e:
        st.error(f"Error loading background image: {e}")
        return False

# Function to find all image files in a directory
def find_image_files(directory="."):
    """Find all image files in the specified directory"""
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]
    image_files = []

    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(directory, extension)))

    return image_files

# Function to create custom CSS
def apply_custom_css():
    st.markdown(
        """
        <style>
        /* Main container styling */
        .main {
            padding: 1rem;
        }

        /* Header styling */
        h1 {
            color: #2c3e50;
            text-align: center;
            font-family: 'Arial', sans-serif;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        /* Subheader styling */
        h3 {
            color: #34495e;
            font-family: 'Arial', sans-serif;
            margin-bottom: 1rem;
        }

        /* Button styling */
        .stButton button {
            font-weight: bold;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Game cell styling */
        .game-cell {
            width: 100%;
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2rem;
            border: 1px solid #ddd;
            background-color: #f8f9fa;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .game-cell:hover {
            background-color: #e9ecef;
        }

        /* Stats container */
        .stats-container {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 2rem;
            color: #7f8c8d;
            font-size: 0.8rem;
        }

        /* Custom difficulty selector */
        .difficulty-selector {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        /* Game board container */
        .game-board {
            margin: 1rem 0;
            display: grid;
            gap: 2px;
        }

        /* Control buttons */
        .control-button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to create game board
def create_game_board(game):
    # Get cell display values
    cell_values = []
    for r in range(game.size):
        row = []
        for c in range(game.size):
            if (r, c) in game.revealed:
                if (r, c) in game.bomb_positions:
                    row.append("💣")
                else:
                    bomb_count = game._count_adjacent_bombs(r, c)
                    row.append(str(bomb_count) if bomb_count > 0 else " ")
            elif (r, c) in game.flagged:
                row.append("🚩")
            else:
                row.append("□")
        cell_values.append(row)

    return cell_values

# Function to format cell display with colors
def format_cell_display(value):
    if value in NUMBER_COLORS:
        return f'<span style="color:{NUMBER_COLORS[value]};">{value}</span>'
    return value

# Function to display timer
def display_timer():
    if 'start_time' in st.session_state:
        elapsed_time = int(time.time() - st.session_state.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return f"{minutes:02d}:{seconds:02d}"
    return "00:00"

# Main function
def main():
    # Apply custom styling
    apply_custom_css()

    # Background image settings
    if 'background_type' not in st.session_state:
        st.session_state.background_type = 'online'

    if 'background_image' not in st.session_state:
        st.session_state.background_image = "https://img.freepik.com/free-vector/abstract-blue-geometric-background_1035-17545.jpg"

    # Title and description
    st.markdown("<h1>💣 Minesweeper Pro 💣</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Clear the board without hitting any bombs!</h3>", unsafe_allow_html=True)

    # Apply background based on session state
    if st.session_state.background_type == 'online':
        add_bg_from_url(st.session_state.background_image)
    else:
        if st.session_state.background_image:
            add_bg_from_local(st.session_state.background_image)

    # Sidebar for game settings and instructions
    with st.sidebar:
        st.markdown("## Game Settings")

        # Difficulty presets
        difficulty = st.radio(
            "Select Difficulty",
            ["Beginner", "Intermediate", "Expert", "Custom"],
            index=0,
            horizontal=False,
        )

        # Background settings
        st.markdown("## Background Settings")
        background_type = st.radio(
            "Background Source",
            ["Online URL", "Local File"],
            index=0 if st.session_state.background_type == 'online' else 1,
            horizontal=True,
        )

        # Update background type in session state
        st.session_state.background_type = 'online' if background_type == "Online URL" else 'local'

        # Background URL input
        if st.session_state.background_type == 'online':
            bg_url = st.text_input(
                "Background Image URL",
                value=st.session_state.background_image if st.session_state.background_type == 'online' else "https://img.freepik.com/free-vector/abstract-blue-geometric-background_1035-17545.jpg",
                help="Enter a URL to an image (jpg, png, etc.)"
            )

            # Update background URL in session state
            if bg_url != st.session_state.background_image:
                st.session_state.background_image = bg_url
                st.rerun()

            # Preset background options
            st.markdown("### Preset Backgrounds")
            preset_cols = st.columns(2)

            preset_backgrounds = {
                "Blue Geometric": "https://img.freepik.com/free-vector/abstract-blue-geometric-background_1035-17545.jpg",
                "Dark Pattern": "https://img.freepik.com/free-vector/dark-hexagonal-background-with-gradient-color_79603-1410.jpg",
                "Light Abstract": "https://img.freepik.com/free-vector/white-abstract-background_23-2148810113.jpg",
                "Tech Circuit": "https://img.freepik.com/free-vector/circuit-board-technology-background-with-hi-tech-digital-data-connection-system_1017-25592.jpg"
            }

            # Create buttons for preset backgrounds
            i = 0
            for name, url in preset_backgrounds.items():
                col_idx = i % 2
                with preset_cols[col_idx]:
                    if st.button(name, key=f"preset_{i}"):
                        st.session_state.background_image = url
                        st.rerun()
                i += 1
        else:
            # Local file selection
            st.markdown("### Local Image Files")

            # Find local image files
            image_files = find_image_files()

            if not image_files:
                st.warning("No image files found in the current directory. Add some images to use as backgrounds.")
            else:
                # Create a dropdown to select local images
                selected_image = st.selectbox(
                    "Select a local image",
                    options=image_files,
                    format_func=lambda x: os.path.basename(x),
                    index=0 if st.session_state.background_image not in image_files else image_files.index(st.session_state.background_image)
                )

                # Update background image in session state
                if selected_image != st.session_state.background_image:
                    st.session_state.background_image = selected_image
                    st.rerun()

                # Show preview of selected image
                st.markdown("### Preview")
                try:
                    img = Image.open(selected_image)
                    st.image(img, width=200, caption=os.path.basename(selected_image))
                except Exception as e:
                    st.error(f"Error loading image: {e}")

        # Set board size and bomb count based on difficulty
        if difficulty == "Beginner":
            size = 8
            bomb_count = 10
        elif difficulty == "Intermediate":
            size = 12
            bomb_count = 30
        elif difficulty == "Expert":
            size = 16
            bomb_count = 60
        else:  # Custom
            size = st.slider("Board Size", min_value=5, max_value=20, value=10)
            max_bombs = min(size * size - 1, 99)  # Ensure we don't fill the entire board
            bomb_count = st.slider("Number of Bombs", min_value=1, max_value=max_bombs, value=size)

        # New game button
        if st.button("🎮 New Game", use_container_width=True):
            st.session_state.game = Minesweeper(size=size, bombs=bomb_count)
            st.session_state.start_time = time.time()
            st.session_state.moves = 0
            st.session_state.game_started = False
            st.rerun()

        # Instructions
        st.markdown("## How to Play")
        st.markdown("""
        - **Left Click**: Reveal a cell
        - **Flag Mode**: Mark potential bomb locations
        - **Goal**: Reveal all non-bomb cells

        **Tips:**
        - Use the numbers as hints
        - Numbers show adjacent bombs
        - Flag suspected bomb locations
        - Be strategic and think ahead!
        """)

        # About section
        st.markdown("## About")
        st.markdown("""
        Minesweeper Pro is an enhanced version of the classic game with modern UI and features.

        Created with ❤️ using Python and Streamlit.
        """)

    # Initialize or get game from session state
    if 'game' not in st.session_state:
        st.session_state.game = Minesweeper(size=size, bombs=bomb_count)
        st.session_state.start_time = time.time()
        st.session_state.moves = 0
        st.session_state.game_started = False

    game = st.session_state.game

    # Game statistics
    st.markdown(
        f"""
        <div class="stats-container">
            <div style="display: flex; justify-content: space-between;">
                <div>⏱️ <b>Time:</b> {display_timer()}</div>
                <div>🔢 <b>Moves:</b> {st.session_state.moves}</div>
                <div>💣 <b>Bombs:</b> {game.bombs}</div>
                <div>🚩 <b>Flags:</b> {len(game.flagged)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Game controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Reveal Mode" if st.session_state.get('flag_mode', False) else "🚩 Flag Mode", use_container_width=True):
            st.session_state.flag_mode = not st.session_state.get('flag_mode', False)
            st.rerun()

    with col2:
        mode_txt = "🚩 Flag Mode Active" if st.session_state.get('flag_mode', False) else "🔍 Reveal Mode Active"
        st.info(mode_txt)

    # Game board
    cell_values = create_game_board(game)

    # Calculate cell size based on board dimensions
    cell_size = max(30, min(50, 600 // game.size))

    # Create a container for the game board with fixed width
    board_container = st.container()

    with board_container:
        # Create a grid of buttons for the game board
        for r in range(game.size):
            cols = st.columns(game.size)
            for c in range(game.size):
                cell_key = f"cell_{r}_{c}"
                cell_value = cell_values[r][c]

                # Style the cell based on its content
                if cell_value.isdigit() and int(cell_value) > 0:
                    cell_style = f'color: {NUMBER_COLORS[cell_value]}; font-weight: bold;'
                else:
                    cell_style = ''

                # Handle game completion
                if game.game_over:
                    if (r, c) in game.bomb_positions:
                        cols[c].button("💣", key=cell_key, disabled=True, use_container_width=True)
                    else:
                        cols[c].button(cell_value, key=cell_key, disabled=True, use_container_width=True)
                elif game.won:
                    if (r, c) in game.bomb_positions:
                        cols[c].button("🚩", key=cell_key, disabled=True, use_container_width=True)
                    else:
                        cols[c].button(cell_value, key=cell_key, disabled=True, use_container_width=True)
                else:
                    # Game in progress
                    if (r, c) in game.revealed:
                        # Apply color to numbers
                        if cell_value.isdigit() and int(cell_value) > 0:
                            cols[c].markdown(
                                f'<div style="text-align: center; {cell_style} font-size: {cell_size//2}px;">{cell_value}</div>',
                                unsafe_allow_html=True
                            )
                        else:
                            cols[c].button(cell_value, key=cell_key, disabled=True, use_container_width=True)
                    else:
                        # Handle cell click
                        left_click = cols[c].button(cell_value, key=cell_key, use_container_width=True)

                        if left_click:
                            # Start timer on first move
                            if not st.session_state.game_started:
                                st.session_state.start_time = time.time()
                                st.session_state.game_started = True

                            # Left-click behavior
                            if st.session_state.get('flag_mode', False):
                                game.toggle_flag(r, c)
                            else:
                                game.reveal(r, c)
                                st.session_state.moves += 1

                            st.rerun()

    # Game over message
    if game.game_over:
        st.error("💣 BOOM! Game Over! You hit a bomb!")

        # Show all bombs
        for r, c in game.bomb_positions:
            if (r, c) not in game.revealed:
                game.revealed.add((r, c))

        # Display final stats
        elapsed_time = int(time.time() - st.session_state.start_time)
        st.markdown(f"**Final Time:** {elapsed_time} seconds | **Moves:** {st.session_state.moves}")

    elif game.won:
        st.balloons()
        st.success("🎉 Congratulations! You cleared the board!")

        # Display final stats
        elapsed_time = int(time.time() - st.session_state.start_time)
        st.markdown(f"**Final Time:** {elapsed_time} seconds | **Moves:** {st.session_state.moves}")

    # Footer
    st.markdown(
        """
        <div class="footer">
            <p>© 2023 Minesweeper Pro | Made with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
