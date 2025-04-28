"""
Utility functions for the Markov Chain Text Generator application.
"""

import re
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import importlib.util

# Check for optional dependencies without showing errors yet
seaborn_spec = importlib.util.find_spec("seaborn")
SEABORN_AVAILABLE = seaborn_spec is not None

nltk_spec = importlib.util.find_spec("nltk")
NLTK_AVAILABLE = nltk_spec is not None

# We'll import these conditionally after st.set_page_config in main.py
if SEABORN_AVAILABLE:
    import seaborn as sns

if NLTK_AVAILABLE:
    import nltk
    from nltk.tokenize import sent_tokenize

from collections import Counter
import json
import os
import base64
from datetime import datetime

# Download NLTK data if NLTK is available
if NLTK_AVAILABLE:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except Exception as e:
            st.warning(f"Could not download NLTK data: {str(e)}")

def get_base64_encoded_image(image_path):
    """
    Get the base64 encoded string of an image for embedding in HTML/CSS.

    Args:
        image_path (str): Path to the image file

    Returns:
        str: Base64 encoded string
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background(image_path=None):
    """
    Set the background image for the Streamlit app.

    Args:
        image_path (str, optional): Path to the image file. If None, uses a gradient.
    """
    if image_path and os.path.exists(image_path):
        encoded_image = get_base64_encoded_image(image_path)
        background_image_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
    else:
        # Use a gradient background if no image is provided
        background_image_style = """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        </style>
        """

    st.markdown(background_image_style, unsafe_allow_html=True)

def load_css(css_file):
    """
    Load and apply custom CSS.

    Args:
        css_file (str): Path to the CSS file
    """
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def analyze_text(text):
    """
    Analyze text and return statistics.

    Args:
        text (str): Text to analyze

    Returns:
        dict: Text statistics
    """
    # Clean and prepare text
    words = re.findall(r'\b\w+\b', text.lower())

    # Calculate word statistics
    word_count = len(words)
    unique_words = len(set(words))

    # Word frequency
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)

    # Basic stats that don't require NLTK
    result = {
        "word_count": word_count,
        "unique_words": unique_words,
        "vocabulary_richness": unique_words / max(1, word_count),
        "most_common_words": most_common_words,
    }

    # Add sentence analysis if NLTK is available
    if NLTK_AVAILABLE:
        sentences = sent_tokenize(text)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / max(1, sentence_count)
        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]

        result.update({
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "sentence_lengths": sentence_lengths
        })
    else:
        # Simple sentence splitting as fallback
        sentences = text.split('.')
        sentence_count = len([s for s in sentences if s.strip()])
        result.update({
            "sentence_count": sentence_count,
            "avg_sentence_length": word_count / max(1, sentence_count),
            "sentence_lengths": []  # Empty list as we can't reliably calculate without NLTK
        })

    return result

def plot_word_frequency(word_freq, title="Word Frequency"):
    """
    Create a bar chart of word frequencies.

    Args:
        word_freq (list): List of (word, count) tuples
        title (str): Chart title

    Returns:
        matplotlib.figure.Figure: The figure object
    """
    words, counts = zip(*word_freq)

    fig, ax = plt.subplots(figsize=(10, 6))

    if SEABORN_AVAILABLE:
        sns.barplot(x=list(counts), y=list(words), palette="viridis", ax=ax)
    else:
        # Fallback to matplotlib
        ax.barh(range(len(words)), counts)
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)

    ax.set_title(title)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Words")

    return fig

def plot_sentence_length_distribution(sentence_lengths):
    """
    Create a histogram of sentence lengths.

    Args:
        sentence_lengths (list): List of sentence lengths

    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if SEABORN_AVAILABLE:
        sns.histplot(sentence_lengths, bins=20, kde=True, ax=ax)
    else:
        # Fallback to matplotlib
        ax.hist(sentence_lengths, bins=20)

    ax.set_title("Sentence Length Distribution")
    ax.set_xlabel("Sentence Length (words)")
    ax.set_ylabel("Frequency")

    return fig

def save_markov_model(chain, filename):
    """
    Save a Markov chain model to a JSON file.

    Args:
        chain (dict): The Markov chain dictionary
        filename (str): Filename to save to

    Returns:
        bool: Success status
    """
    try:
        # Convert tuple keys to strings for JSON serialization
        serializable_chain = {}
        for key, value in chain.items():
            serializable_chain[str(key)] = value

        with open(filename, 'w') as f:
            json.dump(serializable_chain, f)
        return True
    except Exception as e:
        st.error(f"Error saving model: {str(e)}")
        return False

def load_markov_model(filename):
    """
    Load a Markov chain model from a JSON file.

    Args:
        filename (str): Filename to load from

    Returns:
        dict: The loaded Markov chain or None if error
    """
    try:
        with open(filename, 'r') as f:
            serialized_chain = json.load(f)

        # Convert string keys back to tuples
        chain = {}
        for key_str, value in serialized_chain.items():
            # Extract words from the string representation of the tuple
            key_parts = re.findall(r"'([^']*)'", key_str)
            if key_parts:
                chain[tuple(key_parts)] = value

        return chain
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def get_sample_texts():
    """
    Get a dictionary of sample texts for the application.

    Returns:
        dict: Dictionary of sample texts
    """
    return {
        "Lorem Ipsum": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "Shakespeare": "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles And by opposing end them. To die—to sleep, No more; and by a sleep to say we end The heart-ache and the thousand natural shocks That flesh is heir to: 'tis a consummation Devoutly to be wish'd.",
        "Programming Concepts": "Python is a high-level, interpreted programming language. It is known for its readability and simplicity. Functions are first-class objects in Python, which means they can be assigned to variables, passed as arguments, and returned from other functions. Object-oriented programming is supported through classes and inheritance. Python's standard library provides many modules for common tasks.",
        "Sci-Fi": "In the year 2150, humanity had finally achieved interstellar travel. The first colony ships departed Earth for the Alpha Centauri system, carrying thousands of hopeful settlers. The journey would take decades, even with the new quantum drive technology. Meanwhile, on Earth, artificial intelligence had evolved to a point where robots were indistinguishable from humans in both appearance and cognition.",
        "Fantasy": "The ancient dragon soared above the misty mountains, its scales gleaming like rubies in the morning sun. Below, the small village prepared for the annual harvest festival, unaware of the dark forces gathering in the enchanted forest. The wizard Thorne consulted his crystal orb, sensing a disturbance in the magical fields that protected the realm from the shadow dimension.",
        "News Style": "Scientists announced a breakthrough in renewable energy technology yesterday. The new solar panels can generate electricity even on cloudy days, potentially revolutionizing the industry. Meanwhile, global leaders gathered at the summit to discuss climate change initiatives. In other news, the local community has started a program to reduce plastic waste in oceans."
    }

def create_footer():
    """Create a professional footer for the application."""
    footer_html = """
    <footer>
        <p>Markov Chain Text Generator © 2025 | Created with Streamlit</p>
        <p>A sophisticated text generation tool using Markov Chain algorithms</p>
    </footer>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
