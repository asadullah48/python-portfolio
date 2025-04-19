#!/usr/bin/env python3
from minesweeper import Minesweeper

if __name__ == "__main__":
    print("🎮 Welcome to Minesweeper CLI! 🎮")
    
    try:
        size = int(input("Enter board size (5-15): "))
        size = max(5, min(15, size))  # Clamp between 5 and 15
        
        bombs = int(input(f"Enter number of bombs (1-{size*size//2}): "))
        bombs = max(1, min(size*size//2, bombs))  # Ensure reasonable bomb count
    except ValueError:
        print("Invalid input, using default values.")
        size = 8
        bombs = 10
    
    # Start Game
    game = Minesweeper(size=size, bombs=bombs)
    game.play()