import streamlit as st
import random
import json
import os
from datetime import datetime
import base64
from pathlib import Path

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Function to load story history
def load_history():
    if os.path.exists("story_history.json"):
        with open("story_history.json", "r") as f:
            return json.load(f)
    return []

# Function to save story to history
def save_to_history(story_data):
    history = load_history()
    history.append(story_data)
    # Keep only the last 10 stories
    if len(history) > 10:
        history = history[-10:]
    with open("story_history.json", "w") as f:
        json.dump(history, f)

# Function to create custom CSS
def apply_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .main-container {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px 15px;
            transition: all 0.3s;
        }
        .stTextInput > div > div > input:focus {
            border-color: #ff4b4b;
            box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2);
        }

        /* Button styling */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        /* Story box styling */
        .story-box {
            background: rgba(255, 255, 255, 0.9);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #ff4b4b;
            margin: 15px 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            font-size: 1.1em;
            line-height: 1.6;
        }

        /* Sidebar styling */
        .css-1d391kg {
            background-color: rgba(247, 247, 247, 0.9);
        }

        /* Header styling */
        h1, h2, h3 {
            color: #333;
            font-family: 'Poppins', sans-serif;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 8px 8px 0 0;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ff4b4b !important;
            color: white !important;
        }

        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #ff4b4b;
        }
        </style>
    """, unsafe_allow_html=True)

# Function to generate random inputs
def generate_random_inputs():
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Riley", "Casey", "Quinn", "Avery", "Skyler", "Dakota"]
    places = ["enchanted forest", "ancient temple", "abandoned spaceship", "haunted mansion", "underwater city",
              "floating island", "crystal cave", "desert oasis", "volcanic lair", "frozen tundra"]
    animals = ["dragon", "phoenix", "kraken", "unicorn", "griffin", "werewolf", "chimera", "basilisk",
               "manticore", "centaur"]
    verbs = ["dancing", "singing", "fighting", "meditating", "flying", "swimming", "teleporting",
             "transforming", "glowing", "levitating"]
    adjectives = ["sparkly", "mysterious", "ancient", "magical", "ferocious", "gentle", "enormous",
                  "microscopic", "ethereal", "chaotic"]
    foods = ["pizza", "enchanted berries", "golden apples", "dragon fruit", "ambrosia", "cosmic ice cream",
             "phoenix eggs", "mermaid tears", "moonlight cookies", "star dust cake"]

    return {
        "name": random.choice(names),
        "place": random.choice(places),
        "animal": random.choice(animals),
        "verb": random.choice(verbs),
        "adjective": random.choice(adjectives),
        "food": random.choice(foods)
    }

def main():
    # Page configuration
    st.set_page_config(
        page_title="Mad Libs Adventure",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    # Download background image if it doesn't exist
    bg_image_path = "images/background.jpg"
    if not os.path.exists(bg_image_path):
        # Create a default gradient background
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Set background image
        set_background(bg_image_path)

    # Apply custom CSS
    apply_custom_css()

    # App header with animation
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3em; margin-bottom: 0;">📖 Mad Libs Adventure</h1>
            <p style="font-size: 1.2em; opacity: 0.8;">Create hilarious stories with just a few words!</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar for customization
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="font-size: 1.8em;">⚙️ Story Settings</h2>
            </div>
        """, unsafe_allow_html=True)

        theme = st.selectbox(
            "Choose a theme:",
            ("Fantasy", "Sci-Fi", "Pirate", "Zombie", "Superhero"),
            help="Select the theme for your story"
        )

        difficulty = st.radio(
            "Difficulty:",
            ("Easy", "Medium", "Hard"),
            help="Easy: Basic words, Medium: More descriptive, Hard: Complex scenarios"
        )

        # Visual theme selector
        st.markdown("### 🎨 Visual Theme")
        color_theme = st.color_picker("Accent Color", "#ff4b4b")

        # Random fill option
        st.markdown("### 🎲 Quick Options")
        if st.button("Random Fill", help="Fill all fields with random values"):
            st.session_state.random_fill = True

        # Reset button
        if st.button("Reset All Fields", help="Clear all input fields"):
            st.session_state.reset_fields = True

    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["📝 Create Story", "📚 Story History", "ℹ️ About"])

    with tab1:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)

        # Initialize session state for random fill
        if 'random_fill' not in st.session_state:
            st.session_state.random_fill = False

        # Initialize session state for reset
        if 'reset_fields' not in st.session_state:
            st.session_state.reset_fields = False

        # Get random inputs if button was clicked
        random_inputs = {}
        if st.session_state.random_fill:
            random_inputs = generate_random_inputs()
            st.session_state.random_fill = False

        # Reset fields if button was clicked
        if st.session_state.reset_fields:
            random_inputs = {"name": "", "place": "", "animal": "", "verb": "", "adjective": "", "food": ""}
            st.session_state.reset_fields = False

        # Input fields (organized in columns for better UI)
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Name:",
                random_inputs.get("name", "Alex") if st.session_state.random_fill else "Alex"
            ).strip().title()

            place = st.text_input(
                "Place:",
                random_inputs.get("place", "the enchanted forest") if st.session_state.random_fill else "the enchanted forest"
            ).strip()

            animal = st.text_input(
                "Animal:",
                random_inputs.get("animal", "dragon") if st.session_state.random_fill else "dragon"
            ).strip().lower()

        with col2:
            verb = st.text_input(
                "Action (verb):",
                random_inputs.get("verb", "dancing") if st.session_state.random_fill else "dancing"
            ).strip().lower()

            adjective = st.text_input(
                "Adjective:",
                random_inputs.get("adjective", "sparkly") if st.session_state.random_fill else "sparkly"
            ).strip().lower()

            food = st.text_input(
                "Food:",
                random_inputs.get("food", "pizza") if st.session_state.random_fill else "pizza"
            ).strip().lower()

        # Calculate progress
        filled_fields = sum(1 for field in [name, place, animal, verb, adjective, food] if field)
        progress = filled_fields / 6

        # Progress bar
        st.progress(progress, text=f"Completion: {int(progress * 100)}%")

        if progress < 1:
            st.info(f"Fill in {6 - filled_fields} more field(s) to complete your story!")

        # Story templates based on theme
        stories = {
            "Fantasy": [
                f"Once upon a time, **{name}** ventured into **{place}**, where a **{adjective} {animal}** was **{verb}**. " +
                f"They shared **{food}**, and legend says they still rule the kingdom together!",

                f"Deep in **{place}**, **{name}** discovered a **{animal}** with **{adjective}** powers. " +
                f"After **{verb}** together and eating **{food}**, they saved the realm from darkness!"
            ],
            "Sci-Fi": [
                f"In the year 3023, **{name}** landed on **{place}**, encountering a **{adjective} {animal}** " +
                f"that communicated by **{verb}**. A peace treaty was signed over **{food}**.",

                f"While exploring **{place}**, astronaut **{name}** was ambushed by a **{adjective} {animal}**. " +
                f"Luckily, **{verb}** distracted it long enough to share **{food}** and form an alliance."
            ],
            "Pirate": [
                f"Captain **{name}** sailed to **{place}**, where a **{adjective} {animal}** " +
                f"was **{verb}** on the deck. The crew fed it **{food}**, and it joined their adventures!",

                f"After a storm, **{name}** washed ashore **{place}**, finding a **{adjective} {animal}** " +
                f"**{verb}** near treasure. They bonded over **{food}** and became pirate partners!"
            ],
            "Zombie": [
                f"In the zombie apocalypse, **{name}** hid in **{place}**, but a **{adjective} {animal}** " +
                f"started **{verb}** nearby. Surprisingly, it just wanted **{food}** and became a loyal pet!",

                f"**{name}** braved **{place}**, dodging zombies until a **{adjective} {animal}** " +
                f"saved them by **{verb}**. They celebrated with **{food}**, the last meal before the world ended."
            ],
            "Superhero": [
                f"Superhero **{name}** was protecting **{place}** when a **{adjective} {animal}** " +
                f"started **{verb}** in the city center. They bonded over **{food}** and became an unstoppable crime-fighting duo!",

                f"While **{verb}** in **{place}**, **{name}** discovered their superpowers after encountering a **{adjective} {animal}**. " +
                f"Their first heroic act? Saving the world's supply of **{food}** from evil forces!"
            ]
        }

        # Generate story button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_button = st.button("✨ Generate Story ✨", type="primary", use_container_width=True)

        # Story generation
        if generate_button:
            if not all([name, place, animal, verb, adjective, food]):
                st.warning("Please fill all fields to generate your story!")
            else:
                selected_story = random.choice(stories[theme])
                st.balloons()  # Celebration effect!

                # Save to history
                story_data = {
                    "theme": theme,
                    "story": selected_story,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "inputs": {
                        "name": name,
                        "place": place,
                        "animal": animal,
                        "verb": verb,
                        "adjective": adjective,
                        "food": food
                    }
                }
                save_to_history(story_data)

                # Display the story in a styled box
                st.subheader("✨ Your Mad Libs Story:")
                st.markdown(
                    f"""
                    <div class="story-box">
                        <h3 style="margin-top: 0; color: #ff4b4b;">A {theme} Adventure</h3>
                        <p>{selected_story}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    # Download option
                    st.download_button(
                        label="📥 Download Story",
                        data=f"# A {theme} Mad Libs Adventure\n\n{selected_story}\n\nCreated on {datetime.now().strftime('%Y-%m-%d')}",
                        file_name=f"mad_libs_{theme.lower()}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col2:
                    # Copy to clipboard button (simulated with JavaScript)
                    st.markdown(
                        f"""
                        <button
                            onclick="navigator.clipboard.writeText(`{selected_story}`);this.innerHTML='✓ Copied!';"
                            style="
                                background-color: #4CAF50;
                                border: none;
                                color: white;
                                padding: 10px 24px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 16px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border-radius: 10px;
                                width: 100%;
                            "
                        >
                            📋 Copy to Clipboard
                        </button>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:
                    # Share button (simulated)
                    st.markdown(
                        f"""
                        <button
                            onclick="alert('Story ready to share!');"
                            style="
                                background-color: #2196F3;
                                border: none;
                                color: white;
                                padding: 10px 24px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 16px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border-radius: 10px;
                                width: 100%;
                            "
                        >
                            🔗 Share Story
                        </button>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown('</div>', unsafe_allow_html=True)

    # History tab
    with tab2:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.subheader("📚 Your Story History")

        history = load_history()
        if not history:
            st.info("You haven't created any stories yet. Go to the 'Create Story' tab to get started!")
        else:
            for i, story_data in enumerate(reversed(history)):
                with st.expander(f"{story_data['theme']} Story - {story_data['date']}"):
                    st.markdown(
                        f"""
                        <div class="story-box" style="border-left-color: {'#ff4b4b' if i % 2 == 0 else '#4CAF50'};">
                            <p>{story_data['story']}</p>
                            <p><small>Created on {story_data['date']}</small></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Recreate button
                    if st.button(f"Recreate This Story", key=f"recreate_{i}"):
                        # Set session state to these values
                        st.session_state.recreate_story = story_data['inputs']
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # About tab
    with tab3:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.subheader("ℹ️ About Mad Libs Adventure")

        st.markdown("""
            ### What is Mad Libs?

            Mad Libs is a word game where players fill in blanks with different types of words (nouns, verbs, adjectives, etc.)
            to create often hilarious and nonsensical stories.

            ### How to Play

            1. Fill in all the word fields in the "Create Story" tab
            2. Click the "Generate Story" button
            3. Enjoy your unique, personalized story!
            4. Download or share your creation

            ### Features

            - **Multiple Themes**: Choose from Fantasy, Sci-Fi, Pirate, Zombie, and Superhero stories
            - **Random Fill**: Quickly generate a story with random words
            - **Story History**: Keep track of your previous creations
            - **Download & Share**: Save your stories or share them with friends

            ### Tips for Fun Stories

            - Use unusual or unexpected words
            - Try combining contrasting themes (like a "fancy" adjective with a "silly" noun)
            - Read your story out loud for maximum enjoyment!

            ---

            Created with ❤️ using Python and Streamlit
        """)

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()