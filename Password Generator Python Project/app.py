import streamlit as st
import random
import string
import secrets
import pyperclip
from typing import List, Dict, Any, Optional
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import time
import json
import os
from datetime import datetime
import requests

class PasswordGenerator:
    """A secure password generator with multiple configuration options."""

    def __init__(self):
        self.complexity_levels = {
            'low': string.ascii_letters + string.digits,
            'medium': string.ascii_letters + string.digits + string.punctuation[:10],
            'high': string.ascii_letters + string.digits + string.punctuation,
            'pin': string.digits,
            'memorable': string.ascii_letters + string.digits + '!@#$%^&*()',
            'custom': ''  # Will be populated based on user selections
        }

        self.password_history = []
        self.history_file = "password_history.json"
        self.load_history()

        # Dictionary of common words for memorable passwords
        self.common_words = [
            "apple", "banana", "carrot", "diamond", "elephant",
            "forest", "guitar", "harvest", "island", "journey",
            "kitchen", "lemon", "mountain", "notebook", "ocean",
            "penguin", "quantum", "rainbow", "sunset", "tiger",
            "umbrella", "volcano", "waterfall", "xylophone", "zeppelin",
            "adventure", "butterfly", "chocolate", "dolphin", "emerald",
            "firefly", "giraffe", "horizon", "igloo", "jasmine",
            "kangaroo", "lighthouse", "moonlight", "nightingale", "orchestra"
        ]

        # Presets for quick password generation
        self.presets = {
            "Standard": {"length": 12, "complexity": "medium"},
            "Extra Strong": {"length": 16, "complexity": "high"},
            "Easy to Remember": {"length": 3, "complexity": "memorable"},
            "PIN Code": {"length": 6, "complexity": "pin"},
            "WiFi Password": {"length": 14, "complexity": "high"}
        }

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
        fig, ax = plt.subplots(figsize=(4, 3))

        # Plot horizontal bar chart
        categories = ['Length', 'Uppercase', 'Lowercase', 'Digits', 'Special']
        values = [
            min(1.0, metrics["length"] / 16),  # Normalize length to max 1.0
            1.0 if metrics["has_upper"] else 0.0,
            1.0 if metrics["has_lower"] else 0.0,
            1.0 if metrics["has_digit"] else 0.0,
            1.0 if metrics["has_special"] else 0.0
        ]

        # Use a gradient color scheme based on strength
        colors = []
        for v in values:
            if v < 0.3:
                colors.append('#FF6B6B')  # Red for weak
            elif v < 0.7:
                colors.append('#FFD166')  # Yellow for medium
            else:
                colors.append('#06D6A0')  # Green for strong

        ax.barh(categories, values, color=colors)
        ax.set_xlim(0, 1)
        ax.set_title(f"Password Strength: {strength_data['label']}")

        # Add percentage labels
        for i, v in enumerate(values):
            ax.text(max(0.05, v - 0.2), i, f"{int(v * 100)}%", va='center', color='white', fontweight='bold')

        # Convert plot to image
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png", dpi=100, transparent=True)
        plt.close(fig)

        return buf

    def save_to_history(self, password: str, metadata: Dict[str, Any] = None) -> None:
        """Save a password to history with timestamp and metadata"""
        if not metadata:
            metadata = {}

        entry = {
            "password": password,
            "timestamp": datetime.now().isoformat(),
            "strength": self.get_strength(password)["label"],
            "metadata": metadata
        }

        self.password_history.append(entry)
        self._save_history()

    def _save_history(self) -> None:
        """Save password history to file"""
        # Keep only the last 20 passwords
        if len(self.password_history) > 20:
            self.password_history = self.password_history[-20:]

        try:
            with open(self.history_file, 'w') as f:
                # Save only masked passwords for security
                masked_history = []
                for entry in self.password_history:
                    masked_entry = entry.copy()
                    if len(entry["password"]) > 4:
                        masked_entry["password"] = entry["password"][:2] + '*' * (len(entry["password"]) - 4) + entry["password"][-2:]
                    else:
                        masked_entry["password"] = '*' * len(entry["password"])
                    masked_history.append(masked_entry)

                json.dump(masked_history, f, indent=2)
        except Exception as e:
            # Silently fail if we can't save history
            pass

    def load_history(self) -> None:
        """Load password history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.password_history = json.load(f)
        except Exception as e:
            # If there's an error, start with empty history
            self.password_history = []

    def clear_history(self) -> None:
        """Clear password history"""
        self.password_history = []
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)
            except:
                pass

    def check_password_vulnerability(self, password: str) -> Dict[str, Any]:
        """Check if a password has been exposed in data breaches using k-anonymity"""
        # Use the first 5 characters of the SHA-1 hash to query the API
        import hashlib

        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]

        try:
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            if response.status_code == 200:
                hashes = (line.split(':') for line in response.text.splitlines())
                for h, count in hashes:
                    if h == suffix:
                        return {
                            "vulnerable": True,
                            "breach_count": int(count),
                            "message": f"This password has been exposed in {count} data breaches!"
                        }
                return {"vulnerable": False, "message": "Password not found in known data breaches."}
            else:
                return {"vulnerable": False, "message": "Could not check password vulnerability."}
        except Exception as e:
            return {"vulnerable": False, "message": "Could not check password vulnerability."}

    def export_passwords(self, format_type: str = "text") -> BytesIO:
        """Export password history to a file"""
        buf = BytesIO()

        if format_type == "text":
            content = "Secure Password Generator - Password Export\n"
            content += "=" * 50 + "\n\n"

            for entry in self.password_history:
                content += f"Password: {entry['password']}\n"
                content += f"Generated: {entry['timestamp']}\n"
                content += f"Strength: {entry['strength']}\n"
                content += "-" * 30 + "\n"

            buf.write(content.encode('utf-8'))

        elif format_type == "json":
            json.dump(self.password_history, buf, indent=2)

        buf.seek(0)
        return buf

def set_background():
    """Set a custom background for the app"""
    # Define custom CSS with a gradient background
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            color: white;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            font-weight: bold;
        }

        div[data-testid="stCodeBlock"] {
            border-radius: 8px;
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        div.stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s ease;
        }

        div.stButton > button:hover {
            background-color: #3e8e41;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
        }

        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3 {
            color: white;
        }

        .password-display {
            font-family: 'Courier New', monospace;
            font-size: 24px;
            padding: 15px;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            text-align: center;
            letter-spacing: 2px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .card {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def generate_password_list():
    """Generate passwords based on Streamlit inputs and display them"""
    generator = PasswordGenerator()

    st.subheader("Generate Secure Passwords")
    st.write("Customize your password settings below")

    # Add preset selection at the top
    preset_selected = st.selectbox(
        "Quick Presets",
        list(generator.presets.keys()) + ["Custom Settings"],
        index=len(generator.presets),
        help="Choose a preset or customize your own settings"
    )

    # Create a container with a border
    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Use preset or custom settings
    if preset_selected != "Custom Settings":
        preset = generator.presets[preset_selected]
        complexity = preset["complexity"]

        if complexity == "memorable":
            length = preset["length"]  # Number of words for memorable
            exclude_chars = ""
        else:
            length = preset["length"]
            exclude_chars = ""

        # Show the preset settings but make them non-interactive
        with col1:
            st.write(f"**Complexity:** {complexity.capitalize()}")
            if complexity == "memorable":
                st.write(f"**Number of Words:** {length}")
            else:
                st.write(f"**Password Length:** {length}")
    else:
        # Custom settings
        with col1:
            complexity = st.selectbox(
                "Password Complexity",
                ["low", "medium", "high", "pin", "memorable", "custom"],
                index=2,
                help="Choose password complexity level"
            )

            # Conditional inputs based on complexity
            if complexity == "memorable":
                num_words = st.slider("Number of Words", 2, 5, 3)
                length = num_words
                exclude_chars = ""
            elif complexity == "custom":
                length = st.slider("Password Length", 8, 64, 16)

                # Custom character set options
                st.write("Include character types:")
                include_lower = st.checkbox("Lowercase (a-z)", value=True)
                include_upper = st.checkbox("Uppercase (A-Z)", value=True)
                include_digits = st.checkbox("Digits (0-9)", value=True)
                include_special = st.checkbox("Special Characters", value=True)

                # Build custom character set
                custom_charset = ""
                if include_lower:
                    custom_charset += string.ascii_lowercase
                if include_upper:
                    custom_charset += string.ascii_uppercase
                if include_digits:
                    custom_charset += string.digits
                if include_special:
                    custom_charset += string.punctuation

                # Update the custom complexity level
                generator.complexity_levels['custom'] = custom_charset
                exclude_chars = st.text_input("Characters to Exclude", "")
            else:
                length = st.slider(
                    "Password Length",
                    min_value=4 if complexity != "pin" else 4,
                    max_value=64,
                    value=12 if complexity != "pin" else 6
                )

                exclude_chars = st.text_input("Characters to Exclude", "")

    with col2:
        # Show complexity info
        if complexity == "custom":
            st.info("""
            **Custom Complexity**

            Create a password with exactly the character types you want.
            Make sure to select at least one character type.
            """)
        elif complexity == "memorable":
            st.info("""
            **Memorable Passwords**

            These passwords use common words combined with numbers and symbols,
            making them easier to remember but still secure.
            """)
        else:
            st.info(f"""
            **Complexity Level: {complexity.capitalize()}**

            - Low: Letters and numbers
            - Medium: Letters, numbers, and some symbols
            - High: Letters, numbers, and all symbols
            - PIN: Numbers only
            """)

        # Add number of passwords to generate
        num_passwords = st.number_input("Number of Passwords", min_value=1, max_value=10, value=1)

        # Generate button with animation
        generate_button = st.button("🔐 Generate Password", use_container_width=True)

    # Close the card container
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

    # Generate passwords when button is clicked
    if generate_button or preset_selected != "Custom Settings":
        try:
            with st.spinner("Generating secure passwords..."):
                if complexity == "memorable":
                    passwords = generator.generate_multiple(
                        count=num_passwords if 'num_passwords' in locals() else 1,
                        length=length,
                        complexity=complexity
                    )
                else:
                    passwords = generator.generate_multiple(
                        count=num_passwords if 'num_passwords' in locals() else 1,
                        length=length,
                        complexity=complexity,
                        exclude_chars=exclude_chars
                    )

                # Save to history with metadata
                for password in passwords:
                    generator.save_to_history(password, {
                        "complexity": complexity,
                        "length": length
                    })

                # Success message with animation
                st.success("✅ Password generated successfully!")
        except ValueError as e:
            st.error(f"Error: {e}")
            return
    else:
        # If no button click yet, show placeholder or return
        if 'passwords' not in st.session_state:
            return
        passwords = st.session_state.passwords

    # Display generated password(s)
    if 'passwords' in locals():
        st.subheader("Your Generated Passwords")
        st.write("Copy, analyze, or export your passwords")

        for i, password in enumerate(passwords):
            strength_info = generator.get_strength(password)
            vulnerability_info = generator.check_password_vulnerability(password)

            # Create a card-like container for each password
            st.markdown(f"""
            <div class="card">
            """, unsafe_allow_html=True)

            # Password display with styling
            st.markdown(f"""
            <div class="password-display">
                {password}
            </div>
            """, unsafe_allow_html=True)

            # Strength meter visualization
            score = strength_info["score"]
            max_score = 7  # Maximum possible score
            percentage = (score / max_score) * 100

            # Determine color based on strength
            if percentage < 40:
                color = "#FF6B6B"  # Red for weak
                emoji = "⚠️"
            elif percentage < 70:
                color = "#FFD166"  # Yellow for medium
                emoji = "🔔"
            else:
                color = "#06D6A0"  # Green for strong
                emoji = "✅"

            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="flex-grow: 1; margin-right: 10px;">
                    <div style="height: 8px; border-radius: 4px; background-color: #333;">
                        <div style="width: {percentage}%; height: 100%; border-radius: 4px; background-color: {color};"></div>
                    </div>
                </div>
                <div>{emoji} {strength_info['label']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons in a row
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📋 Copy", key=f"copy_{i}_{password}", use_container_width=True):
                    pyperclip.copy(password)
                    st.success("Password copied to clipboard!")

            with col2:
                if st.button("🔍 Analyze", key=f"analyze_{i}", use_container_width=True):
                    st.session_state.password_to_analyze = password
                    st.experimental_rerun()

            with col3:
                if vulnerability_info["vulnerable"]:
                    st.error(f"⚠️ {vulnerability_info['message']}")
                else:
                    st.success("✅ Not found in data breaches")

            # Expandable details section
            with st.expander("Password Details"):
                detail_col1, detail_col2 = st.columns([3, 2])

                with detail_col1:
                    st.write("**Password Properties:**")
                    metrics = strength_info["metrics"]

                    st.markdown(f"""
                    - **Length:** {metrics['length']} characters
                    - **Uppercase:** {'Yes' if metrics['has_upper'] else 'No'}
                    - **Lowercase:** {'Yes' if metrics['has_lower'] else 'No'}
                    - **Digits:** {'Yes' if metrics['has_digit'] else 'No'}
                    - **Special Characters:** {'Yes' if metrics['has_special'] else 'No'}
                    - **Entropy:** ~{strength_info['entropy']} bits
                    """)

                with detail_col2:
                    # Display strength visualization using the function
                    strength_buf = generator.create_strength_chart(password)
                    strength_buf.seek(0)
                    st.image(strength_buf, use_container_width=True)

            # Close the card container
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)

        # Export options
        with st.expander("Export Passwords"):
            export_col1, export_col2 = st.columns(2)

            with export_col1:
                export_format = st.radio("Export Format", ["Text File", "JSON"])

            with export_col2:
                if st.button("📥 Export Passwords", use_container_width=True):
                    format_type = "text" if export_format == "Text File" else "json"
                    export_buf = generator.export_passwords(format_type)

                    file_extension = "txt" if format_type == "text" else "json"
                    filename = f"passwords_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"

                    st.download_button(
                        label="Download File",
                        data=export_buf,
                        file_name=filename,
                        mime=f"text/{file_extension}",
                        use_container_width=True
                    )



def main():
    # Set page config
    st.set_page_config(
        page_title="Secure Password Generator",
        page_icon="🔒",
        layout="wide",
    )

    # Apply custom background and styling
    set_background()

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
        st.header("Generate Passwords")
        generate_password_list()

    with tab2:
        st.header("Check Your Password Strength")
        password_to_check = st.text_input("Enter a password to check", type="password")

        if password_to_check:
            generator = PasswordGenerator()
            strength_info = generator.get_strength(password_to_check)
            vulnerability_info = generator.check_password_vulnerability(password_to_check)

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

            # Vulnerability check
            st.subheader("Data Breach Check")
            if vulnerability_info["vulnerable"]:
                st.error(f"⚠️ {vulnerability_info['message']}")
            else:
                st.success(f"✅ {vulnerability_info['message']}")

    with tab3:
        st.header("About This App")

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
            - Data breach vulnerability checking
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