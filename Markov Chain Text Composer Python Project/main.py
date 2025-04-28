import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from markov_chain import MarkovChainGenerator
from utils import set_background, load_css, create_footer, get_sample_texts

def main():
    # Page configuration
    st.set_page_config(
        page_title="Markov Text Generator",
        page_icon="🔤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS and set background
    load_css('style.css')
    set_background()
    
    # Main title with custom styling
    st.markdown("""
        <div class="title-container">
            <h1 class="title-text">🔄 Markov Chain Text Generator</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="subtitle">
        Generate creative text using advanced Markov Chain algorithms. Upload text, choose samples, 
        or enter your own content to create AI-generated variations.
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Generation Settings")
        
        # Advanced settings in an expander
        with st.expander("🛠️ Advanced Settings", expanded=True):
            order = st.slider(
                "Chain Order",
                min_value=1,
                max_value=5,
                value=2,
                help="Higher values create more coherent but less creative text"
            )
            
            length = st.slider(
                "Output Length",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                help="Number of words to generate"
            )
            
            creativity = st.slider(
                "Creativity Factor",
                min_value=0.1,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Higher values increase randomness"
            )
            
            preserve_case = st.checkbox(
                "Preserve Case",
                value=False,
                help="Maintain original text capitalization"
            )
    
    # Initialize generator with settings
    generator = MarkovChainGenerator(order=order, creativity=creativity)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Text Input",
        "📁 File Upload",
        "📊 Analysis",
        "💾 Save/Load Model"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter Your Text")
            
            # Sample text selector
            sample_texts = get_sample_texts()
            sample_option = st.selectbox(
                "Choose a sample text or enter your own:",
                ["Custom Input"] + list(sample_texts.keys())
            )
            
            # Text input area
            if sample_option == "Custom Input":
                text_input = st.text_area(
                    "Input Text",
                    height=200,
                    placeholder="Enter text here to build a Markov chain...",
                    key="custom_input"
                )
            else:
                text_input = st.text_area(
                    "Input Text",
                    value=sample_texts[sample_option],
                    height=200,
                    key="sample_input"
                )
        
        with col2:
            st.subheader("Generation Options")
            starting_words = st.text_input(
                "Starting Words (Optional)",
                placeholder="e.g., Once upon, The cat",
                help="Comma-separated words to start generation"
            )
            
            generate_button = st.button(
                "🚀 Generate Text",
                key="generate_text",
                use_container_width=True
            )
    
        # Generate and display text
        if generate_button and text_input:
            with st.spinner("Generating text..."):
                generator.build_chain(text_input, preserve_case=preserve_case)
                
                start_list = None
                if starting_words:
                    start_list = [word.strip() for word in starting_words.split(',')]
                
                generated_text = generator.generate_text(
                    length=length,
                    start_words=start_list
                )
                
                # Display generated text in a styled container
                st.markdown("""
                    <div class="generated-text-container fadeIn">
                    <h3>📝 Generated Text:</h3>
                    """, unsafe_allow_html=True)
                st.markdown(f"*{generated_text}*")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "⬇️ Download Text",
                        data=generated_text,
                        file_name="markov_generated_text.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        "💾 Save Model",
                        data=generator.export_model_json(),
                        file_name="markov_model.json",
                        mime="application/json",
                        use_container_width=True
                    )
    
    with tab2:
        st.subheader("Upload Text File")
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt'],
            help="Upload a .txt file to generate text from"
        )
        
        if uploaded_file is not None:
            file_text = uploaded_file.getvalue().decode("utf-8")
            
            # File preview with toggle
            with st.expander("📄 File Preview", expanded=False):
                st.text(file_text[:1000] + ("..." if len(file_text) > 1000 else ""))
            
            col1, col2 = st.columns(2)
            
            with col1:
                starting_words_file = st.text_input(
                    "Starting Words (Optional)",
                    placeholder="e.g., The cat, Once upon",
                    key="start_file"
                )
            
            with col2:
                generate_from_file = st.button(
                    "🚀 Generate from File",
                    key="generate_file",
                    use_container_width=True
                )
            
            if generate_from_file:
                with st.spinner("Generating from file..."):
                    generator.build_chain(file_text, preserve_case=preserve_case)
                    
                    start_list = None
                    if starting_words_file:
                        start_list = [word.strip() for word in starting_words_file.split(',')]
                    
                    generated_text = generator.generate_text(
                        length=length,
                        start_words=start_list
                    )
                    
                    st.markdown("""
                        <div class="generated-text-container fadeIn">
                        <h3>📝 Generated Text:</h3>
                        """, unsafe_allow_html=True)
                    st.markdown(f"*{generated_text}*")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Download options
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "⬇️ Download Text",
                            data=generated_text,
                            file_name=f"markov_generated_{uploaded_file.name}",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            "💾 Save Model",
                            data=generator.export_model_json(),
                            file_name=f"markov_model_{uploaded_file.name}.json",
                            mime="application/json",
                            use_container_width=True
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
            with st.spinner("Analyzing text..."):
                chain = generator.build_chain(text_for_analysis, preserve_case=preserve_case)
                
                # Create columns for metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Total States</div>
                        </div>
                        """.format(len(chain)), unsafe_allow_html=True)
                
                with col2:
                    vocabulary = generator.get_vocabulary()
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Vocabulary Size</div>
                        </div>
                        """.format(len(vocabulary)), unsafe_allow_html=True)
                
                with col3:
                    avg_transitions = sum(len(v) for v in chain.values()) / len(chain) if chain else 0
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">{:.2f}</div>
                            <div class="metric-label">Avg Transitions/State</div>
                        </div>
                        """.format(avg_transitions), unsafe_allow_html=True)
                
                # Transition analysis
                st.subheader("🔝 Top Transitions")
                transition_counts = generator.analyze_transitions()
                
                if transition_counts:
                    transitions_df = pd.DataFrame({
                        'From State': [k[0] for k in transition_counts.keys()],
                        'To State': [k[1] for k in transition_counts.keys()],
                        'Count': list(transition_counts.values())
                    }).sort_values('Count', ascending=False).head(10)
                    
                    # Create Sankey diagram
                    fig = go.Figure(data=[go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=20,
                            line=dict(color="black", width=0.5),
                            label=list(set(transitions_df['From State'].tolist() + 
                                         transitions_df['To State'].tolist())),
                            color="blue"
                        ),
                        link=dict(
                            source=[list(set(transitions_df['From State'].tolist() + 
                                          transitions_df['To State'].tolist())).index(x) 
                                  for x in transitions_df['From State']],
                            target=[list(set(transitions_df['From State'].tolist() + 
                                          transitions_df['To State'].tolist())).index(x) 
                                  for x in transitions_df['To State']],
                            value=transitions_df['Count'],
                            color="rgba(30, 136, 229, 0.4)"
                        )
                    )])
                    
                    fig.update_layout(title_text="Transition Flow Diagram", font_size=10)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(
                        transitions_df,
                        use_container_width=True,
                        hide_index=True
                    )
    
    with tab4:
        st.subheader("💾 Save/Load Model")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Save Current Model")
            if generator.markov_chain:
                st.download_button(
                    "💾 Save Model to File",
                    data=generator.export_model_json(),
                    file_name="markov_model.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("Generate text first to save a model")
        
        with col2:
            st.markdown("### Load Existing Model")
            model_file = st.file_uploader(
                "Upload a model file",
                type=['json'],
                key="model_upload"
            )
            
            if model_file is not None:
                if generator.load_model_json(model_file.getvalue().decode()):
                    st.success("Model loaded successfully!")
                else:
                    st.error("Error loading model")
    
    # Add footer
    create_footer()

if __name__ == "__main__":
    main()

