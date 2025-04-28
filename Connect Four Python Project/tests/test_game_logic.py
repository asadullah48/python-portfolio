import pytest
from connect_four import ConnectFourGame

def test_horizontal_win():
    game = ConnectFourGame()
    # Place 4 pieces in a row horizontally
    for col in range(4):
        game.make_move(col)  # Player 1
        if col < 3:
            game.make_move(6)  # Player 2
    
    assert game.check_win(1) == True
    assert game.winner == 1

def test_vertical_win():
    game = ConnectFourGame()
    # Place 4 pieces in a column
    for _ in range(4):
        game.make_move(0)  # Player 1
        if _ < 3:
            game.make_move(1)  # Player 2
    
    assert game.check_win(1) == True