import pygame

def weapon_selection(screen, font):
    # Weapons
    weapons = [
        {"name": "Shotgun", "description": "Wide spread, high damage, slow fire rate."},
        {"name": "Pistol", "description": "Balanced fire rate and damage."},
        {"name": "Rifle", "description": "High fire rate, long range, low damage."}
    ]

    # Define weapon box dimensions
    weapon_box_width = 400
    weapon_box_height = 100
    weapon_box_margin = 20
    weapon_boxes = []

    # Create weapon boxes
    for i, weapon in enumerate(weapons):
        x = (screen.get_width() - weapon_box_width) // 2
        y = 200 + i * (weapon_box_height + weapon_box_margin)
        rect = pygame.Rect(x, y, weapon_box_width, weapon_box_height)
        weapon_boxes.append(rect)

    # Weapon selection loop
    selected_weapon = None
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        # Render weapon boxes and text
        for i, weapon in enumerate(weapons):
            color = (200, 200, 200)  # Default color
            if weapon_boxes[i].collidepoint(pygame.mouse.get_pos()):
                color = (100, 255, 100)  # Highlighted color
            pygame.draw.rect(screen, color, weapon_boxes[i], border_radius=10)
            text = font.render(weapon["name"], True, (255, 255, 255))
            desc = font.render(weapon["description"], True, (255, 255, 255))
            screen.blit(text, (weapon_boxes[i].x + 10, weapon_boxes[i].y + 10))
            screen.blit(desc, (weapon_boxes[i].x + 10, weapon_boxes[i].y + 50))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(weapon_boxes):
                    if rect.collidepoint(event.pos):
                        selected_weapon = weapons[i]["name"]
                        running = False

        pygame.display.flip()

    return selected_weapon
