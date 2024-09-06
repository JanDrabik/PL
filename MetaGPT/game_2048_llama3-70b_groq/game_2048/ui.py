"""
UI class responsible for displaying the game board and score.
"""
import pygame

class UI:
    """
    UI class responsible for displaying the game board and score.
    
    Attributes:
    game (Game): The game instance.
    """
    def __init__(self, game: 'Game') -> None:
        """
        Initializes the UI with a game instance.
        
        Args:
        game (Game): The game instance.
        """
        self.game = game
        self.screen = pygame.display.set_mode((400, 400))  # Default screen size
        pygame.display.set_caption('2048 Game')

    def display_board(self) -> None:
        """
        Displays the game board.
        """
        self.screen.fill((255, 255, 255))  # White background
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.screen, (200, 200, 200), (j * 100, i * 100, 100, 100), 1)
                if self.game.board[i][j] != 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.game.board[i][j]), True, (0, 0, 0))
                    self.screen.blit(text, (j * 100 + 40, i * 100 + 40))
        pygame.display.flip()

    def display_score(self) -> None:
        """
        Displays the game score.
        """
        font = pygame.font.Font(None, 36)
        text = font.render('Score: ' + str(self.game.score), True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def handle_events(self) -> None:
        """
        Handles user events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.move_up()
                elif event.key == pygame.K_DOWN:
                    self.game.move_down()
                elif event.key == pygame.K_LEFT:
                    self.game.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.game.move_right()
                self.display_board()
                self.display_score()
