import pygame
from menu import main_menu
from game import Game
from settings import *


# Initialize Pygame
pygame.init()

def main():
    # Set up the screen
    screen = pygame.display.set_mode((800, 600))  # Replace with your WIDTH and HEIGHT
    pygame.display.set_caption("Liv")

    # Show the main menu
    main_menu(screen)

    # Run the game
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()
