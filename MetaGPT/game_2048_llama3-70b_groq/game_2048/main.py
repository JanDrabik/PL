import pygame
from game import Game

def main():
    """
    Main function to start the game.
    """
    pygame.init()
    game = Game("easy")  # Initialize the game with default difficulty as "easy"
    game.start_game()

if __name__ == "__main__":
    main()
