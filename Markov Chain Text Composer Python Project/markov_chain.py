import random
import re
import os
import logging
import argparse
import json
from collections import Counter
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('markov_chain')

class MarkovChainGenerator:
    """A class to generate text using Markov chains with enhanced features."""

    def __init__(self, order=2, creativity=1.0):
        """Initialize the Markov Chain generator.

        Args:
            order (int): The number of words to consider for state (default: 2)
            creativity (float): Creativity factor (1.0 is normal, higher values increase randomness)
        """
        self.order = order
        self.creativity = creativity
        self.markov_chain = {}
        self.vocabulary = set()
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "source_length": 0,
            "chain_size": 0,
            "order": order
        }
        logger.info(f"Initialized MarkovChainGenerator with order {order} and creativity {creativity}")

    def clean_text(self, text, preserve_case=False):
        """Clean and normalize text.

        Args:
            text (str): Input text to clean
            preserve_case (bool): Whether to preserve case or convert to lowercase

        Returns:
            str: Cleaned text
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters except punctuation needed for sentence structure
        text = re.sub(r'[^\w\s.,!?;:\'\"-]', '', text)

        # Convert to lowercase if not preserving case
        if not preserve_case:
            text = text.lower()

        return text.strip()

    def build_chain(self, text, preserve_case=False):
        """Build a Markov chain from the input text.

        Args:
            text (str): Text to build the chain from
            preserve_case (bool): Whether to preserve case in the text

        Returns:
            dict: The built Markov chain
        """
        cleaned_text = self.clean_text(text, preserve_case)
        words = cleaned_text.split()

        if len(words) <= self.order:
            logger.warning("Text too short to build chain with current order")
            return {}

        logger.info(f"Building Markov chain from {len(words)} words")

        # Reset chain and vocabulary
        self.markov_chain = {}
        self.vocabulary = set(words)

        # Update metadata
        self.metadata.update({
            "created_at": datetime.now().isoformat(),
            "source_length": len(words),
            "vocabulary_size": len(self.vocabulary)
        })

        for i in range(len(words) - self.order):
            key = tuple(words[i:i+self.order])  # Create key (tuple of words)
            next_word = words[i + self.order]  # Get next word

            if key not in self.markov_chain:
                self.markov_chain[key] = []
            self.markov_chain[key].append(next_word)

        # Update metadata with chain size
        self.metadata["chain_size"] = len(self.markov_chain)
        logger.info(f"Built chain with {len(self.markov_chain)} states and {len(self.vocabulary)} unique words")
        return self.markov_chain

    def build_from_file(self, filepath, preserve_case=False):
        """Build a Markov chain from a text file.

        Args:
            filepath (str): Path to the text file
            preserve_case (bool): Whether to preserve case in the text

        Returns:
            dict: The built Markov chain
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
            logger.info(f"Successfully loaded text from {filepath}")
            self.metadata["source_file"] = os.path.basename(filepath)
            return self.build_chain(text, preserve_case)
        except Exception as e:
            logger.error(f"Error loading file {filepath}: {str(e)}")
            return {}

    def generate_text(self, length=50, start_words=None, creativity=None, temperature=1.0):
        """Generate text using the built Markov chain with creativity options.

        Args:
            length (int): Length of text to generate in words
            start_words (list): Optional list of starting words
            creativity (float): Override the default creativity factor
            temperature (float): Controls randomness (higher = more random)

        Returns:
            str: Generated text
        """
        if not self.markov_chain:
            logger.error("Cannot generate text: Markov chain is empty")
            return "Error: Markov chain not built yet."

        # Use provided creativity if given, otherwise use the instance value
        creativity_factor = creativity if creativity is not None else self.creativity

        # Choose starting point
        if start_words and len(start_words) >= self.order:
            # Use provided starting words if they exist in the chain
            key = tuple(start_words[-self.order:])
            if key not in self.markov_chain:
                logger.warning(f"Starting words {start_words} not found in chain, using random start")
                key = random.choice(list(self.markov_chain.keys()))
            generated_words = list(start_words)
        else:
            # Use random starting point
            key = random.choice(list(self.markov_chain.keys()))
            generated_words = list(key)

        logger.info(f"Generating text with length {length}, creativity {creativity_factor}, temperature {temperature}")

        for _ in range(length - len(generated_words)):
            # Normal Markov chain generation
            if key in self.markov_chain and self.markov_chain[key]:
                # Apply creativity factor - higher values increase chance of picking a random word
                if random.random() < (1.0 - 1.0/creativity_factor):
                    # Pick a completely random word from vocabulary for more creative output
                    next_word = random.choice(list(self.vocabulary))
                else:
                    # Apply temperature to control randomness
                    if temperature == 1.0:
                        next_word = random.choice(self.markov_chain[key])
                    else:
                        # With lower temperature, favor more common transitions
                        word_counts = Counter(self.markov_chain[key])
                        words, counts = zip(*word_counts.items())

                        # Adjust counts based on temperature
                        adjusted_counts = [count ** (1.0 / max(0.1, temperature)) for count in counts]
                        total = sum(adjusted_counts)
                        probabilities = [count / total for count in adjusted_counts]

                        next_word = random.choices(words, weights=probabilities, k=1)[0]

                generated_words.append(next_word)
                # Update key with the new sequence of words
                key = tuple(generated_words[-self.order:])
            else:
                logger.info("Reached end state with no transitions")
                break

        return " ".join(generated_words)

    def save_model(self, filepath):
        """Save the Markov chain model to a file.

        Args:
            filepath (str): Path to save the model

        Returns:
            bool: Success status
        """
        try:
            # Convert tuple keys to strings for JSON serialization
            serializable_chain = {}
            for key, value in self.markov_chain.items():
                serializable_chain[str(key)] = value

            model_data = {
                "metadata": self.metadata,
                "chain": serializable_chain,
                "vocabulary": list(self.vocabulary),
                "order": self.order,
                "creativity": self.creativity
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(model_data, f, indent=2)

            logger.info(f"Model saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False

    def load_model(self, filepath):
        """Load a Markov chain model from a file.

        Args:
            filepath (str): Path to the model file

        Returns:
            bool: Success status
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                model_data = json.load(f)

            # Extract metadata and parameters
            self.metadata = model_data.get("metadata", {})
            self.order = model_data.get("order", 2)
            self.creativity = model_data.get("creativity", 1.0)
            self.vocabulary = set(model_data.get("vocabulary", []))

            # Convert string keys back to tuples
            serialized_chain = model_data.get("chain", {})
            self.markov_chain = {}

            for key_str, value in serialized_chain.items():
                # Extract words from the string representation of the tuple
                key_parts = re.findall(r"'([^']*)'", key_str)
                if key_parts:
                    self.markov_chain[tuple(key_parts)] = value

            logger.info(f"Model loaded from {filepath} with {len(self.markov_chain)} states")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False

    def get_statistics(self):
        """Get statistics about the Markov chain.

        Returns:
            dict: Statistics about the chain
        """
        if not self.markov_chain:
            return {"error": "Chain is empty"}

        # Calculate transition statistics
        total_transitions = sum(len(values) for values in self.markov_chain.values())
        avg_transitions = total_transitions / max(1, len(self.markov_chain))

        # Find most common transitions
        transition_counts = {}
        for key, values in self.markov_chain.items():
            for word in values:
                state_str = ' '.join(key)
                transition = f"'{state_str}' → '{word}'"
                if transition in transition_counts:
                    transition_counts[transition] += 1
                else:
                    transition_counts[transition] = 1

        # Get top transitions
        top_transitions = sorted(transition_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "states": len(self.markov_chain),
            "vocabulary_size": len(self.vocabulary),
            "total_transitions": total_transitions,
            "avg_transitions_per_state": avg_transitions,
            "top_transitions": top_transitions,
            "metadata": self.metadata
        }

def main():
    """Main function to run the Markov Chain generator from command line."""
    parser = argparse.ArgumentParser(description='Generate text using a Markov Chain')
    parser.add_argument('--file', type=str, help='Input text file')
    parser.add_argument('--text', type=str, help='Input text directly')
    parser.add_argument('--order', type=int, default=2, help='Markov chain order (default: 2)')
    parser.add_argument('--length', type=int, default=50, help='Length of generated text (default: 50)')
    parser.add_argument('--start', type=str, help='Starting words (comma separated)')

    args = parser.parse_args()

    generator = MarkovChainGenerator(order=args.order)

    # Build chain from file or text
    if args.file:
        generator.build_from_file(args.file)
    elif args.text:
        generator.build_chain(args.text)
    else:
        # Use sample text if no input provided
        sample_text = """This is a simple example of a Markov Chain text generator.
        Markov chains are used to model sequences of words based on probabilities.
        The order of a Markov chain determines how many previous words are considered.
        Higher order chains produce more coherent text but require more data."""
        generator.build_chain(sample_text)

    # Parse starting words if provided
    start_words = None
    if args.start:
        start_words = args.start.split(',')

    # Generate and print text
    generated_text = generator.generate_text(length=args.length, start_words=start_words)
    print("🔹 Generated Text:\n", generated_text)

if __name__ == "__main__":
    main()