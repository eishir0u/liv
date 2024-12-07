import pygame

def weapon_selection(screen, font):
    # Load background image
    background = pygame.image.load("asset/selectionbg.jpg").convert()  # Replace with your image file
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))  # Scale to fit the screen
    # Weapons
    weapons = [
        {"name": "Shotgun", "image": pygame.image.load("asset/shotgun.png").convert_alpha()},
        {"name": "Pistol", "image": pygame.image.load("asset/pistol.png").convert_alpha()},
        {"name": "Rifle", "image": pygame.image.load("asset/rifle.png").convert_alpha()}
    ]

    # Scale weapon images for consistency
    for weapon in weapons:
        weapon["image"] = pygame.transform.scale(weapon["image"], (150, 150))  # Resize as needed
        

    # Define weapon box dimensions
    weapon_box_width = 200
    weapon_box_height = 250
    weapon_box_margin = 30
    border_radius = 15  # Rounded corner radius

    # Calculate horizontal positioning
    total_width = len(weapons) * weapon_box_width + (len(weapons) - 1) * weapon_box_margin
    start_x = (screen.get_width() - total_width) // 2  # Center horizontally

    # Create weapon boxes
    weapon_boxes = []
    for i, weapon in enumerate(weapons):
        x = start_x + i * (weapon_box_width + weapon_box_margin)
        y = screen.get_height() // 2 - weapon_box_height // 2
        rect = pygame.Rect(x, y, weapon_box_width, weapon_box_height)
        weapon_boxes.append(rect)

    # Weapon selection loop
    selected_weapon = None
    running = True
    while running:
        # Draw background
        screen.blit(background, (0, 0))  # Draw background image

        # Render weapon boxes and images
        for i, weapon in enumerate(weapons):
            # Create semi-transparent surface for the weapon box
            box_surface = pygame.Surface((weapon_box_width, weapon_box_height), pygame.SRCALPHA)
            if weapon_boxes[i].collidepoint(pygame.mouse.get_pos()):
                color = (100, 255, 100, 150)  # Semi-transparent green when hovered
            else:
                color = (200, 200, 200, 150)  # Semi-transparent grey
            box_surface.fill((0, 0, 0, 0))  # Make the surface fully transparent
            pygame.draw.rect(box_surface, color, (0, 0, weapon_box_width, weapon_box_height), border_radius=border_radius)

            # Blit the semi-transparent rounded box onto the screen
            screen.blit(box_surface, (weapon_boxes[i].x, weapon_boxes[i].y))

            # Draw weapon image
            image_x = weapon_boxes[i].x + (weapon_box_width - weapon["image"].get_width()) // 2
            image_y = weapon_boxes[i].y + 20
            screen.blit(weapon["image"], (image_x, image_y))

            # Draw weapon name
            name_surface = font.render(weapon["name"], True, (255, 255, 255))
            name_x = weapon_boxes[i].x + (weapon_box_width - name_surface.get_width()) // 2
            name_y = weapon_boxes[i].y + weapon_box_height - 40
            screen.blit(name_surface, (name_x, name_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(weapon_boxes):
                    if rect.collidepoint(event.pos):
                        selected_weapon = weapons[i]["name"]
                        running = False  # Exit the selection loop

        pygame.display.flip()

    return selected_weapon
