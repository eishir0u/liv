import pygame
import os
from weapon_selection import weapon_selection

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
    """Display the main menu with an animated background."""
    menu_running = True

    # Load frames for the animated background
    background_frames = []
    frame_folder = "menuframes"  # Folder containing frames
    for frame_file in sorted(os.listdir(frame_folder)):  # Ensure frames are loaded in order
        frame_path = os.path.join(frame_folder, frame_file)
        
        # Load and scale each frame
        frame = pygame.image.load(frame_path).convert()
        frame = pygame.transform.scale(frame, (1280, 720))  # Change size to screen resolution
        background_frames.append(frame)

    # Load button images
    start_button_img = pygame.image.load("PlayBtn.png").convert_alpha()
    quit_button_img = pygame.image.load("ExitBtn.png").convert_alpha()

    # Scale buttons if needed
    start_button_img = pygame.transform.scale(start_button_img, (200, 100))
    quit_button_img = pygame.transform.scale(quit_button_img, (200, 100))

    # Button positions
    start_button_rect = start_button_img.get_rect(center=(640, 300))  # Center of the screen
    quit_button_rect = quit_button_img.get_rect(center=(640, 450))  # Below the start button

    # Animation variables
    current_frame = 0
    frame_delay = 100  # Delay in milliseconds between frames
    last_frame_update = pygame.time.get_ticks()

    while menu_running:
        # Get the current time
        now = pygame.time.get_ticks()

        # Update the background frame
        if now - last_frame_update > frame_delay:
            current_frame = (current_frame + 1) % len(background_frames)  # Loop through frames
            last_frame_update = now

        # Draw the current frame of the animated background
        screen.blit(background_frames[current_frame], (0, 0))

        # Draw title
        draw_text(screen, "Liv", 540, 150, WHITE)

        # Draw buttons
        screen.blit(start_button_img, start_button_rect.topleft)
        screen.blit(quit_button_img, quit_button_rect.topleft)

        pygame.display.flip()
        # Event handling for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):  # Start button clicked
                    menu_running = False
                    selected_weapon = weapon_selection(screen, font)  # Call weapon selection
                    print(f"Selected Weapon: {selected_weapon}")  # For debugging/logging
                    
                elif quit_button_rect.collidepoint(mouse_pos):  # Quit button clicked
                    pygame.quit()
                    exit()
                    