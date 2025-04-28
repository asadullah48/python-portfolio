"""
Dependency installer for Markov Chain Text Generator
This script checks and installs all required dependencies
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using pip"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
        return True
    except Exception as e:
        print(f"Error installing {package_name}: {str(e)}")
        return False

def main():
    """Main function to install all dependencies"""
    print("Checking and installing dependencies for Markov Chain Text Generator...")
    
    # List of required packages
    required_packages = [
        "streamlit>=1.0.0",
        "pandas>=1.0.0",
        "matplotlib>=3.0.0",
        "seaborn>=0.11.0",
        "nltk>=3.6.0",
        "plotly>=5.0.0",
        "scikit-learn>=1.0.0",
        "pillow>=9.0.0"
    ]
    
    # Install each package
    success = True
    for package in required_packages:
        if not install_package(package):
            success = False
    
    if success:
        print("\nAll dependencies installed successfully!")
        print("You can now run the application with: streamlit run main.py")
    else:
        print("\nSome dependencies could not be installed.")
        print("The application may still run with limited functionality.")
        print("Try running: streamlit run main.py")

if __name__ == "__main__":
    main()
