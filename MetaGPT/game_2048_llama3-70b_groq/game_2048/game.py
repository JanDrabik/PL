"""
This module contains the Game class, which represents the game state and provides methods for game logic.
"""

class Game:
    """
    The Game class represents the game state and provides methods for game logic.
    
    Attributes:
    - board (list[list[int]]): A 2D list representing the game board.
    - score (int): The current score of the game.
    - difficulty (str): The difficulty level of the game.
    """
    
    def __init__(self, difficulty: str = "easy"):
        """
        Initializes a new game with the specified difficulty level.
        
        Args:
        - difficulty (str): The difficulty level of the game. Defaults to "easy".
        """
        self.board = [[0]*4 for _ in range(4)]  # Initialize a 4x4 game board
        self.score = 0
        self.difficulty = difficulty
    
    def start_game(self):
        """
        Starts a new game by resetting the board and score.
        """
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
    
    def move_up(self):
        """
        Moves the tiles up in the game board.
        """
        # TO DO: Implement the logic for moving tiles up
        pass
    
    def move_down(self):
        """
        Moves the tiles down in the game board.
        """
        # TO DO: Implement the logic for moving tiles down
        pass
    
    def move_left(self):
        """
        Moves the tiles left in the game board.
        """
        # TO DO: Implement the logic for moving tiles left
        pass
    
    def move_right(self):
        """
        Moves the tiles right in the game board.
        """
        # TO DO: Implement the logic for moving tiles right
        pass
    
    def get_score(self):
        """
        Returns the current score of the game.
        
        Returns:
        - int: The current score of the game.
        """
        return self.score
