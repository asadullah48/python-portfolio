#!/usr/bin/env python3
"""
Connect Four - CLI Version
A terminal-based implementation of the classic Connect Four game.
Run with: python connect-four.py
"""

import os
import time
import numpy as np

# Game constants
ROW_COUNT = 6
COL_COUNT = 7

# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    BG_BLUE = '\033[44m'

class ConnectFourCLI:
    def __init__(self):
        """Initialize the Connect Four game with an empty board."""
        self.board = np.zeros((ROW_COUNT, COL_COUNT))
        self.game_over = False
        self.turn = 0  # 0 for Player 1 (Red), 1 for Player 2 (Yellow)
        self.winner = None
        self.moves_count = 0

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_board(self):
        """Print the current state of the board to the terminal."""
        self.clear_screen()
        print(f"\n{Colors.BOLD}🎮 Connect Four - CLI Edition{Colors.RESET}\n")
        
        # Print column numbers on top
        print("  ", end="")
        for col in range(COL_COUNT):
            print(f"{Colors.BOLD}{col + 1}{Colors.RESET} ", end="")
        print("\n")
        
        # Print the board from top to bottom
        for row in range(ROW_COUNT - 1, -1, -1):
            print(f"{Colors.BG_BLUE} ", end="")
            for col in range(COL_COUNT):
                if self.board[row][col] == 0:
                    print("⚪", end="")
                elif self.board[row][col] == 1:
                    print(f"{Colors.RED}🔴{Colors.RESET}", end="")
                else:
                    print(f"{Colors.YELLOW}🟡{Colors.RESET}", end="")
            print(f" {Colors.RESET}")
        
        # Print bottom border
        print(f"{Colors.BG_BLUE}" + " " * (COL_COUNT * 2 + 1) + f"{Colors.RESET}\n")

    def make_move(self, col):
        """Process a move in the selected column and return game status message."""
        if self.game_over:
            return "Game is over! Please restart to play again."
            
        if not 0 <= col < COL_COUNT:
            return f"Column must be between 1 and {COL_COUNT}."
            
        if not self.is_valid_location(col):
            return "Column is full! Choose another column."
            
        # Find the next open row and drop the piece
        row = self.get_next_open_row(col)
        piece = 1 if self.turn == 0 else 2
        self.drop_piece(row, col, piece)
        self.moves_count += 1
        
        # Check for win condition
        if self.check_win(piece):
            self.game_over = True
            self.winner = piece
            return f"🎉 Player {piece} ({self.get_player_color(piece)}) wins!"
        
        # Check for draw condition
        if self.moves_count == ROW_COUNT * COL_COUNT:
            self.game_over = True
            return "🤝 It's a draw!"
        
        # Switch turns
        self.turn = 1 - self.turn
        return None

    def get_player_color(self, piece):
        """Return the color name of the player piece."""
        return "Red" if piece == 1 else "Yellow"

    def drop_piece(self, row, col, piece):
        """Place a piece on the board at the specified position."""
        self.board[row][col] = piece

    def is_valid_location(self, col):
        """Check if a piece can be placed in the specified column."""
        return 0 <= col < COL_COUNT and self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        """Find the lowest empty row in the specified column."""
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r
        return -1  # Should never reach here if is_valid_location is checked first

    def check_win(self, piece):
        """Check if the current player has won after placing their piece."""
        # Horizontal check
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical check
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal check (positive slope)
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal check (negative slope)
        for c in range(COL_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True
                    
        return False

    def print_instructions(self):
        """Print game instructions."""
        print(f"{Colors.BOLD}HOW TO PLAY:{Colors.RESET}")
        print("1. Players take turns dropping colored discs into the board")
        print("2. Enter the column number (1-7) to drop your disc")
        print("3. Connect 4 discs in a row (horizontally, vertically, or diagonally) to win")
        print("4. Red goes first, followed by Yellow")
        print("5. Type 'quit' to exit the game\n")
        input("Press Enter to start the game...")

    def play(self):
        """Main game loop."""
        self.print_instructions()
        self.clear_screen()
        
        while not self.game_over:
            # Print the current board
            self.print_board()
            
            # Show whose turn it is
            player_color = Colors.RED if self.turn == 0 else Colors.YELLOW
            player_symbol = "🔴" if self.turn == 0 else "🟡"
            print(f"{player_color}Player {self.turn + 1}'s turn {player_symbol}{Colors.RESET}")
            
            # Get player input
            try:
                move = input("Enter column (1-7) or 'quit' to exit: ")
                
                if move.lower() == 'quit':
                    print("Thanks for playing!")
                    return
                
                col = int(move) - 1  # Convert to 0-indexed
                
                result = self.make_move(col)
                if result:
                    self.print_board()
                    print(result)
                    if self.game_over:
                        play_again = input("\nPlay again? (y/n): ")
                        if play_again.lower() == 'y':
                            self.__init__()  # Reset the game
                            self.clear_screen()
                            continue
                        else:
                            print("Thanks for playing!")
                            return
            
            except ValueError:
                print("Please enter a valid column number.")
                time.sleep(1)
                continue
            except KeyboardInterrupt:
                print("\nGame interrupted. Thanks for playing!")
                return

def main():
    """Entry point for the Connect Four CLI game."""
    game = ConnectFourCLI()
    try:
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")

if __name__ == "__main__":
    main()