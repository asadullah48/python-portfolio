import os
import subprocess
import sys

def main():
    """
    Run the enhanced Minesweeper game using Streamlit.
    """
    print("Starting Enhanced Minesweeper...")
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("Streamlit is installed.")
    except ImportError:
        print("Streamlit is not installed. Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully.")
    
    # Run the Streamlit app
    os.system(f"{sys.executable} -m streamlit run enhanced_minesweeper.py")

if __name__ == "__main__":
    main()
