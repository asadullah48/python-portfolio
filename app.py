import streamlit as st
import base64
from PIL import Image
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import os
import glob
from datetime import datetime
import time
import numpy as np
from pathlib import Path
import re
import json
import requests

# Page configuration
st.set_page_config(
    page_title="Asadullah's Python Portfolio",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/asadullah48',
        'Report a bug': 'https://github.com/asadullah48',
        'About': "# Asadullah's Python Portfolio\nA showcase of 25 Python projects built with Streamlit."
    }
)

# Custom CSS with improved styling, dark mode support, and animations
st.markdown("""
<style>
    /* Light mode styles */
    :root {
        --background-color: #f8f9fa;
        --text-color: #212529;
        --card-bg-color: #ffffff;
        --card-border: 1px solid #e9ecef;
        --primary-color: #4361ee;
        --secondary-color: #3a0ca3;
        --header-bg: linear-gradient(135deg, #4361ee, #3a0ca3);
        --accent-color: #f72585;
        --success-color: #4cc9f0;
        --card-shadow: 0 4px 6px rgba(0,0,0,0.05);
        --hover-shadow: 0 10px 25px rgba(0,0,0,0.1);
        --sidebar-bg: #ffffff;
        --sidebar-text: #212529;
    }

    /* Dark mode styles */
    .dark-mode {
        --background-color: #121212;
        --text-color: #f8f9fa;
        --card-bg-color: #1e1e1e;
        --card-border: 1px solid #333;
        --primary-color: #4cc9f0;
        --secondary-color: #7209b7;
        --header-bg: linear-gradient(135deg, #4cc9f0, #7209b7);
        --accent-color: #f72585;
        --success-color: #4cc9f0;
        --card-shadow: 0 4px 6px rgba(0,0,0,0.2);
        --hover-shadow: 0 10px 25px rgba(0,0,0,0.3);
        --sidebar-bg: #1a1a1a;
        --sidebar-text: #f8f9fa;
    }

    /* Main container styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Background image/pattern */
    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
        z-index: -1;
    }

    .dark-mode body::before {
        opacity: 0.2;
    }

    body {
        color: var(--text-color);
        background-color: var(--background-color);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: var(--card-border);
        padding: 1rem;
    }

    [data-testid="stSidebar"] .block-container {
        margin-top: 1rem;
    }

    /* Project card styling */
    .project-card {
        background-color: var(--card-bg-color);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        border: var(--card-border);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: var(--card-shadow);
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
    }

    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary-color), var(--accent-color));
        opacity: 0.8;
    }

    .project-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--hover-shadow);
    }

    /* Category and difficulty labels */
    .category-label {
        background-color: var(--primary-color);
        color: white;
        padding: 5px 12px;
        border-radius: 30px;
        font-size: 0.8em;
        margin-right: 8px;
        display: inline-block;
        margin-bottom: 8px;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .difficulty-beginner {
        background: linear-gradient(135deg, #4CAF50, #8BC34A);
    }

    .difficulty-intermediate {
        background: linear-gradient(135deg, #FF9800, #FFC107);
    }

    .difficulty-advanced {
        background: linear-gradient(135deg, #F44336, #FF5722);
    }

    /* Header styling */
    .header-container {
        text-align: center;
        padding: 40px 30px;
        background: var(--header-bg);
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        color: white;
    }

    .header-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M3 3h18v18H3V3z' fill='rgba(255,255,255,0.1)'/%3E%3C/svg%3E");
        background-repeat: repeat;
        opacity: 0.2;
        transform: rotate(45deg);
    }

    .header-container h1 {
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .animated-card {
        animation: slideIn 0.5s ease-out forwards;
    }

    .animated-header {
        animation: fadeIn 1s ease-in forwards;
    }

    .pulse-animation {
        animation: pulse 2s infinite;
    }

    /* Project count and success message */
    .project-count {
        font-size: 1.8em;
        color: white;
        font-weight: bold;
        margin: 15px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    .success-message {
        font-style: italic;
        color: rgba(255,255,255,0.9);
        font-size: 1.2em;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Buttons styling */
    .view-details-btn {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        margin-top: auto;
        transition: all 0.3s ease;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }

    .view-details-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
    }

    /* Search box styling */
    .search-box {
        border-radius: 30px !important;
        border: var(--card-border) !important;
        padding: 12px 24px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }

    .search-box:focus {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        border-color: var(--primary-color) !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 12px 20px;
        background-color: var(--card-bg-color);
        border: var(--card-border);
        border-bottom: none;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }

    /* Social icons */
    .social-icons {
        font-size: 28px;
        margin: 0 12px;
        color: var(--primary-color);
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .social-icons:hover {
        color: var(--accent-color);
        transform: translateY(-3px);
    }

    /* GitHub stats card */
    .github-stats {
        background-color: var(--card-bg-color);
        padding: 20px;
        border-radius: 16px;
        border: var(--card-border);
        margin-bottom: 25px;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }

    .github-stats:hover {
        box-shadow: var(--hover-shadow);
    }

    /* Favorite button */
    .favorite-btn {
        background: none;
        border: none;
        color: #FFD700;
        font-size: 1.8em;
        cursor: pointer;
        position: absolute;
        top: 15px;
        right: 15px;
        z-index: 10;
        transition: all 0.3s ease;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .favorite-btn:hover {
        transform: scale(1.2);
    }

    /* Screenshot gallery */
    .screenshot-gallery {
        display: flex;
        overflow-x: auto;
        padding: 15px 0;
        gap: 15px;
        margin: 20px 0;
        scrollbar-width: thin;
    }

    .screenshot-img {
        max-height: 220px;
        border-radius: 12px;
        border: var(--card-border);
        transition: all 0.3s ease;
        box-shadow: var(--card-shadow);
    }

    .screenshot-img:hover {
        transform: scale(1.05);
        box-shadow: var(--hover-shadow);
    }

    /* Tech stack pill */
    .tech-pill {
        background: linear-gradient(135deg, var(--accent-color), var(--primary-color));
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8em;
        margin-right: 8px;
        margin-bottom: 8px;
        display: inline-block;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Project stats card */
    .stats-card {
        background-color: var(--card-bg-color);
        border-radius: 16px;
        padding: 20px;
        box-shadow: var(--card-shadow);
        margin-bottom: 20px;
        border: var(--card-border);
        transition: all 0.3s ease;
    }

    .stats-card:hover {
        box-shadow: var(--hover-shadow);
    }

    .stats-card h3 {
        margin: 0;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Demo section */
    .demo-section {
        background-color: rgba(0, 0, 0, 0.03);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: var(--card-border);
    }

    /* Timeline */
    .timeline-container {
        position: relative;
        padding-left: 40px;
        margin-bottom: 30px;
    }

    .timeline-item {
        position: relative;
        padding-bottom: 25px;
        padding-left: 15px;
    }

    .timeline-item:before {
        content: '';
        position: absolute;
        left: -40px;
        top: 0;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 1;
    }

    .timeline-item:after {
        content: '';
        position: absolute;
        left: -30px;
        top: 20px;
        width: 2px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary-color), rgba(var(--primary-color-rgb), 0.2));
    }

    .timeline-item:last-child:after {
        display: none;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background-color);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--primary-color), var(--secondary-color));
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(var(--secondary-color), var(--primary-color));
    }

    /* Emoji styling */
    .emoji {
        font-size: 1.6em;
        margin-right: 5px;
        vertical-align: middle;
    }

    /* Deployment badge */
    .deployment-badge {
        background: linear-gradient(135deg, #9C27B0, #673AB7);
        color: white;
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 0.8em;
        display: inline-block;
        margin: 8px 0;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .deployment-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Profile image styling */
    .profile-image {
        border-radius: 50%;
        border: 3px solid var(--primary-color);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .profile-image:hover {
        transform: scale(1.05);
        border-color: var(--accent-color);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }

    /* Skills progress bar */
    .stProgress > div > div {
        background-color: var(--primary-color);
        background-image: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    }

    /* Tooltip styling */
    div[data-baseweb="tooltip"] {
        background-color: var(--card-bg-color) !important;
        border: var(--card-border) !important;
        border-radius: 8px !important;
        box-shadow: var(--card-shadow) !important;
        color: var(--text-color) !important;
        padding: 10px 15px !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header-container {
            padding: 30px 20px;
        }

        .header-container h1 {
            font-size: 2rem;
        }

        .project-card {
            padding: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'show_project_details' not in st.session_state:
    st.session_state.show_project_details = False

# Define tech stacks used in projects
tech_stacks = {
    "Python": "🐍",
    "Pygame": "🎮",
    "TkInter": "🖼️",
    "Flask": "🌶️",
    "FastAPI": "⚡",
    "SQLite": "🗃️",
    "SQLAlchemy": "🔄",
    "Pandas": "🐼",
    "NumPy": "🔢",
    "Matplotlib": "📊",
    "Seaborn": "📈",
    "Streamlit": "🔥",
    "Requests": "🌐",
    "BeautifulSoup": "🍲",
    "Pillow": "🖼️",
    "OpenCV": "👁️",
    "Scikit-learn": "🧠",
    "PyTorch": "🔥",
    "TensorFlow": "📊",
    "Socket.io": "🔌",
}

# Define project data with enhanced info
projects = [
    {
        "id": 1,
        "title": "Mad Libs",
        "description": "A text-based game where players provide various words that are then inserted into blanks within a story, creating a humorous narrative.",
        "category": "Games",
        "difficulty": "Beginner",
        "key_features": ["String manipulation", "User input handling", "Text formatting"],
        "image": "madlibs.png",
        "github_link": "https://github.com/asadullah48/Mad-Libs-Generator",
        "streamlit_link": "https://libsgenerator.streamlit.app/",
        "tech_stack": ["Python", "TkInter"],
        "completion_date": "2025-02-15",
        "testimonial": "Great starter project to learn string formatting and user input!",
        "code_snippet": """def generate_story(words):
    story = f\"\"\"
    Once upon a time, there was a {words['adjective']} {words['animal']} who loved to {words['verb']} in the {words['place']}.
    Every {words['day_of_week']}, the {words['animal']} would {words['verb']} with its {words['adjective2']} friend.
    \"\"\"
    return story"""
    },
    {
        "id": 2,
        "title": "Guess the Number Game (Computer)",
        "description": "A game where the computer generates a random number and the player has to guess it with feedback provided.",
        "category": "Games",
        "difficulty": "Beginner",
        "key_features": ["Random number generation", "Conditional logic", "User input validation"],
        "image": "guess_number.png",
        "github_link": "https://github.com/asadullah48/guess-the-number-game",
        "streamlit_link": "https://guess-number-user-asadullah.streamlit.app/",
        "tech_stack": ["Python", "Streamlit"],
        "completion_date": "2025-02-15",
        "testimonial": "Simple but fun! Great for beginners to understand loops and conditionals.",
        "code_snippet": """import random

def guess_number():
    number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("Guess a number between 1 and 100: "))
        attempts += 1

        if guess < number:
            print("Too low!")
        elif guess > number:
            print("Too high!")
        else:
            print(f"You got it in {attempts} attempts!")
            break"""
    },
    {
        "id": 3,
        "title": "Minesweeper Game",
        "description": "A classic Minesweeper game implementation where players must uncover cells while avoiding hidden mines.",
        "category": "Games",
        "difficulty": "Intermediate",
        "key_features": ["Grid-based gameplay", "Recursive cell revealing", "Game state management", "Mine generation algorithm"],
        "image": "minesweeper.png",
        "github_link": "https://github.com/asadullah48/minesweeper",
        "streamlit_link": "https://minesweepergame.streamlit.app/",
        "tech_stack": ["Python", "Pygame", "NumPy"],
        "completion_date": "2023-09-15",
        "testimonial": "This project really helped me understand recursive algorithms and grid-based game design!",
        "code_snippet": """import random

def create_board(size, num_mines):
    # Create an empty board
    board = [[0 for _ in range(size)] for _ in range(size)]

    # Place mines randomly
    mines_placed = 0
    while mines_placed < num_mines:
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        if board[x][y] != 'M':
            board[x][y] = 'M'
            mines_placed += 1

            # Update adjacent cell counts
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and board[nx][ny] != 'M':
                        board[nx][ny] += 1

    return board"""
    },
    # Continue with other projects...
    {
        "id": 4,
        "title": "Rock, Paper, Scissors",
        "description": "Implementation of the classic hand game with a computer opponent using random selection.",
        "category": "Games",
        "difficulty": "Beginner",
        "key_features": ["Game logic", "Random choice", "Score tracking"],
        "image": "rock_paper_scissors.png",
        "github_link": "https://github.com/asadullah48/rock-paper-scissors",
        "streamlit_link": "https://rockpaperapp.streamlit.app/",
        "tech_stack": ["Python", "Streamlit"],
        "completion_date": "2023-07-15",
        "testimonial": "A perfect introduction to game development concepts in Python.",
    },
    # Adding more projects with streamlit links (continued from original list)
    # ... add more projects with enhanced information ...
    {
        "id": 20,
        "title": "Online Multiplayer Game",
        "description": "A networked game allowing multiple players to interact in real-time.",
        "category": "Network",
        "difficulty": "Advanced",
        "key_features": ["Socket programming", "Game state synchronization", "Multiple client handling"],
        "image": "multiplayer_game.png",
        "github_link": "https://github.com/asadullah48/multiplayer-pong",
        "streamlit_link": "https://multiplayer-pong.streamlit.app/",
        "tech_stack": ["Python", "Flask", "Socket.io", "JavaScript"],
        "completion_date": "2024-02-15",
        "testimonial": "This project taught me a ton about networking in Python!"
    },
    {
        "id": 21,
        "title": "Web Scraping Program",
        "description": "Application that extracts and processes data from websites automatically.",
        "category": "Data",
        "difficulty": "Intermediate",
        "key_features": ["HTML parsing", "Data extraction", "Automated browsing"],
        "image": "web_scraping.png",
        "github_link": "https://github.com/asadullah48/github-profile-explorer",
        "streamlit_link": "https://explorergithu.streamlit.app/",
        "tech_stack": ["Python", "BeautifulSoup", "Requests", "Pandas"],
        "completion_date": "2023-11-20",
        "testimonial": "My first project dealing with real-world data extraction!"
    },
]

# Create project emojis map
project_emojis = {
    "Games": "🎮",
    "Utilities": "🔧",
    "AI & Advanced": "🧠",
    "Algorithms": "📊",
    "Multimedia": "📷",
    "Network": "🌐",
    "Data": "📈"
}

# Helper function to load screenshot images
def get_project_screenshots(project_id):
    """
    Load actual screenshots from the project directories or screenshorts folder
    Falls back to placeholder images if no screenshots are found
    """
    screenshots = []

    # Try to find screenshots in the project directory
    project_name = next((p["title"] for p in projects if p["id"] == project_id), "")
    if project_name:
        # Look for screenshots in the project directory
        project_dirs = [d for d in os.listdir() if os.path.isdir(d) and project_name.lower() in d.lower()]

        for project_dir in project_dirs:
            # Check for screenshots in the project directory
            for img_path in glob.glob(f"{project_dir}/**/*.png", recursive=True) + glob.glob(f"{project_dir}/**/*.jpg", recursive=True):
                try:
                    img = Image.open(img_path)
                    screenshots.append(img)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")

        # If no screenshots found in project directory, check the screenshots folder
        if not screenshots:
            for img_path in glob.glob(f"screenshorts/project_{project_id}/*.png") + glob.glob(f"screenshorts/project_{project_id}/*.jpg"):
                try:
                    img = Image.open(img_path)
                    if img.size[0] > 0 and img.size[1] > 0:  # Make sure image is valid
                        screenshots.append(img)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")

    # If no screenshots found, use placeholder images
    if not screenshots:
        num_screenshots = random.randint(2, 4)
        screenshots = [get_placeholder_image(width=300, height=200, text=f"Screenshot {i+1} for Project {project_id}")
                for i in range(num_screenshots)]

    return screenshots

# Helper functions
def get_placeholder_image(width=300, height=200, text=""):
    """Generate a placeholder image with text."""
    colors = [
        (66, 133, 244),  # Blue
        (234, 67, 53),   # Red
        (251, 188, 5),   # Yellow
        (52, 168, 83),   # Green
        (103, 58, 183),  # Purple
        (255, 109, 0)    # Orange
    ]

    # Use the text to determine the color consistently
    color_index = sum(ord(c) for c in text) % len(colors) if text else random.randint(0, len(colors)-1)
    bg_color = colors[color_index]

    # Create the image with the background color
    img = Image.new('RGB', (width, height), color=bg_color)

    # Add text to the image if provided
    if text:
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)

            # Use a default font
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()

            # Calculate text position to center it
            text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (width//2, height//2)
            position = ((width - text_width) // 2, (height - text_height) // 2)

            # Draw the text
            draw.text(position, text, fill="white", font=font)
        except Exception as e:
            print(f"Error adding text to image: {e}")

    return img

def get_image_base64(img):
    """Convert PIL image to base64 string."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_difficulty_color(difficulty):
    """Return appropriate CSS class for difficulty level."""
    if difficulty == "Beginner":
        return "difficulty-beginner"
    elif difficulty == "Intermediate":
        return "difficulty-intermediate"
    else:
        return "difficulty-advanced"

def toggle_favorite(project_id):
    """Toggle project favorite status."""
    if project_id in st.session_state.favorites:
        st.session_state.favorites.remove(project_id)
    else:
        st.session_state.favorites.add(project_id)

def format_date(date_str):
    """Format date string to a more readable format."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

# Function to display project details
def show_project_details(project):
    # Header with project title and back button
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h1 style="margin: 0;">{project_emojis.get(project['category'], '📁')} {project['title']}</h1>
        <button onclick="document.getElementById('back_btn').click();"
                style="background: transparent;
                       color: var(--text-color);
                       border: 1px solid var(--primary-color);
                       padding: 8px 16px;
                       border-radius: 8px;
                       cursor: pointer;
                       font-weight: 500;
                       transition: all 0.3s ease;">
            ← Back to Projects
        </button>
    </div>
    """, unsafe_allow_html=True)

    # Category, difficulty, and deployment badge in a more visually appealing layout
    st.markdown(f"""
    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 25px;">
        <span class="category-label">{project['category']}</span>
        <span class="category-label {get_difficulty_color(project['difficulty'])}">{project['difficulty']}</span>
        {"<a href='" + project['streamlit_link'] + "' target='_blank'><span class='deployment-badge'>🚀 Live Demo</span></a>" if "streamlit_link" in project else ""}
        <a href="{project['github_link']}" target="_blank" style="text-decoration: none;">
            <span style="background: linear-gradient(135deg, #333, #666);
                         color: white;
                         padding: 6px 12px;
                         border-radius: 30px;
                         font-size: 0.8em;
                         display: inline-block;
                         margin: 0;
                         font-weight: 500;
                         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                         transition: all 0.3s ease;">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/github.svg" width="14" height="14" style="filter: invert(1); vertical-align: middle; margin-right: 5px;">
                GitHub Repository
            </span>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Project overview section with modern layout
    st.markdown("""
    <div style="background-color: var(--card-bg-color);
                border-radius: 16px;
                border: var(--card-border);
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: var(--card-shadow);">
        <h2 style="margin-top: 0; margin-bottom: 20px; font-size: 1.5em;">📋 Project Overview</h2>
    """, unsafe_allow_html=True)

    # Project content in columns with better layout
    col1, col2 = st.columns([1, 2])

    with col1:
        # Try to find a project image
        project_image = None
        try:
            # Look for project image in the project directory
            project_name = project["title"]
            project_dirs = [d for d in os.listdir() if os.path.isdir(d) and project_name.lower() in d.lower()]

            for project_dir in project_dirs:
                for img_path in glob.glob(f"{project_dir}/*.png") + glob.glob(f"{project_dir}/*.jpg"):
                    if not ("screenshot" in img_path.lower() or "screen" in img_path.lower()):
                        project_image = Image.open(img_path)
                        break
        except Exception as e:
            print(f"Error loading project image: {e}")

        # If no project image found, use placeholder
        if not project_image:
            project_image = get_placeholder_image(width=300, height=300, text=project["title"])

        # Display project image with styling
        st.image(project_image, caption=f"Project #{project['id']}: {project['title']}",
                 use_column_width=True, output_format="PNG", clamp=True)

        # Favorite button with better styling
        fav_status = "★ Remove from favorites" if project["id"] in st.session_state.favorites else "☆ Add to favorites"
        fav_color = "#FFD700" if project["id"] in st.session_state.favorites else "var(--text-color)"

        st.markdown(f"""
        <button onclick="document.getElementById('fav_{project['id']}').click();"
                style="background: transparent;
                       color: {fav_color};
                       border: 1px solid {fav_color};
                       padding: 8px 16px;
                       border-radius: 8px;
                       cursor: pointer;
                       font-weight: 500;
                       width: 100%;
                       margin-top: 10px;
                       transition: all 0.3s ease;">
            {fav_status}
        </button>
        """, unsafe_allow_html=True)

        # Tech stack with improved styling
        if "tech_stack" in project:
            st.markdown("### 🔧 Tech Stack")
            st.markdown("""
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
            """, unsafe_allow_html=True)

            for tech in project["tech_stack"]:
                st.markdown(f"""
                <span class="tech-pill">{tech_stacks.get(tech, '🔍')} {tech}</span>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Completion date with better styling
        if "completion_date" in project:
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 15px; background-color: rgba(var(--primary-color-rgb), 0.1); border-radius: 10px;">
                <strong>Completed on:</strong> {format_date(project['completion_date'])}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Description with better styling
        st.markdown(f"""
        <div style="margin-bottom: 25px;">
            <h3 style="margin-top: 0; margin-bottom: 15px; font-size: 1.3em;">📝 Description</h3>
            <p style="font-size: 1.1em; line-height: 1.6;">{project["description"]}</p>
        </div>
        """, unsafe_allow_html=True)

        # Key features with better styling
        st.markdown("""
        <h3 style="margin-bottom: 15px; font-size: 1.3em;">✨ Key Features</h3>
        <ul style="padding-left: 20px; margin-bottom: 25px;">
        """, unsafe_allow_html=True)

        for feature in project["key_features"]:
            st.markdown(f"""
            <li style="margin-bottom: 8px; font-size: 1.05em;">{feature}</li>
            """, unsafe_allow_html=True)

        st.markdown("</ul>", unsafe_allow_html=True)

        # Show testimonial if available with better styling
        if "testimonial" in project:
            st.markdown("""
            <h3 style="margin-bottom: 15px; font-size: 1.3em;">💬 User Feedback</h3>
            <div style="background-color: rgba(var(--primary-color-rgb), 0.1);
                        border-left: 4px solid var(--primary-color);
                        padding: 15px;
                        border-radius: 4px;
                        margin-bottom: 25px;
                        font-style: italic;">
            """, unsafe_allow_html=True)

            st.markdown(f'"{project["testimonial"]}"', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Close the project overview card
    st.markdown("</div>", unsafe_allow_html=True)

    # Code snippet if available with better styling
    if "code_snippet" in project:
        st.markdown("""
        <div style="background-color: var(--card-bg-color);
                    border-radius: 16px;
                    border: var(--card-border);
                    padding: 25px;
                    margin-bottom: 30px;
                    box-shadow: var(--card-shadow);">
            <h2 style="margin-top: 0; margin-bottom: 20px; font-size: 1.5em;">💻 Sample Code</h2>
        """, unsafe_allow_html=True)

        st.code(project["code_snippet"], language="python")
        st.markdown("</div>", unsafe_allow_html=True)

    # Screenshots gallery with better styling
    st.markdown("""
    <div style="background-color: var(--card-bg-color);
                border-radius: 16px;
                border: var(--card-border);
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: var(--card-shadow);">
        <h2 style="margin-top: 0; margin-bottom: 20px; font-size: 1.5em;">📸 Screenshots</h2>
    """, unsafe_allow_html=True)

    # Get screenshots
    screenshots = get_project_screenshots(project["id"])

    # Display screenshots in a scrollable container with better styling
    st.markdown("""
    <div class="screenshot-gallery" style="padding-bottom: 10px;">
    """, unsafe_allow_html=True)

    for idx, img in enumerate(screenshots):
        # Convert image to base64 for display
        img_base64 = get_image_base64(img)

        st.markdown(f"""
        <div style="display: inline-block; margin-right: 15px;">
            <img src="data:image/png;base64,{img_base64}" class="screenshot-img" alt="Screenshot {idx+1}" />
            <p style="text-align: center; margin-top: 8px; font-size: 0.9em; color: var(--text-color);">Screenshot {idx+1}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Add tabs for more project details with better styling
    st.markdown("""
    <div style="background-color: var(--card-bg-color);
                border-radius: 16px;
                border: var(--card-border);
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: var(--card-shadow);">
        <h2 style="margin-top: 0; margin-bottom: 20px; font-size: 1.5em;">📚 Additional Information</h2>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["✨ Features", "🎮 Demo", "💬 Feedback", "📚 Documentation"])

    with tabs[0]:
        st.markdown("### Detailed Features")
        st.markdown("""
        <div style="background-color: rgba(var(--primary-color-rgb), 0.05);
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 15px;">
            <p style="margin-top: 0;">This project demonstrates the following concepts and techniques:</p>

            <h4 style="margin-bottom: 10px; color: var(--primary-color);">1. Core Functionality</h4>
            <ul>
                <li>Implementation of the main features</li>
                <li>Error handling and edge cases</li>
            </ul>

            <h4 style="margin-bottom: 10px; margin-top: 20px; color: var(--primary-color);">2. Code Organization</h4>
            <ul>
                <li>Modular code structure</li>
                <li>Clean separation of concerns</li>
            </ul>

            <h4 style="margin-bottom: 10px; margin-top: 20px; color: var(--primary-color);">3. User Experience</h4>
            <ul>
                <li>Intuitive interface</li>
                <li>Clear feedback to user actions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("### Interactive Demo")
        if "streamlit_link" in project:
            st.markdown(f"""
            <div class="demo-section" style="text-align: center; padding: 30px;">
                <h4 style="margin-top: 0;">Try it yourself!</h4>
                <p>Experience this project live on Streamlit:</p>
                <a href="{project['streamlit_link']}" target="_blank" style="text-decoration: none;">
                    <button style="background: linear-gradient(135deg, #FF4B4B, #FF8F8F);
                                   color: white;
                                   border: none;
                                   padding: 12px 24px;
                                   border-radius: 8px;
                                   cursor: pointer;
                                   font-weight: 500;
                                   box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                                   transition: all 0.3s ease;
                                   margin-top: 10px;">
                        <span style="font-size: 1.2em;">🚀</span> Launch Demo App
                    </button>
                </a>
                <p style="margin-top: 20px; font-size: 0.9em; color: var(--text-color);">
                    Note: The app is hosted on Streamlit Cloud and may take a few seconds to load if it hasn't been accessed recently.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Demo coming soon! Check the GitHub repository for the latest updates.")

    with tabs[2]:
        st.markdown("### Project Feedback")
        st.markdown("""
        <div style="background-color: rgba(var(--primary-color-rgb), 0.05);
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 15px;
                    text-align: center;">
            <h4 style="margin-top: 0;">How would you rate this project?</h4>
            <p>Your feedback helps improve future projects!</p>
        </div>
        """, unsafe_allow_html=True)

        # Rating buttons with better styling
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.button("⭐", key=f"rate1_{project['id']}")
        with col2:
            st.button("⭐⭐", key=f"rate2_{project['id']}")
        with col3:
            st.button("⭐⭐⭐", key=f"rate3_{project['id']}")
        with col4:
            st.button("⭐⭐⭐⭐", key=f"rate4_{project['id']}")
        with col5:
            st.button("⭐⭐⭐⭐⭐", key=f"rate5_{project['id']}")

        # Comment box with better styling
        st.text_area("Leave a comment", key=f"comment_{project['id']}",
                    placeholder="Share your thoughts about this project...")

        # Submit button with better styling
        if st.button("Submit Feedback", key=f"submit_{project['id']}"):
            st.success("Thank you for your feedback! Your input is valuable for future improvements.")

    with tabs[3]:
        st.markdown("### Documentation")
        st.markdown("""
        <div style="background-color: rgba(var(--primary-color-rgb), 0.05);
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 15px;">
            <h4 style="margin-top: 0; color: var(--primary-color);">Installation</h4>
            <pre style="background-color: var(--card-bg-color);
                        padding: 15px;
                        border-radius: 8px;
                        border: var(--card-border);
                        margin-bottom: 20px;">
git clone [repository-url]
cd [project-directory]
pip install -r requirements.txt</pre>

            <h4 style="color: var(--primary-color);">Usage</h4>
            <pre style="background-color: var(--card-bg-color);
                        padding: 15px;
                        border-radius: 8px;
                        border: var(--card-border);
                        margin-bottom: 20px;">
streamlit run app.py</pre>

            <h4 style="color: var(--primary-color);">Configuration</h4>
            <p>Customize the behavior by modifying settings in the <code>config.py</code> file.</p>

            <h4 style="color: var(--primary-color); margin-top: 20px;">Contributing</h4>
            <p>Contributions are welcome! Please feel free to submit a Pull Request.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Back button (hidden, activated by the button in the header)
    if st.button("Back to Projects", key="back_btn"):
        st.session_state.show_project_details = False
        st.session_state.selected_project = None
        st.rerun()

# Function to categorize projects
def get_project_categories():
    categories = {}
    for project in projects:
        cat = project["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(project)
    return categories

# Function to generate project stats
def get_project_stats():
    total_projects = len(projects)

    # Difficulty breakdown
    difficulty_counts = {}
    for project in projects:
        difficulty = project["difficulty"]
        if difficulty not in difficulty_counts:
            difficulty_counts[difficulty] = 0
        difficulty_counts[difficulty] += 1

    # Category breakdown
    category_counts = {}
    for project in projects:
        category = project["category"]
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1

    # Timeline data (based on completion dates if available)
    timeline_data = []
    for project in projects:
        if "completion_date" in project:
            timeline_data.append({
                "id": project["id"],
                "title": project["title"],
                "date": project["completion_date"]
            })

    # Sort by date
    timeline_data.sort(key=lambda x: x["date"])

    # Tech stack usage
    tech_usage = {}
    for project in projects:
        if "tech_stack" in project:
            for tech in project["tech_stack"]:
                if tech not in tech_usage:
                    tech_usage[tech] = 0
                tech_usage[tech] += 1

    return {
        "total": total_projects,
        "difficulties": difficulty_counts,
        "categories": category_counts,
        "timeline": timeline_data,
        "tech_usage": tech_usage
    }

# Main function
def main():
    # If a project is selected to view details
    if st.session_state.show_project_details and st.session_state.selected_project:
        project = next((p for p in projects if p["id"] == st.session_state.selected_project), None)
        if project:
            show_project_details(project)
            return

    # Sidebar
    with st.sidebar:
        # Try to find a profile picture
        profile_pic = None
        try:
            # Look for profile picture in the root directory
            for img_path in glob.glob("*.png") + glob.glob("*.jpg"):
                if "profile" in img_path.lower() or "avatar" in img_path.lower() or "photo" in img_path.lower():
                    profile_pic = Image.open(img_path)
                    break

            # If not found, check the screenshots directory
            if not profile_pic:
                for img_path in glob.glob("screenshorts/*.png") + glob.glob("screenshorts/*.jpg"):
                    if "profile" in img_path.lower() or "avatar" in img_path.lower() or "photo" in img_path.lower():
                        profile_pic = Image.open(img_path)
                        break
        except Exception as e:
            print(f"Error loading profile picture: {e}")

        # If no profile picture found, use placeholder
        if not profile_pic:
            profile_pic = get_placeholder_image(200, 200, "Asadullah")

        # Display profile picture with styling
        # Convert image to base64 for custom styling
        profile_pic_base64 = get_image_base64(profile_pic)

        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <div style="text-align: center;">
                <img src="data:image/png;base64,{profile_pic_base64}"
                     width="180"
                     class="profile-image"
                     style="border-radius: 50%; border: 3px solid var(--primary-color); box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />
                <p style="margin-top: 8px; font-weight: 500;">Asadullah</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Dark mode toggle with better styling
        col1, col2 = st.columns([1, 3])
        with col1:
            dark_mode = st.toggle("🌓", value=st.session_state.dark_mode, key="toggle_dark_mode")
        with col2:
            st.markdown("<span style='margin-top: 5px; display: inline-block;'>Dark Mode</span>", unsafe_allow_html=True)

        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.markdown("""
            <script>
                document.body.classList.toggle('dark-mode');
            </script>
            """, unsafe_allow_html=True)

        # About Me section with better styling
        st.markdown("## 👨‍💻 About Me")
        st.markdown("""
        <div style="background-color: var(--card-bg-color); padding: 15px; border-radius: 10px; border: var(--card-border); margin-bottom: 20px; box-shadow: var(--card-shadow);">
            Python developer with a passion for building useful applications and solving real-world problems through code.
            <br><br>
            Currently learning and growing at GIAIC (Gen AI program), focusing on AI/ML technologies and full-stack development.
            <br><br>
            <strong>Location:</strong> Pakistan 🇵🇰<br>
            <strong>Education:</strong> Computer Science<br>
            <strong>Experience:</strong> 2+ years in Python development
        </div>
        """, unsafe_allow_html=True)

        # Quick links with improved styling
        st.markdown("## 🔗 Connect With Me")
        st.markdown("""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <a href="https://github.com/asadullah48" target="_blank" class="social-icons">
                <i class="fab fa-github"></i>
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/github.svg" width="30" height="30" style="filter: var(--icon-filter);">
            </a>
            <a href="https://www.linkedin.com/in/asadullah-shafique-a00679325/" target="_blank" class="social-icons">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/linkedin.svg" width="30" height="30" style="filter: var(--icon-filter);">
            </a>
            <a href="https://medium.com/@texcotembroiderysourcinghouse" target="_blank" class="social-icons">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/medium.svg" width="30" height="30" style="filter: var(--icon-filter);">
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Skills section with improved visualization
        st.markdown("## 🛠️ Skills")

        skills = {
            "Python": 90,
            "Web Development": 75,
            "Data Analysis": 70,
            "Machine Learning": 65,
            "UI/UX Design": 60
        }

        # Create a more visually appealing skills display
        for skill, level in skills.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{skill}**")
                st.progress(level/100)
            with col2:
                st.markdown(f"<h4 style='text-align: right; margin: 0; color: var(--primary-color);'>{level}%</h4>", unsafe_allow_html=True)

        # Download CV button
        st.markdown("""
        <div style="text-align: center; margin: 25px 0 15px 0;">
            <a href="#" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                               color: white;
                               border: none;
                               padding: 10px 20px;
                               border-radius: 8px;
                               cursor: pointer;
                               font-weight: 500;
                               box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                               transition: all 0.3s ease;
                               width: 100%;">
                    📄 Download CV
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

        # Show favorites with improved styling
        if st.session_state.favorites:
            st.markdown("## ⭐ Favorites")
            st.markdown("<div style='max-height: 300px; overflow-y: auto;'>", unsafe_allow_html=True)

            for project_id in st.session_state.favorites:
                project = next((p for p in projects if p["id"] == project_id), None)
                if project:
                    st.markdown(f"""
                    <div style="background-color: var(--card-bg-color);
                                padding: 10px 15px;
                                border-radius: 10px;
                                margin-bottom: 10px;
                                border: var(--card-border);
                                transition: all 0.3s ease;
                                box-shadow: var(--card-shadow);">
                        <span style="font-weight: 500;">{project_emojis.get(project['category'], '📁')} {project['title']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"View Details", key=f"fav_sidebar_{project_id}"):
                        st.session_state.selected_project = project_id
                        st.session_state.show_project_details = True
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
        <script>
            document.body.classList.add('dark-mode');
        </script>
        """, unsafe_allow_html=True)

    # Header with animated background and modern design
    st.markdown("""
    <div class="header-container animated-header">
        <div class="header-content">
            <h1>🐍 Python Projects Portfolio 🚀</h1>
            <p class="project-count pulse-animation">25 Project Milestone Achievement</p>
            <p class="success-message">From beginner to advanced, a journey through Python development</p>

            <div style="margin-top: 25px;">
                <a href="#projects" style="text-decoration: none;">
                    <button style="background: rgba(255,255,255,0.2);
                                   color: white;
                                   border: 2px solid white;
                                   padding: 10px 25px;
                                   border-radius: 30px;
                                   cursor: pointer;
                                   font-weight: 500;
                                   transition: all 0.3s ease;
                                   backdrop-filter: blur(5px);
                                   margin: 0 10px;">
                        Explore Projects
                    </button>
                </a>
                <a href="https://github.com/asadullah48" target="_blank" style="text-decoration: none;">
                    <button style="background: rgba(255,255,255,0.2);
                                   color: white;
                                   border: 2px solid white;
                                   padding: 10px 25px;
                                   border-radius: 30px;
                                   cursor: pointer;
                                   font-weight: 500;
                                   transition: all 0.3s ease;
                                   backdrop-filter: blur(5px);
                                   margin: 0 10px;">
                        GitHub Profile
                    </button>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # About section with card-based layout
    st.markdown('<div id="about"></div>', unsafe_allow_html=True)

    about_col1, about_col2 = st.columns([2, 1])

    with about_col1:
        st.markdown("## 🌟 About My Journey")
        st.markdown("""
        <div style="background-color: var(--card-bg-color);
                    padding: 25px;
                    border-radius: 16px;
                    border: var(--card-border);
                    box-shadow: var(--card-shadow);
                    margin-bottom: 20px;">
            <p style="font-size: 1.1em; line-height: 1.6;">
                Welcome to my portfolio of <strong>25 Python projects</strong> built with Streamlit! This collection represents my growth
                as a developer, from simple console games to complex AI applications. Each project has been a stepping stone
                in my learning journey, challenging me to expand my skills and explore new technologies.
                <br><br>
                I'm grateful to my mentors at <strong>GIAIC</strong> - Sir Zia, Sir Arif Karim, and Sir Ameen Alam - for their guidance
                and to my fellow students for their support and collaborative spirit. This portfolio is a testament to what
                can be achieved through consistent learning and practice.
                <br><br>
                Feel free to explore my projects, check out their GitHub repositories, and reach out if you'd like to
                connect or collaborate!
            </p>

            <div style="margin-top: 20px; display: flex; gap: 15px; flex-wrap: wrap;">
                <span class="tech-pill">Python</span>
                <span class="tech-pill">Streamlit</span>
                <span class="tech-pill">Data Analysis</span>
                <span class="tech-pill">Web Development</span>
                <span class="tech-pill">Game Development</span>
                <span class="tech-pill">Machine Learning</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with about_col2:
        # Key stats in visually appealing cards
        st.markdown("""
        <div style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                        color: white;
                        padding: 20px;
                        border-radius: 16px;
                        text-align: center;
                        margin-bottom: 20px;
                        box-shadow: var(--card-shadow);">
                <h1 style="font-size: 3em; margin: 0; font-weight: 800;">25</h1>
                <p style="margin: 5px 0 0 0; font-size: 1.2em;">Python Projects</p>
            </div>

            <div style="background: linear-gradient(135deg, #FF9800, #F44336);
                        color: white;
                        padding: 20px;
                        border-radius: 16px;
                        text-align: center;
                        margin-bottom: 20px;
                        box-shadow: var(--card-shadow);">
                <h1 style="font-size: 3em; margin: 0; font-weight: 800;">7</h1>
                <p style="margin: 5px 0 0 0; font-size: 1.2em;">Categories</p>
            </div>

            <div style="background: linear-gradient(135deg, #4CAF50, #8BC34A);
                        color: white;
                        padding: 20px;
                        border-radius: 16px;
                        text-align: center;
                        box-shadow: var(--card-shadow);">
                <h1 style="font-size: 3em; margin: 0; font-weight: 800;">100%</h1>
                <p style="margin: 5px 0 0 0; font-size: 1.2em;">Deployed on Streamlit</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Project Stats Overview
    stats = get_project_stats()
    st.markdown("## 📊 Portfolio Overview")

    # Stats cards in columns
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.markdown("""
        <div class="stats-card">
            <h3 style="margin: 0; color: var(--primary-color);">25</h3>
            <p style="margin: 0;">Total Projects</p>
        </div>
        """, unsafe_allow_html=True)

    with stat_cols[1]:
        st.markdown(f"""
        <div class="stats-card">
            <h3 style="margin: 0; color: #4CAF50;">{stats['difficulties'].get('Beginner', 0)}</h3>
            <p style="margin: 0;">Beginner Projects</p>
        </div>
        """, unsafe_allow_html=True)

    with stat_cols[2]:
        st.markdown(f"""
        <div class="stats-card">
            <h3 style="margin: 0; color: #FF9800;">{stats['difficulties'].get('Intermediate', 0)}</h3>
            <p style="margin: 0;">Intermediate Projects</p>
        </div>
        """, unsafe_allow_html=True)

    with stat_cols[3]:
        st.markdown(f"""
        <div class="stats-card">
            <h3 style="margin: 0; color: #F44336;">{stats['difficulties'].get('Advanced', 0)}</h3>
            <p style="margin: 0;">Advanced Projects</p>
        </div>
        """, unsafe_allow_html=True)

    # Search and Filters
    st.markdown("## 🔍 Explore Projects")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_query = st.text_input("Search Projects", placeholder="Enter keywords...", key="search")

    with col2:
        categories = ["All"] + sorted(list(set(p["category"] for p in projects)))
        category_filter = st.multiselect(
            "Filter by Category",
            options=categories[1:],
            default=[]
        )

    with col3:
        difficulty_filter = st.multiselect(
            "Filter by Difficulty",
            options=["Beginner", "Intermediate", "Advanced"],
            default=[]
        )

    # Apply filters
    filtered_projects = projects

    # Search filter
    if search_query:
        filtered_projects = [p for p in filtered_projects if
                            search_query.lower() in p["title"].lower() or
                            search_query.lower() in p["description"].lower() or
                            any(search_query.lower() in feature.lower() for feature in p["key_features"])]

    # Category filter
    if category_filter:
        filtered_projects = [p for p in filtered_projects if p["category"] in category_filter]

    # Difficulty filter
    if difficulty_filter:
        filtered_projects = [p for p in filtered_projects if p["difficulty"] in difficulty_filter]

    # View tabs
    view_tabs = st.tabs(["📱 Card View", "📋 List View", "📊 Stats", "📆 Timeline"])

    # Card View
    with view_tabs[0]:
        # Display projects in grid
        st.markdown('<div id="projects"></div>', unsafe_allow_html=True)
        st.markdown(f"## 🚀 Explore Projects ({len(filtered_projects)})")

        # Show featured project if no filters
        if not search_query and not category_filter and not difficulty_filter:
            featured_project = next((p for p in projects if p["id"] == 13), projects[0])  # Sudoku Solver or first project

            st.markdown("""
            <h3 style="display: flex; align-items: center; margin-bottom: 20px;">
                <span style="background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
                             -webkit-background-clip: text;
                             -webkit-text-fill-color: transparent;
                             margin-right: 10px;
                             font-size: 1.8em;">✨</span>
                Featured Project
            </h3>
            """, unsafe_allow_html=True)

            with st.container():
                # Create a more visually appealing featured project card
                st.markdown(f"""
                <div style="background-color: var(--card-bg-color);
                            border-radius: 16px;
                            border: var(--card-border);
                            overflow: hidden;
                            box-shadow: var(--card-shadow);
                            transition: all 0.3s ease;
                            margin-bottom: 30px;"
                     class="animated-card">
                    <div style="display: flex; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 250px; padding: 0;">
                            <div style="height: 100%; min-height: 250px; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); display: flex; align-items: center; justify-content: center;">
                                <span style="font-size: 5em; color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">{project_emojis.get(featured_project['category'], '📁')}</span>
                            </div>
                        </div>
                        <div style="flex: 2; min-width: 300px; padding: 25px;">
                            <h2 style="margin-top: 0; margin-bottom: 15px;">{featured_project['title']}</h2>

                            <div style="margin-bottom: 15px;">
                                <span class="category-label">{featured_project['category']}</span>
                                <span class="category-label {get_difficulty_color(featured_project['difficulty'])}">{featured_project['difficulty']}</span>
                                {"<a href='" + featured_project['streamlit_link'] + "' target='_blank'><span class='deployment-badge'>🚀 Live Demo</span></a>" if "streamlit_link" in featured_project else ""}
                            </div>

                            <p style="margin-bottom: 20px; font-size: 1.1em; line-height: 1.5;">{featured_project['description']}</p>

                            <div style="display: flex; gap: 15px; margin-top: 20px;">
                                <a href="javascript:void(0);" onclick="document.getElementById('featured_btn').click();" style="text-decoration: none;">
                                    <button style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                                                   color: white;
                                                   border: none;
                                                   padding: 10px 20px;
                                                   border-radius: 8px;
                                                   cursor: pointer;
                                                   font-weight: 500;
                                                   box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                                                   transition: all 0.3s ease;">
                                        View Details
                                    </button>
                                </a>
                                <a href="{featured_project['github_link']}" target="_blank" style="text-decoration: none;">
                                    <button style="background: transparent;
                                                   color: var(--text-color);
                                                   border: 1px solid var(--primary-color);
                                                   padding: 10px 20px;
                                                   border-radius: 8px;
                                                   cursor: pointer;
                                                   font-weight: 500;
                                                   transition: all 0.3s ease;">
                                        GitHub Repository
                                    </button>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Hidden button for the featured project
                if st.button("View Details", key=f"featured_btn", help="View project details"):
                    st.session_state.selected_project = featured_project["id"]
                    st.session_state.show_project_details = True
                    st.rerun()

        # Create rows with 3 columns each for project cards
        for i in range(0, len(filtered_projects), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(filtered_projects):
                    project = filtered_projects[i + j]
                    with cols[j]:
                        with st.container():
                            # Favorite status
                            fav_status = "★" if project["id"] in st.session_state.favorites else "☆"

                            # Create a more visually appealing project card
                            st.markdown(f"""
                            <div class="project-card animated-card">
                                <div style="position: absolute; top: 15px; right: 15px; font-size: 1.5em; color: {'#FFD700' if project["id"] in st.session_state.favorites else '#ccc'}; cursor: pointer;" onclick="document.getElementById('fav_list_{project['id']}').click();">
                                    {fav_status}
                                </div>

                                <div style="margin-bottom: 15px; display: flex; align-items: center;">
                                    <span style="font-size: 2em; margin-right: 10px; color: var(--primary-color);">{project_emojis.get(project['category'], '📁')}</span>
                                    <h3 style="margin: 0;">{project['title']}</h3>
                                </div>

                                <div style="margin-bottom: 15px;">
                                    <span class="category-label">{project['category']}</span>
                                    <span class="category-label {get_difficulty_color(project['difficulty'])}">{project['difficulty']}</span>
                                </div>

                                {"<a href='" + project['streamlit_link'] + "' target='_blank' style='text-decoration: none;'><span class='deployment-badge'>🚀 Live Demo</span></a>" if "streamlit_link" in project else ""}

                                <p style="margin: 15px 0; flex-grow: 1;">{project['description'][:120]}{'...' if len(project['description']) > 120 else ''}</p>

                                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                                    <button class="view-details-btn" onclick="document.getElementById('btn_{project['id']}').click();">
                                        View Details
                                    </button>
                                    <a href="{project['github_link']}" target="_blank" style="text-decoration: none;">
                                        <button style="background: transparent;
                                                       color: var(--text-color);
                                                       border: 1px solid var(--primary-color);
                                                       padding: 8px 12px;
                                                       border-radius: 8px;
                                                       cursor: pointer;
                                                       transition: all 0.3s ease;">
                                            GitHub
                                        </button>
                                    </a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Hidden buttons for functionality
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                if st.button("View", key=f"btn_{project['id']}", help="View project details"):
                                    st.session_state.selected_project = project["id"]
                                    st.session_state.show_project_details = True
                                    st.rerun()
                            with col2:
                                if st.button(fav_status, key=f"fav_list_{project['id']}", help="Add to favorites"):
                                    toggle_favorite(project["id"])

    # List View
    with view_tabs[1]:
        for project in filtered_projects:
            with st.container():
                cols = st.columns([1, 4])
                with cols[0]:
                    img = get_placeholder_image(100, 100, project["title"])
                    st.image(img)

                with cols[1]:
                    st.markdown(f"### {project_emojis.get(project['category'], '📁')} {project['title']}")

                    # Category and difficulty badges in one line
                    st.markdown(f"""
                    <span class="category-label">{project['category']}</span>
                    <span class="category-label {get_difficulty_color(project['difficulty'])}">{project['difficulty']}</span>
                    {"<span class='deployment-badge'>🚀 Live Demo</span>" if "streamlit_link" in project else ""}
                    """, unsafe_allow_html=True)

                    st.markdown(project["description"])

                    # Tech stack if available
                    if "tech_stack" in project:
                        tech_stack = ", ".join([f"{tech_stacks.get(tech, '🔍')} {tech}" for tech in project["tech_stack"]])
                        st.markdown(f"**Tech:** {tech_stack}")

                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.button(f"View Details", key=f"list_btn_{project['id']}"):
                            st.session_state.selected_project = project["id"]
                            st.session_state.show_project_details = True
                            st.experimental_rerun()
                    with col2:
                        st.markdown(f"[GitHub 🔗]({project['github_link']})")
                    with col3:
                        fav_status = "★ Favorite" if project["id"] in st.session_state.favorites else "☆ Add to favorites"
                        if st.button(fav_status, key=f"list_fav_{project['id']}"):
                            toggle_favorite(project["id"])

            st.markdown("---")

    # Stats View
    with view_tabs[2]:
        # Create category and difficulty distribution charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Projects by Category")
            # Create DataFrame for category chart
            category_df = pd.DataFrame({
                'Category': list(stats['categories'].keys()),
                'Count': list(stats['categories'].values())
            })

            fig = px.pie(
                category_df,
                values='Count',
                names='Category',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Projects by Difficulty")
            # Create DataFrame for difficulty chart
            difficulty_df = pd.DataFrame({
                'Difficulty': list(stats['difficulties'].keys()),
                'Count': list(stats['difficulties'].values())
            })

            # Set custom colors for difficulties
            difficulty_colors = {
                'Beginner': '#4CAF50',
                'Intermediate': '#FF9800',
                'Advanced': '#F44336'
            }

            color_map = {diff: difficulty_colors.get(diff, '#CCCCCC') for diff in difficulty_df['Difficulty']}

            fig = px.bar(
                difficulty_df,
                x='Difficulty',
                y='Count',
                color='Difficulty',
                color_discrete_map=color_map
            )
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        # Tech stack usage chart
        st.markdown("### Technology Usage")

        if stats['tech_usage']:
            tech_df = pd.DataFrame({
                'Technology': list(stats['tech_usage'].keys()),
                'Projects': list(stats['tech_usage'].values())
            }).sort_values('Projects', ascending=False)

            fig = px.bar(
                tech_df,
                x='Technology',
                y='Projects',
                color='Projects',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tech stack data not available for analysis.")

    # Timeline View
    with view_tabs[3]:
        st.markdown("### Project Development Timeline")

        if stats['timeline']:
            timeline_data_sorted = sorted(stats['timeline'], key=lambda x: x['date'])

            for item in timeline_data_sorted:
                project = next((p for p in projects if p["id"] == item["id"]), None)
                if project:
                    st.markdown(f"""
                    <div class="timeline-item">
                        <strong>{format_date(item['date'])}</strong>: {project_emojis.get(project['category'], '📁')} {item['title']}
                        <span class="category-label {get_difficulty_color(project['difficulty'])}" style="margin-left: 10px;">{project['difficulty']}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Timeline data not available.")

        # Add a chart showing project completion over time
        if stats['timeline']:
            # Create a dataframe with dates and cumulative project count
            dates = [item['date'] for item in stats['timeline']]
            dates.sort()

            timeline_df = pd.DataFrame({
                'Date': dates,
                'Project': range(1, len(dates) + 1)
            })

            st.markdown("### Growth Over Time")
            fig = px.line(
                timeline_df,
                x='Date',
                y='Project',
                markers=True,
                title='Cumulative Projects Completed'
            )
            fig.update_layout(yaxis_title="Total Projects")
            st.plotly_chart(fig, use_container_width=True)

# Run the app
if __name__ == "__main__":
    main()