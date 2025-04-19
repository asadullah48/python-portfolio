import streamlit as st
import random

def main():
    st.set_page_config(page_title="Mad Libs Fun!", page_icon="📖")
    
    st.title("📖 Mad Libs Generator")
    st.markdown("Fill in the blanks and create a funny story!")
    
    # Sidebar for customization
    with st.sidebar:
        st.header("Settings ⚙️")
        theme = st.selectbox("Choose a theme:", ("Fantasy", "Sci-Fi", "Pirate", "Zombie"))
        difficulty = st.radio("Difficulty:", ("Easy", "Medium", "Hard"))
    
    # Input fields (organized in columns for better UI)
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name:", "Alex").strip().title()
        place = st.text_input("Place:", "the enchanted forest").strip()
        animal = st.text_input("Animal:", "dragon").strip().lower()
    
    with col2:
        verb = st.text_input("Action (verb):", "dancing").strip().lower()
        adjective = st.text_input("Adjective:", "sparkly").strip().lower()
        food = st.text_input("Food:", "pizza").strip().lower()
    
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
        ]
    }
    
    # Generate story button
    if st.button("Generate Story ✨", type="primary"):
        if not all([name, place, animal, verb, adjective, food]):
            st.warning("Please fill all fields!")
        else:
            selected_story = random.choice(stories[theme])
            st.balloons()  # Celebration effect!
            
            # Display the story in a styled box
            st.subheader("Your Mad Libs Story:")
            st.markdown(
                f"""
                <div style="
                    background: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid #ff4b4b;
                    margin: 10px 0;
                ">
                {selected_story}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Download option
            st.download_button(
                label="Download Story 📥",
                data=selected_story,
                file_name="mad_libs_story.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()