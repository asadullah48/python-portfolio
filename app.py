import streamlit as st
import base64
from PIL import Image
import io
import pandas as pd
import plotly.express as px
import random
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Asadullah's Python Portfolio",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with improved styling, dark mode support, and animations
st.markdown("""
<style>
    /* Light mode styles */
    :root {
        --background-color: #f9f9f9;
        --text-color: #333333;
        --card-bg-color: #ffffff;
        --card-border: 1px solid #ddd;
        --primary-color: #4CAF50;
        --secondary-color: #3949AB;
        --header-bg: #f0f2f6;
        --accent-color: #FF5722;
    }
    
    /* Dark mode styles */
    .dark-mode {
        --background-color: #121212;
        --text-color: #e0e0e0;
        --card-bg-color: #1e1e1e;
        --card-border: 1px solid #333;
        --primary-color: #5CBA60;
        --secondary-color: #4959CB;
        --header-bg: #1a1a1a;
        --accent-color: #FF7043;
    }
    
    body {
        color: var(--text-color);
        background-color: var(--background-color);
        transition: all 0.3s ease;
    }
    
    .project-card {
        background-color: var(--card-bg-color);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: var(--card-border);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .category-label {
        background-color: var(--primary-color);
        color: white;
        padding: 4px 10px;
        border-radius: 30px;
        font-size: 0.8em;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    
    .difficulty-beginner {
        background-color: #4CAF50;
    }
    
    .difficulty-intermediate {
        background-color: #FF9800;
    }
    
    .difficulty-advanced {
        background-color: #F44336;
    }
    
    .header-container {
        text-align: center;
        padding: 30px;
        background-color: var(--header-bg);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .project-count {
        font-size: 1.5em;
        color: var(--primary-color);
        font-weight: bold;
        margin: 15px 0;
    }
    
    .success-message {
        font-style: italic;
        color: var(--secondary-color);
        font-size: 1.1em;
    }
    
    .view-details-btn {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: auto;
        transition: background-color 0.3s ease;
    }
    
    .view-details-btn:hover {
        background-color: var(--secondary-color);
    }
    
    .search-box {
        border-radius: 30px !important;
        border: var(--card-border) !important;
        padding: 10px 20px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: var(--card-bg-color);
    }
    
    .social-icons {
        font-size: 24px;
        margin: 0 10px;
        color: var(--primary-color);
        text-decoration: none;
    }
    
    .github-stats {
        background-color: var(--card-bg-color);
        padding: 15px;
        border-radius: 10px;
        border: var(--card-border);
        margin-bottom: 20px;
    }
    
    /* Favorite button styles */
    .favorite-btn {
        background: none;
        border: none;
        color: #FFD700;
        font-size: 1.5em;
        cursor: pointer;
        position: absolute;
        top: 10px;
        right: 10px;
    }
    
    /* Screenshot gallery styles */
    .screenshot-gallery {
        display: flex;
        overflow-x: auto;
        padding: 10px 0;
        gap: 10px;
        margin: 15px 0;
    }
    
    .screenshot-img {
        max-height: 200px;
        border-radius: 8px;
        border: var(--card-border);
        transition: transform 0.2s ease;
    }
    
    .screenshot-img:hover {
        transform: scale(1.05);
    }
    
    /* Tech stack pill */
    .tech-pill {
        background-color: var(--accent-color);
        color: white;
        padding: 3px 8px;
        border-radius: 15px;
        font-size: 0.75em;
        margin-right: 5px;
        display: inline-block;
    }
    
    /* Project stats */
    .stats-card {
        background-color: var(--card-bg-color);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: var(--card-border);
    }
    
    /* Demo section */
    .demo-section {
        background-color: rgba(0, 0, 0, 0.03);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Timeline */
    .timeline-container {
        position: relative;
        padding-left: 30px;
        margin-bottom: 20px;
    }
    
    .timeline-item {
        position: relative;
        padding-bottom: 15px;
    }
    
    .timeline-item:before {
        content: '';
        position: absolute;
        left: -30px;
        top: 0;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background-color: var(--primary-color);
    }
    
    .timeline-item:after {
        content: '';
        position: absolute;
        left: -23px;
        top: 15px;
        width: 2px;
        height: 100%;
        background-color: var(--primary-color);
    }
    
    .timeline-item:last-child:after {
        display: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-color);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    
    /* Make sure emojis display at a reasonable size */
    .emoji {
        font-size: 1.5em;
    }
    
    /* Deployment badge */
    .deployment-badge {
        background-color: #9C27B0;
        color: white;
        padding: 4px 10px;
        border-radius: 30px;
        font-size: 0.8em;
        display: inline-block;
        margin: 5px 0;
    }
    
    /* Animation for cards */
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .animated-card {
        animation: slideIn 0.5s ease-out;
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
        "title": "Guess the Number Game (User)",
        "description": "A reverse guessing game where the player thinks of a number and the computer tries to guess it.",
        "category": "Games",
        "difficulty": "Beginner",
        "key_features": ["Binary search algorithm", "AI decision making", "Feedback processing"],
        "image": "guess_number_user.png",
        "github_link": "https://github.com/asadullah48/guess-the-number-game",
        "streamlit_link": "https://guess-number-user-asadullah.streamlit.app/",
        "tech_stack": ["Python", "Streamlit"],
        "completion_date": "2023-07-05",
        "testimonial": "This was a fun twist on the classic guess the number game!",
        "code_snippet": """def computer_guess(x):
    low = 1
    high = x
    feedback = ''
    
    while feedback != 'c':
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low
        
        feedback = input(f'Is {guess} too high (H), too low (L), or correct (C)? ').lower()
        
        if feedback == 'h':
            high = guess - 1
        elif feedback == 'l':
            low = guess + 1
    
    print(f'Yay! The computer guessed your number, {guess}, correctly!')"""
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
    This would typically load actual screenshots from a directory
    For now, we'll use placeholder images
    """
    # In a real implementation, you would load actual images from a directory
    # such as f"screenshots/{project_id}/"
    num_screenshots = random.randint(2, 5)  # Simulating a random number of screenshots
    return [get_placeholder_image(width=300, height=200, text=f"Screenshot {i+1} for Project {project_id}") 
            for i in range(num_screenshots)]

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
    st.markdown(f"# {project_emojis.get(project['category'], '📁')} {project['title']}")
    
    # Category, difficulty, and deployment badge
    badges_col1, badges_col2, badges_col3 = st.columns([1, 1, 2])
    with badges_col1:
        st.markdown(f"""
        <span class="category-label">{project['category']}</span>
        """, unsafe_allow_html=True)
    with badges_col2:
        st.markdown(f"""
        <span class="category-label {get_difficulty_color(project['difficulty'])}">{project['difficulty']}</span>
        """, unsafe_allow_html=True)
    with badges_col3:
        if "streamlit_link" in project:
            st.markdown(f"""
            <a href="{project['streamlit_link']}" target="_blank">
                <span class="deployment-badge">🚀 Live Demo</span>
            </a>
            """, unsafe_allow_html=True)
    
    # Project image and info in columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        img = get_placeholder_image(text=project["title"])
        st.image(img, caption=f"Project #{project['id']}: {project['title']}")
        
        # GitHub link button
        st.markdown(f"[View on GitHub 🔗]({project['github_link']})")
        
        # Favorite button
        fav_status = "★ Remove from favorites" if project["id"] in st.session_state.favorites else "☆ Add to favorites"
        if st.button(fav_status, key=f"fav_{project['id']}"):
            toggle_favorite(project["id"])
        
        # Tech stack
        if "tech_stack" in project:
            st.markdown("### 🔧 Tech Stack")
            for tech in project["tech_stack"]:
                st.markdown(f"""
                <span class="tech-pill">{tech_stacks.get(tech, '🔍')} {tech}</span>
                """, unsafe_allow_html=True)
        
        # Completion date
        if "completion_date" in project:
            st.markdown(f"**Completed on:** {format_date(project['completion_date'])}")
    
    with col2:
        st.markdown(f"### 📝 Description")
        st.markdown(project["description"])
        
        st.markdown("### ✨ Key Features")
        for feature in project["key_features"]:
            st.markdown(f"- {feature}")
        
        # Show testimonial if available
        if "testimonial" in project:
            st.markdown("### 💬 User Feedback")
            st.info(f'"{project["testimonial"]}"')
        
        # Code snippet if available
        if "code_snippet" in project:
            st.markdown("### 💻 Sample Code")
            st.code(project["code_snippet"], language="python")
    
    # Screenshots gallery
    st.markdown("### 📸 Screenshots")
    screenshots = get_project_screenshots(project["id"])
    
    # Display screenshots in a scrollable container
    st.markdown("""
    <div class="screenshot-gallery">
    """, unsafe_allow_html=True)
    
    screenshot_cols = st.columns(len(screenshots))
    for idx, img in enumerate(screenshots):
        with screenshot_cols[idx]:
            st.image(img, caption=f"Screenshot {idx+1}", use_container_width=True)
    
    # Add tabs for more project details
    tabs = st.tabs(["✨ Features", "🎮 Demo", "💬 Feedback", "📚 Documentation"])
    
    with tabs[0]:
        st.markdown("### Detailed Features")
        st.markdown("""
        This project demonstrates the following concepts and techniques:
        
        1. **Core Functionality**
           - Implementation of the main features
           - Error handling and edge cases
           
        2. **Code Organization**
           - Modular code structure
           - Clean separation of concerns
           
        3. **User Experience**
           - Intuitive interface
           - Clear feedback to user actions
        """)
    
    with tabs[1]:
        st.markdown("### Interactive Demo")
        if "streamlit_link" in project:
            st.markdown(f"""
            <div class="demo-section">
                <h4>Try it yourself!</h4>
                <p>Experience this project live on Streamlit:</p>
                <a href="{project['streamlit_link']}" target="_blank">
                    <button style="background-color: #FF4B4B; color: white; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer;">
                        Launch Demo App
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Demo coming soon! Check the GitHub repository for the latest updates.")
    
    with tabs[2]:
        st.write("How would you rate this project?")
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
        
        st.text_area("Leave a comment", key=f"comment_{project['id']}")
        if st.button("Submit Feedback", key=f"submit_{project['id']}"):
            st.success("Thank you for your feedback!")
    
    with tabs[3]:
        st.markdown("### Documentation")
        st.markdown("""
        #### Installation
        ```bash
        git clone [repository-url]
        cd [project-directory]
        pip install -r requirements.txt
        ```
        
        #### Usage
        ```bash
        streamlit run app.py
        ```
        
        #### Configuration
        Customize the behavior by modifying settings in the `config.py` file.
        
        #### Contributing
        Contributions are welcome! Please feel free to submit a Pull Request.
        """)
    
    # Back button
    if st.button("← Back to Projects"):
        st.session_state.show_project_details = False
        st.session_state.selected_project = None
        st.experimental_rerun()

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
        st.image(get_placeholder_image(200, 200, "Profile"), caption="Asadullah")
        
        st.markdown("## 👨‍💻 About Me")
        st.markdown("""
        Python developer with a passion for building useful applications. 
        Currently learning and growing at GIAIC (Gen AI program).
        """)
        
        # Dark mode toggle
        if st.toggle("🌓 Dark Mode", key="toggle_dark_mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.markdown("""
            <script>
                document.body.classList.toggle('dark-mode');
            </script>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick links
        st.markdown("## 🔗 Quick Links")
        st.markdown("[🐙 GitHub](https://github.com/asadullah48)")
        st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/asadullah-shafique-a00679325/)")
        st.markdown("[📝 Blog](https://medium.com/@texcotembroiderysourcinghouse")
        
        st.markdown("---")
        
        # Skills section
        st.markdown("## 🛠️ Skills")
        skills = {
            "Python": 90,
            "Web Development": 75,
            "Data Analysis": 70,
            "Machine Learning": 65,
            "UI/UX Design": 60
        }
        
        for skill, level in skills.items():
            st.markdown(f"**{skill}**")
            st.progress(level/100)
        
        st.markdown("---")
        
        # Show favorites
        # ... inside the sidebar ...
        if st.session_state.favorites:
            st.markdown("## ⭐ Favorites")
            for project_id in st.session_state.favorites:
                project = next((p for p in projects if p["id"] == project_id), None)
                if project:
                    # Corrected: Removed the duplicate/incomplete 'if' statement above
                    if st.button(f"🔖 {project['title']}", key=f"fav_sidebar_{project_id}"): 
                        st.session_state.selected_project = project_id
                        st.session_state.show_project_details = True
                        st.experimental_rerun()

    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
        <script>
            document.body.classList.add('dark-mode');
        </script>
        """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🐍 Python Projects Portfolio 🚀</h1>
        <p class="project-count">25 Project Milestone Achievement</p>
        <p class="success-message">From beginner to advanced, a journey through Python development</p>
    </div>
    """, unsafe_allow_html=True)
    
    # About section
    st.markdown("## 🌟 About My Journey")
    st.write("""
    Welcome to my portfolio of 25 Python projects built with Streamlit! This collection represents my growth 
    as a developer, from simple console games to complex AI applications. Each project has been a stepping stone 
    in my learning journey, challenging me to expand my skills and explore new technologies.
    
    I'm grateful to my mentors at GIAIC - Sir Zia, Sir Arif Karim, and Sir Ameen Alam - for their guidance 
    and to my fellow students for their support and collaborative spirit. This portfolio is a testament to what 
    can be achieved through consistent learning and practice.
    
    Feel free to explore my projects, check out their GitHub repositories, and reach out if you'd like to 
    connect or collaborate!
    """)
    
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
        st.markdown(f"### Projects ({len(filtered_projects)})")
        
        # Show featured project if no filters
        if not search_query and not category_filter and not difficulty_filter:
            featured_project = next((p for p in projects if p["id"] == 13), projects[0])  # Sudoku Solver or first project
            st.markdown("#### ✨ Featured Project")
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    img = get_placeholder_image(text=featured_project["title"])
                    st.image(img, caption=f"Featured: {featured_project['title']}")
                
                with col2:
                    st.markdown(f"### {project_emojis.get(featured_project['category'], '📁')} {featured_project['title']}")
                    
                    # Category and difficulty badges
                    st.markdown(f"""
                    <span class="category-label">{featured_project['category']}</span>
                    <span class="category-label {get_difficulty_color(featured_project['difficulty'])}">{featured_project['difficulty']}</span>
                    """, unsafe_allow_html=True)
                    
                    # Show streamlit link badge if available
                    if "streamlit_link" in featured_project:
                        st.markdown(f"""
                        <a href="{featured_project['streamlit_link']}" target="_blank">
                            <span class="deployment-badge">🚀 Live Demo</span>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(featured_project["description"])
                    
                    # View details button
                    if st.button("View Details", key=f"featured_btn"):
                        st.session_state.selected_project = featured_project["id"]
                        st.session_state.show_project_details = True
                        st.experimental_rerun()
            
            st.markdown("---")
        
        # Create rows with 3 columns each
        for i in range(0, len(filtered_projects), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(filtered_projects):
                    project = filtered_projects[i + j]
                    with cols[j]:
                        with st.container():
                            # Favorite status
                            fav_status = "★" if project["id"] in st.session_state.favorites else "☆"
                            
                            st.markdown(f"""
                            <div class="project-card animated-card">
                                <h3>{project_emojis.get(project['category'], '📁')} {project['title']}</h3>
                                <span class="category-label">{project['category']}</span>
                                <span class="category-label {get_difficulty_color(project['difficulty'])}">{project['difficulty']}</span>
                                {"<span class='deployment-badge'>🚀 Live Demo</span>" if "streamlit_link" in project else ""}
                                <p>{project['description'][:100]}{'...' if len(project['description']) > 100 else ''}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                if st.button(f"View Details", key=f"btn_{project['id']}"):
                                    st.session_state.selected_project = project["id"]
                                    st.session_state.show_project_details = True
                                    st.experimental_rerun()
                            with col2:
                                if st.button(fav_status, key=f"fav_list_{project['id']}"):
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