import random

class Minesweeper:
    def __init__(self, size=5, bombs=3):
        """
        Initialize a Minesweeper game.
        
        Args:
            size (int): The size of the board (size x size).
            bombs (int): Number of bombs to place on the board.
        """
        self.size = size
        self.bombs = min(bombs, size * size - 1)  # Ensure bombs don't exceed board capacity
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.bomb_positions = set()
        self.revealed = set()
        self.flagged = set()  # Add flagging capability
        self.game_over = False
        self.won = False
        self._place_bombs()
    
    def _place_bombs(self):
        """Place bombs randomly on the board."""
        while len(self.bomb_positions) < self.bombs:
            r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.bomb_positions.add((r, c))
    
    def _count_adjacent_bombs(self, r, c):
        """
        Count the number of bombs adjacent to the given cell.
        
        Args:
            r (int): Row index.
            c (int): Column index.
            
        Returns:
            int: Number of adjacent bombs.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = sum((r+dr, c+dc) in self.bomb_positions 
                    for dr, dc in directions 
                    if 0 <= r+dr < self.size and 0 <= c+dc < self.size)
        return count
    
    def reveal(self, r, c):
        """
        Reveal a cell at the given coordinates.
        
        Args:
            r (int): Row index.
            c (int): Column index.
            
        Returns:
            bool: True if the move is valid, False if game over.
        """
        # Check if game is already over
        if self.game_over or self.won:
            return False
            
        # Check if the cell is already revealed or flagged
        if (r, c) in self.revealed or (r, c) in self.flagged:
            return True
            
        # Check if hit a bomb
        if (r, c) in self.bomb_positions:
            self.game_over = True
            return False
        
        # Reveal the cell
        self.revealed.add((r, c))
        bomb_count = self._count_adjacent_bombs(r, c)
        self.board[r][c] = str(bomb_count) if bomb_count > 0 else '0'
        
        # Auto-reveal empty cells
        if bomb_count == 0:
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    self.reveal(nr, nc)
        
        # Check if won
        if len(self.revealed) == (self.size ** 2 - self.bombs):
            self.won = True
            
        return True
    
    def toggle_flag(self, r, c):
        """
        Toggle a flag at the given coordinates.
        
        Args:
            r (int): Row index.
            c (int): Column index.
        """
        if (r, c) in self.revealed:
            return
            
        if (r, c) in self.flagged:
            self.flagged.remove((r, c))
        else:
            self.flagged.add((r, c))
    
    def get_cell_display(self, r, c):
        """
        Get the display character for a cell.
        
        Args:
            r (int): Row index.
            c (int): Column index.
            
        Returns:
            str: Character to display for the cell.
        """
        if (r, c) in self.flagged:
            return "🚩"
        elif (r, c) not in self.revealed:
            return "□"
        elif (r, c) in self.bomb_positions:
            return "💣"
        else:
            bomb_count = self._count_adjacent_bombs(r, c)
            if bomb_count == 0:
                return " "
            return str(bomb_count)
    
    def display(self):
        """Display the current state of the board."""
        # Print column numbers
        print("  " + " ".join(str(i) for i in range(self.size)))
        
        for r in range(self.size):
            # Print row number
            print(f"{r} ", end="")
            
            for c in range(self.size):
                if self.game_over and (r, c) in self.bomb_positions:
                    print("💣", end=" ")
                elif (r, c) in self.flagged:
                    print("🚩", end=" ")
                elif (r, c) not in self.revealed:
                    print("□", end=" ")
                else:
                    bomb_count = self._count_adjacent_bombs(r, c)
                    print(str(bomb_count) if bomb_count > 0 else " ", end=" ")
            print()
    
    def play(self):
        """Run the game interactively in the console."""
        print("🎮 Welcome to Minesweeper! 🎮")
        print("Enter 'r row col' to reveal a cell")
        print("Enter 'f row col' to flag/unflag a cell")
        print("Enter 'q' to quit")
        
        while not (self.game_over or self.won):
            self.display()
            
            try:
                cmd = input("Enter command: ").strip().split()
                if not cmd:
                    continue
                    
                if cmd[0] == 'q':
                    print("Thanks for playing!")
                    return
                    
                if cmd[0] not in ['r', 'f'] or len(cmd) != 3:
                    print("Invalid command format. Use 'r row col' or 'f row col'")
                    continue
                    
                r, c = int(cmd[1]), int(cmd[2])
                
                if not (0 <= r < self.size and 0 <= c < self.size):
                    print("Invalid coordinates, try again.")
                    continue
                    
                if cmd[0] == 'r':
                    if not self.reveal(r, c):
                        self.display()
                        print("💣 You hit a bomb! Game Over!")
                        break
                    if self.won:
                        self.display()
                        print("🎉 Congratulations! You cleared the board!")
                        break
                elif cmd[0] == 'f':
                    self.toggle_flag(r, c)
                    
            except ValueError:
                print("Invalid input, please try again.")
                
        # Game ended, show final board
        self.display()
        if self.game_over:
            print("💣 Game Over! You hit a bomb.")
        elif self.won:
            print("🎉 You won!")
        else:
            print("Thanks for playing!")