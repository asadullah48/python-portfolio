import numpy as np

class AIPlayer:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        
    def get_move(self, board):
        if self.difficulty == 'easy':
            return self._random_move(board)
        elif self.difficulty == 'medium':
            return self._smart_move(board)
        else:
            return self._minimax(board)
            
    def _random_move(self, board):
        valid_moves = [c for c in range(7) if board[5][c] == 0]
        return np.random.choice(valid_moves) if valid_moves else None
        
    def _smart_move(self, board):
        # Check for winning move
        for col in range(7):
            if self._is_winning_move(board, col, 2):
                return col
        # Block opponent's winning move
        for col in range(7):
            if self._is_winning_move(board, col, 1):
                return col
        return self._random_move(board)