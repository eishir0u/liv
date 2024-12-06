import pygame

def pause_screen(screen, font):
    background = pygame.image.load("selectionbg.jpg").convert()  
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    pause_running = True
    pause_font = pygame.font.SysFont(None, 48)
    
    # Define button colors
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (100, 100, 255)
    
    # Load button images
    resume_button_img = pygame.image.load("ResumeBtn.png").convert_alpha() 
    return_button_img = pygame.image.load("ReturnBtn.png").convert_alpha() 
    
    resume_button_img = pygame.transform.scale(resume_button_img, (150, 100))
    return_button_img = pygame.transform.scale(return_button_img, (150, 100))

    resume_button_rect = resume_button_img.get_rect(center=(screen.get_width() // 2, 300))
    return_button_rect = return_button_img.get_rect(center=(screen.get_width() // 2, 450))

    while pause_running:
        screen.blit(background, (0, 0))
        
        # Draw pause text
        pause_text = pause_font.render("PAUSED", True, WHITE)
        pause_text_rect = pause_text.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(pause_text, pause_text_rect)
        
        # Draw buttons
        screen.blit(resume_button_img, resume_button_rect.topleft)
        screen.blit(return_button_img, return_button_rect.topleft)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                if resume_button_rect.collidepoint(mouse_pos):  # Resume button clicked
                    pause_running = False
                elif return_button_rect.collidepoint(mouse_pos):  # Return to Menu button clicked
                    return "menu"  # This will return to the main menu

        pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS
    return "resume"  # If the game resumes
