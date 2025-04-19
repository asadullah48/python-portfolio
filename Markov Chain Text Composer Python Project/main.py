import streamlit as st
import os
import pandas as pd
from markov_chain import MarkovChainGenerator

def main():
    st.set_page_config(
        page_title="Markov Text Generator",
        page_icon="🔤",
        layout="wide"
    )
    
    st.title("🔄 Markov Chain Text Generator")
    st.markdown("""
    Generate realistic text using Markov Chains. Upload a text file or enter your own text to create
    a model that generates new content based on the patterns in your input.
    """)
    
    # Sidebar for parameters
    st.sidebar.header("⚙️ Parameters")
    order = st.sidebar.slider("Chain Order (words to consider)", 1, 5, 2, 
                          help="Higher values create more coherent but less creative text")
    length = st.sidebar.slider("Output Length (words)", 10, 500, 100)
    
    # Initialize the generator
    generator = MarkovChainGenerator(order=order)
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📝 Enter Text", "📁 Upload File", "📊 Analysis"])
    
    with tab1:
        st.subheader("Enter Your Text")
        
        # Sample texts dropdown
        sample_option = st.selectbox(
            "Or choose a sample text:",
            ["None", "Lorem Ipsum", "Shakespeare", "Programming Concepts"]
        )
        
        sample_texts = {
            "Lorem Ipsum": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "Shakespeare": "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles And by opposing end them. To die—to sleep, No more; and by a sleep to say we end The heart-ache and the thousand natural shocks That flesh is heir to: 'tis a consummation Devoutly to be wish'd.",
            "Programming Concepts": "Python is a high-level, interpreted programming language. It is known for its readability and simplicity. Functions are first-class objects in Python, which means they can be assigned to variables, passed as arguments, and returned from other functions. Object-oriented programming is supported through classes and inheritance. Python's standard library provides many modules for common tasks."
        }
        
        if sample_option != "None":
            text_input = st.text_area("Input Text", value=sample_texts[sample_option], height=200)
        else:
            text_input = st.text_area("Input Text", height=200, 
                                   placeholder="Enter text here to build a Markov chain...")
        
        starting_words = st.text_input("Starting Words (optional, comma-separated)", 
                                    placeholder="e.g., The cat, Once upon")
        
        start_button = st.button("🚀 Generate Text", key="generate_text")
        
        if start_button and text_input:
            generator.build_chain(text_input)
            
            start_list = None
            if starting_words:
                start_list = starting_words.split(',')
                
            generated_text = generator.generate_text(length=length, start_words=start_list)
            
            st.subheader("📝 Generated Text:")
            st.markdown(f"*{generated_text}*")
            
            # Add download button for generated text
            st.download_button(
                label="Download Generated Text",
                data=generated_text,
                file_name="markov_generated_text.txt",
                mime="text/plain"
            )
    
    with tab2:
        st.subheader("Upload a Text File")
        uploaded_file = st.file_uploader("Choose a file", type=['txt'])
        
        if uploaded_file is not None:
            # Read file as string and display preview
            file_text = uploaded_file.getvalue().decode("utf-8")
            st.write("File Preview:")
            st.text(file_text[:500] + ("..." if len(file_text) > 500 else ""))
            
            starting_words_file = st.text_input("Starting Words (optional, comma-separated)", 
                                           placeholder="e.g., The cat, Once upon", key="start_file")
            
            generate_from_file = st.button("🚀 Generate from File", key="generate_file")
            
            if generate_from_file:
                generator.build_chain(file_text)
                
                start_list = None
                if starting_words_file:
                    start_list = starting_words_file.split(',')
                    
                generated_text = generator.generate_text(length=length, start_words=start_list)
                
                st.subheader("📝 Generated Text:")
                st.markdown(f"*{generated_text}*")
                
                # Add download button for generated text
                st.download_button(
                    label="Download Generated Text",
                    data=generated_text,
                    file_name=f"markov_generated_{uploaded_file.name}",
                    mime="text/plain"
                )
    
    with tab3:
        st.subheader("Markov Chain Analysis")
        
        text_for_analysis = st.text_area(
            "Enter text for analysis:", 
            height=150,
            placeholder="Enter text to analyze its Markov chain properties...",
            key="analysis_text"
        )
        
        analyze_button = st.button("📊 Analyze Text", key="analyze")
        
        if analyze_button and text_for_analysis:
            # Build the chain and analyze
            chain = generator.build_chain(text_for_analysis)
            
            # Display stats
            st.write(f"📊 **Chain Statistics:**")
            st.write(f"- Total number of states: {len(chain)}")
            
            # Find most common transitions
            transition_counts = {}
            for key, values in chain.items():
                for word in values:
                    state_str = ' '.join(key)
                    transition = f"'{state_str}' → '{word}'"
                    if transition in transition_counts:
                        transition_counts[transition] += 1
                    else:
                        transition_counts[transition] = 1
            
            # Display top transitions
            if transition_counts:
                st.write("🔝 **Top Transitions:**")
                
                # Convert to dataframe for better display
                transitions_df = pd.DataFrame({
                    'Transition': list(transition_counts.keys()),
                    'Count': list(transition_counts.values())
                }).sort_values('Count', ascending=False).head(10)
                
                st.dataframe(transitions_df, use_container_width=True)
                
                # Find dead ends (states with no outgoing transitions)
                all_states = set()
                for key in chain.keys():
                    all_states.add(' '.join(key))
                    
                # Calculate vocabulary size
                vocabulary = set()
                for key in chain.keys():
                    for word in key:
                        vocabulary.add(word)
                for values in chain.values():
                    for word in values:
                        vocabulary.add(word)
                
                st.write(f"📚 **Vocabulary size:** {len(vocabulary)} unique words")
                st.write(f"🔄 **Average transitions per state:** {sum(len(v) for v in chain.values()) / len(chain) if chain else 0:.2f}")
                
                # Generate text sample for comparison
                st.write("💡 **Sample generation:**")
                sample = generator.generate_text(length=30)
                st.write(sample)

if __name__ == "__main__":
    main()