import random
from enum import Enum, auto
from typing import Tuple, Dict, Optional

class Choice(Enum):
    """Enumeration of possible game choices."""
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def __str__(self):
        return self.name.lower()

class GameResult(Enum):
    """Possible game outcomes."""
    WIN = auto()
    LOSE = auto()
    DRAW = auto()

class RockPaperScissors:
    """A complete Rock-Paper-Scissors game implementation."""
    
    WIN_CONDITIONS: Dict[Tuple[Choice, Choice], GameResult] = {
        (Choice.ROCK, Choice.SCISSORS): GameResult.WIN,
        (Choice.PAPER, Choice.ROCK): GameResult.WIN,
        (Choice.SCISSORS, Choice.PAPER): GameResult.WIN,
    }
    
    EMOJIS = {
        Choice.ROCK: "🪨",
        Choice.PAPER: "📄",
        Choice.SCISSORS: "✂️"
    }
    
    def __init__(self):
        """Initialize game with score tracking."""
        self.scores = {"player": 0, "computer": 0, "ties": 0}
        self.round = 0

    def _get_computer_choice(self) -> Choice:
        """Generate a random choice for the computer."""
        return random.choice(list(Choice))

    def _get_user_choice(self) -> Optional[Choice]:
        """Prompt user for their choice with validation."""
        while True:
            user_input = input(
                "\nChoose (r)ock, (p)aper, (s)cissors, or (q)uit: "
            ).strip().lower()
            
            if user_input in ('q', 'quit'):
                return None
            
            choice_map = {
                'r': Choice.ROCK,
                'p': Choice.PAPER,
                's': Choice.SCISSORS,
                'rock': Choice.ROCK,
                'paper': Choice.PAPER,
                'scissors': Choice.SCISSORS
            }
            
            if user_input in choice_map:
                return choice_map[user_input]
            
            print("❌ Invalid choice! Please try again.")

    def _determine_winner(self, user: Choice, computer: Choice) -> GameResult:
        """Determine the game outcome based on choices."""
        if user == computer:
            return GameResult.DRAW
        return self.WIN_CONDITIONS.get((user, computer), GameResult.LOSE)

    def _display_result(self, user: Choice, computer: Choice, result: GameResult) -> None:
        """Show the game result with visual feedback."""
        print(f"\nYou chose: {user} {self.EMOJIS[user]}")
        print(f"Computer chose: {computer} {self.EMOJIS[computer]}")
        
        if result == GameResult.WIN:
            print("🎉 You win this round!")
            self.scores["player"] += 1
        elif result == GameResult.LOSE:
            print("💻 Computer wins this round!")
            self.scores["computer"] += 1
        else:
            print("🤝 It's a tie!")
            self.scores["ties"] += 1
        
        print(f"\nScore: You {self.scores['player']} - {self.scores['computer']} Computer "
              f"(Ties: {self.scores['ties']})")

    def _show_welcome(self) -> None:
        """Display welcome message and instructions."""
        print("\n" + "=" * 50)
        print(" ROCK PAPER SCISSORS ".center(50, "🔥"))
        print("=" * 50)
        print("\nGame Rules:")
        print("- Rock beats Scissors")
        print("- Paper beats Rock")
        print("- Scissors beat Paper")
        print("\nCommands:")
        print("(r)ock, (p)aper, (s)cissors, or (q)uit")

    def _show_final_stats(self) -> None:
        """Display game statistics when quitting."""
        total = sum(self.scores.values())
        if total == 0:
            return
            
        print("\n" + "=" * 25 + " FINAL STATS " + "=" * 25)
        print(f"Total Rounds Played: {total}")
        print(f"Your Wins: {self.scores['player']}")
        print(f"Computer Wins: {self.scores['computer']}")
        print(f"Ties: {self.scores['ties']}")
        
        win_rate = (self.scores['player'] / (total - self.scores['ties'])) * 100
        print(f"Win Rate: {win_rate:.1f}%")
        print("=" * 62)

    def play_round(self) -> bool:
        """Play one round of the game."""
        self.round += 1
        print(f"\nRound {self.round}")
        
        user_choice = self._get_user_choice()
        if user_choice is None:
            return False
        
        computer_choice = self._get_computer_choice()
        result = self._determine_winner(user_choice, computer_choice)
        self._display_result(user_choice, computer_choice, result)
        
        return True

    def run(self) -> None:
        """Run the game with multiple rounds."""
        self._show_welcome()
        
        while True:
            if not self.play_round():
                self._show_final_stats()
                print("\nThanks for playing! Goodbye! 👋")
                break

if __name__ == "__main__":
    try:
        game = RockPaperScissors()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")