"""
This module contains the GameAlgorithm class, which is responsible for generating tiles and checking the game over status.
"""

import random

class GameAlgorithm:
    """
    This class contains methods to generate tiles and check the game over status.
    """
    def __init__(self, game: 'Game') -> None:
        """
        Initializes the GameAlgorithm class with a Game instance.
        
        Args:
        game (Game): The Game instance.
        """
        self.game = game

    def generate_tile(self) -> None:
        """
        Generates a new tile on the game board.
        """
        # Randomly select a position on the board
        row = random.randint(0, len(self.game.board) - 1)
        col = random.randint(0, len(self.game.board[0]) - 1)
        
        # Check if the position is empty
        if self.game.board[row][col] == 0:
            # Generate a new tile with a value of 2 or 4
            self.game.board[row][col] = random.choice([2, 4])

    def check_game_over(self) -> bool:
        """
        Checks if the game is over.
        
        Returns:
        bool: True if the game is over, False otherwise.
        """
        # Check if there are any empty cells on the board
        for row in self.game.board:
            for cell in row:
                if cell == 0:
                    return False
        
        # Check if there are any possible moves
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                if i < len(self.game.board) - 1 and self.game.board[i][j] == self.game.board[i + 1][j]:
                    return False
                if j < len(self.game.board[0]) - 1 and self.game.board[i][j] == self.game.board[i][j + 1]:
                    return False
        
        return True

    def update_score(self) -> None:
        """
        Updates the game score.
        """
        # TO DO: Implement the logic to update the score
        pass
