#!/usr/bin/env python3
import random
import string
import secrets
import argparse
from typing import List

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

    def get_strength(self, password: str) -> str:
        """Estimate password strength."""
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        score = 0
        if length >= 16: score += 3
        elif length >= 12: score += 2
        elif length >= 8: score += 1
        
        score += has_upper + has_lower + has_digit + has_special
        
        if score >= 6: return "Very Strong"
        if score >= 5: return "Strong"
        if score >= 3: return "Moderate"
        return "Weak"

    def interactive_mode(self):
        """Run in interactive command-line mode."""
        print("\n" + "=" * 50)
        print(" 🔒 SECURE PASSWORD GENERATOR 🔒 ".center(50))
        print("=" * 50)
        
        while True:
            try:
                print("\nOptions:")
                print("1. Generate single password")
                print("2. Generate multiple passwords")
                print("3. View password history")
                print("4. Exit")
                
                choice = input("\nEnter your choice (1-4): ")
                
                if choice == '1':
                    self._generate_single_password()
                elif choice == '2':
                    self._generate_multiple_passwords()
                elif choice == '3':
                    self._show_history()
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
            except Exception as e:
                print(f"Error: {e}")

    def _generate_single_password(self):
        """Handle single password generation in interactive mode."""
        print("\nPassword Settings:")
        complexity = input("Complexity (low, medium, high, pin, memorable) [high]: ").lower() or 'high'
        
        if complexity == 'memorable':
            num_words = int(input("Number of words (2-5) [3]: ") or 3)
            password = self.generate_password(num_words, complexity)
        else:
            length = int(input("Length [12]: ") or 12)
            exclude = input("Characters to exclude [none]: ")
            password = self.generate_password(length, complexity, exclude)
            
        strength = self.get_strength(password)
        
        print("\n" + "-" * 40)
        print(f"Generated Password: {password}")
        print(f"Strength: {strength}")
        print("-" * 40)

    def _generate_multiple_passwords(self):
        """Handle multiple password generation in interactive mode."""
        count = int(input("\nNumber of passwords to generate [5]: ") or 5)
        complexity = input("Complexity (low, medium, high, pin, memorable) [high]: ").lower() or 'high'
        
        if complexity == 'memorable':
            num_words = int(input("Number of words (2-5) [3]: ") or 3)
            passwords = self.generate_multiple(count, length=num_words, complexity=complexity)
        else:
            length = int(input("Length [12]: ") or 12)
            exclude = input("Characters to exclude [none]: ")
            passwords = self.generate_multiple(count, length=length, complexity=complexity, exclude_chars=exclude)
        
        print("\n" + "=" * 40)
        print(" 🔑 GENERATED PASSWORDS 🔑 ".center(40))
        print("=" * 40)
        
        for i, pwd in enumerate(passwords, 1):
            strength = self.get_strength(pwd)
            print(f"{i}. {pwd} ({strength})")
        
        print("=" * 40)

    def _show_history(self):
        """Display password generation history."""
        if not self.password_history:
            print("\n❌ No passwords generated yet!")
            return
            
        print("\n" + "=" * 40)
        print(" 📜 PASSWORD HISTORY 📜 ".center(40))
        print("=" * 40)
        
        for i, pwd in enumerate(self.password_history[-10:], 1):  # Show last 10
            strength = self.get_strength(pwd)
            print(f"{i}. {pwd} ({strength})")
        
        print("=" * 40)

def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="🔒 Generate secure passwords with various options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate a single strong password:
    python cli.py
    
  Generate a 16-character password:
    python cli.py -l 16
    
  Generate 5 medium-complexity passwords:
    python cli.py -n 5 -c medium
    
  Generate a PIN:
    python cli.py -c pin -l 6
    
  Generate a memorable password:
    python cli.py -c memorable
        """
    )
    
    parser.add_argument('-n', '--number', type=int, default=1, help="Number of passwords to generate")
    parser.add_argument('-l', '--length', type=int, default=12, help="Password length (or number of words for memorable)")
    parser.add_argument('-c', '--complexity', default='high', 
                       choices=['low', 'medium', 'high', 'pin', 'memorable'],
                       help="Password complexity level")
    parser.add_argument('-e', '--exclude', default='', help="Characters to exclude")
    parser.add_argument('-i', '--interactive', action='store_true', help="Run in interactive mode")
    
    args = parser.parse_args()
    generator = PasswordGenerator()
    
    if args.interactive:
        generator.interactive_mode()
    else:
        try:
            passwords = generator.generate_multiple(
                count=args.number,
                length=args.length,
                complexity=args.complexity,
                exclude_chars=args.exclude
            )
            
            print("\n🔐 Generated Passwords:")
            for pwd in passwords:
                strength = generator.get_strength(pwd)
                print(f"  {pwd} ({strength})")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            parser.print_help()

if __name__ == "__main__":
    main()