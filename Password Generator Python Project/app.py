import streamlit as st
import random
import string
import secrets
import pyperclip
from typing import List
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import time

class PasswordGenerator:
    """A secure password generator with multiple configuration options."""
    
    def __init__(self):
        self.complexity_levels = {
            'low': string.ascii_letters + string.digits,
            'medium': string.ascii_letters + string.digits + string.punctuation[:10],
            'high': string.ascii_letters + string.digits + string.punctuation,
            'pin': string.digits,
            'memorable': string.ascii_letters + string.digits + '!@#$%^&*()'
        }
        
        self.password_history = []
        
        # Dictionary of common words for memorable passwords
        self.common_words = [
            "apple", "banana", "carrot", "diamond", "elephant", 
            "forest", "guitar", "harvest", "island", "journey",
            "kitchen", "lemon", "mountain", "notebook", "ocean",
            "penguin", "quantum", "rainbow", "sunset", "tiger",
            "umbrella", "volcano", "waterfall", "xylophone", "zeppelin"
        ]

    def generate_password(self, length: int = 12, complexity: str = 'high', exclude_chars: str = '') -> str:
        """
        Generate a secure password with specified parameters.
        
        Args:
            length: Length of the password (default: 12)
            complexity: Complexity level ('low', 'medium', 'high', 'pin', 'memorable') (default: 'high')
            exclude_chars: Characters to exclude from generation
            
        Returns:
            Generated password string
        """
        if complexity not in self.complexity_levels:
            raise ValueError(f"Invalid complexity level. Choose from {list(self.complexity_levels.keys())}")
        
        if length < 4 and complexity != 'memorable':
            raise ValueError("Password length must be at least 4 characters")
        
        # Special handling for memorable passwords
        if complexity == 'memorable':
            return self._generate_memorable_password(length)
            
        charset = self.complexity_levels[complexity]
        charset = ''.join(c for c in charset if c not in exclude_chars)
        
        if not charset:
            raise ValueError("No characters available after exclusions")
            
        # Ensure at least one character from each required character class
        password = []
        if complexity != 'pin':
            password.append(secrets.choice(string.ascii_lowercase))
            password.append(secrets.choice(string.ascii_uppercase))
            password.append(secrets.choice(string.digits))
            if complexity in ('medium', 'high', 'memorable'):
                special_chars = [c for c in string.punctuation if c not in exclude_chars]
                if special_chars:
                    password.append(secrets.choice(special_chars))
        
        # Fill the rest with random choices
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(secrets.choice(charset) for _ in range(remaining_length))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        generated = ''.join(password)
        self.password_history.append(generated)
        return generated

    def _generate_memorable_password(self, num_words: int = 3) -> str:
        """Generate a memorable password using words and separators."""
        separators = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=']
        words = random.sample(self.common_words, num_words)
        
        # Capitalize randomly and add numbers
        for i in range(len(words)):
            if random.choice([True, False]):
                words[i] = words[i].capitalize()
            
        # Add separators between words
        separator = random.choice(separators)
        password = separator.join(words)
        
        # Add a random number at the end
        password += str(random.randint(10, 99))
        
        self.password_history.append(password)
        return password

    def generate_multiple(self, count: int = 1, **kwargs) -> List[str]:
        """Generate multiple passwords with the same parameters."""
        return [self.generate_password(**kwargs) for _ in range(count)]

    def get_strength(self, password: str) -> dict:
        """
        Estimate password strength with detailed metrics.
        
        Returns a dictionary with:
        - score: Overall strength score
        - label: Text label of strength
        - entropy: Estimated entropy in bits
        - metrics: Dictionary of individual metrics
        """
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        # Base score
        score = 0
        if length >= 16: score += 3
        elif length >= 12: score += 2
        elif length >= 8: score += 1
        
        # Character diversity score
        char_diversity = has_upper + has_lower + has_digit + has_special
        score += char_diversity
        
        # Calculate entropy (rough estimation)
        charset_size = 0
        if has_lower: charset_size += 26
        if has_upper: charset_size += 26
        if has_digit: charset_size += 10
        if has_special: charset_size += 32
        
        entropy = length * (charset_size.bit_length() if charset_size > 0 else 0)
        
        # Determine strength label
        if score >= 6: label = "Very Strong"
        elif score >= 5: label = "Strong"
        elif score >= 3: label = "Moderate"
        else: label = "Weak"
        
        return {
            "score": score,
            "label": label,
            "entropy": entropy,
            "metrics": {
                "length": length,
                "has_upper": has_upper,
                "has_lower": has_lower,
                "has_digit": has_digit,
                "has_special": has_special,
                "char_diversity": char_diversity
            }
        }
        
    def create_strength_chart(self, password):
        """Create a visual representation of password strength"""
        strength_data = self.get_strength(password)
        metrics = strength_data["metrics"]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(4, 2.5))
        
        # Plot horizontal bar chart
        categories = ['Length', 'Uppercase', 'Lowercase', 'Digits', 'Special']
        values = [
            min(1.0, metrics["length"] / 12),  # Normalize length to max 1.0
            1.0 if metrics["has_upper"] else 0.0,
            1.0 if metrics["has_lower"] else 0.0,
            1.0 if metrics["has_digit"] else 0.0,
            1.0 if metrics["has_special"] else 0.0
        ]
        
        colors = ['#FF9999' if v < 0.5 else '#99CC99' for v in values]
        
        ax.barh(categories, values, color=colors)
        ax.set_xlim(0, 1)
        ax.set_title(f"Password Strength: {strength_data['label']}")
        
        # Convert plot to image
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        
        return buf

def generate_password_list():
    """Generate passwords based on Streamlit inputs and display them"""
    generator = PasswordGenerator()
    
    st.subheader("Generate Passwords")
    
    col1, col2 = st.columns(2)
    
    with col1:
        complexity = st.selectbox(
            "Password Complexity",
            ["low", "medium", "high", "pin", "memorable"],
            index=2,
            help="Choose password complexity level"
        )
        
        # Conditional inputs based on complexity
        if complexity == "memorable":
            num_words = st.slider("Number of Words", 2, 5, 3)
            exclude_chars = ""
            passwords = generator.generate_multiple(
                count=1,
                length=num_words,
                complexity=complexity
            )
        else:
            length = st.slider(
                "Password Length", 
                min_value=4 if complexity != "pin" else 4,
                max_value=32, 
                value=12 if complexity != "pin" else 6
            )
            
            exclude_chars = st.text_input("Characters to Exclude", "")
            
            try:
                passwords = generator.generate_multiple(
                    count=1,
                    length=length,
                    complexity=complexity,
                    exclude_chars=exclude_chars
                )
            except ValueError as e:
                st.error(f"Error: {e}")
                return
    
    with col2:
        if complexity != "memorable":
            st.info(f"""
            **Complexity Level: {complexity.capitalize()}**
            
            - Low: Letters and numbers
            - Medium: Letters, numbers, and some symbols
            - High: Letters, numbers, and all symbols
            - PIN: Numbers only
            - Memorable: Word-based passwords
            """)
        else:
            st.info("""
            **Memorable Passwords**
            
            These passwords use common words combined with numbers and symbols,
            making them easier to remember but still secure.
            """)
    
    st.subheader("Your Password")
    
    # Display generated password(s)
    for password in passwords:
        strength_info = generator.get_strength(password)
        
        # Create columns for password details
        pwd_col1, pwd_col2 = st.columns([3, 1])
        
        with pwd_col1:
            st.code(password, language="text")
            
            # Copy button
            if st.button("📋 Copy to Clipboard", key=f"copy_{password}"):
                pyperclip.copy(password)
                st.success("Password copied to clipboard!")
                
            # Display strength metrics
            st.caption(f"Strength: {strength_info['label']} | Entropy: ~{strength_info['entropy']} bits")
        
        with pwd_col2:
            # Display strength visualization using the function
            strength_buf = generator.create_strength_chart(password)
            strength_buf.seek(0)
            st.image(strength_buf, use_container_width=True)

def main():
    st.set_page_config(
        page_title="Secure Password Generator",
        page_icon="🔒",
        layout="wide",
    )
    
    # Display logo and title in a row
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.image("https://www.creative-tim.com/gpts/logos/password-generator.png", width=100)
        
    with col2:
        st.title("Secure Password Generator")
        st.caption("Generate strong, secure passwords for all your accounts")
    
    # Add tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Generate Passwords", "Password Strength Checker", "About"])
    
    with tab1:
        generate_password_list()
    
    with tab2:
        st.subheader("Check Your Password Strength")
        password_to_check = st.text_input("Enter a password to check", type="password")
        
        if password_to_check:
            generator = PasswordGenerator()
            strength_info = generator.get_strength(password_to_check)
            
            st.write(f"**Strength:** {strength_info['label']}")
            st.write(f"**Entropy:** ~{strength_info['entropy']} bits")
            
            # Display metrics
            st.write("**Password Properties:**")
            metrics = strength_info["metrics"]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Length", metrics["length"])
            col2.metric("Uppercase", "Yes" if metrics["has_upper"] else "No")
            col3.metric("Lowercase", "Yes" if metrics["has_lower"] else "No")
            col4.metric("Special Chars", "Yes" if metrics["has_special"] else "No")
            
            # Show strength visualization
            st.subheader("Strength Analysis")
            strength_buf = generator.create_strength_chart(password_to_check)
            strength_buf.seek(0)
            st.image(strength_buf, use_container_width=True)

    with tab3:
        st.subheader("About This App")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://www.creative-tim.com/gpts/logos/password-generator.png", width=150)
            
        with col2:
            st.write("""
            This Password Generator creates strong, secure passwords to help protect your online accounts. 
            
            ### Features:
            - Multiple complexity levels
            - Memorable password option
            - Password strength analysis
            - Copy to clipboard functionality
            
            ### Security Tips:
            - Use a different password for each account
            - Enable two-factor authentication when available
            - Consider using a password manager
            """)
        
        st.write("""
        ### Developer
        Created by [Asadullah](https://github.com/asadullah48)
        
        [View Source Code on GitHub](https://github.com/asadullah48/secure-password-generator)
        """)

if __name__ == "__main__":
    main()