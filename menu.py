import pygame

# Colors (for text if needed)
WHITE = (255, 255, 255)

# Fonts
pygame.init()  # Ensure Pygame is initialized
font = pygame.font.SysFont(None, 48)

def draw_text(screen, text, x, y, color=WHITE):
    """Draw text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def main_menu(screen):
    """Display the main menu with a background image and button images."""
    menu_running = True

    # Load background image
    background_img = pygame.image.load("menubg.gif").convert()
    background_img = pygame.transform.scale(background_img, (1280, 720))

    # Load button images
    start_button_img = pygame.image.load("PlayBtn.png").convert_alpha()
    quit_button_img = pygame.image.load("ExitBtn.png").convert_alpha()
    
    # Scale buttons if needed
    start_button_img = pygame.transform.scale(start_button_img, (200, 100))
    quit_button_img = pygame.transform.scale(quit_button_img, (200, 100))
    
    # Button positions
    start_button_rect = start_button_img.get_rect(center=(640, 300))  # Center of the screen
    quit_button_rect = quit_button_img.get_rect(center=(640, 450))  # Below the start button

    while menu_running:
        # Draw background
        screen.blit(background_img, (0, 0))

        # Draw title
        draw_text(screen, "Liv", 540, 150, WHITE)

        # Draw buttons
        screen.blit(start_button_img, start_button_rect.topleft)
        screen.blit(quit_button_img, quit_button_rect.topleft)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):  # Start button clicked
                    menu_running = False
                elif quit_button_rect.collidepoint(mouse_pos):  # Quit button clicked
                    pygame.quit()
                    exit()
