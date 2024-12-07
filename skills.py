import pygame

def skill_selection(screen, font):
    background = pygame.image.load("asset/selectionbg.jpg").convert()  
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))  # Scale to screen size

# Load unique skill icons
    icons = {
        "Speed": pygame.image.load("asset/speed.png").convert_alpha(),
        "Attack Speed": pygame.image.load("asset/aspd.png").convert_alpha(),
        "Health": pygame.image.load("asset/health.png").convert_alpha()
    }

    # Scale icons to a consistent size
    icon_size = (80, 80)
    for key in icons:
        icons[key] = pygame.transform.scale(icons[key], icon_size)

    skills = [
        {"name": "Speed", "description": "Increase player speed.", "icon": icons["Speed"]},
        {"name": "Attack Speed", "description": "Increase fire rate.", "icon": icons["Attack Speed"]},
        {"name": "Health", "description": "Increase max health.", "icon": icons["Health"]}
    ]

    # Define skill box dimensions
    skill_box_width = 600
    skill_box_height = 100
    skill_box_margin = 20
    skill_boxes = []

    # Create skill boxes
    for i, skill in enumerate(skills):
        x = (screen.get_width() - skill_box_width) // 2
        y = 200 + i * (skill_box_height + skill_box_margin)
        rect = pygame.Rect(x, y, skill_box_width, skill_box_height)
        skill_boxes.append(rect)

    # Skill selection loop
    selected_skill = None
    running = True
    while running:
        screen.blit(background, (0, 0))  # Draw the background image

        # Render skill boxes and text
        for i, skill in enumerate(skills):
            color = (200, 200, 200)  # Default color
            if skill_boxes[i].collidepoint(pygame.mouse.get_pos()):
                color = (100, 100, 255)  # Highlighted color
            pygame.draw.rect(screen, color, skill_boxes[i], border_radius=10)

            # Draw skill icon
            icon_x = skill_boxes[i].x + 10
            icon_y = skill_boxes[i].y + (skill_box_height - icon_size[1]) // 2
            screen.blit(skill["icon"], (icon_x, icon_y))

            # Draw skill name and description
            text_x = icon_x + icon_size[0] + 10
            text = font.render(skill["name"], True, (255, 255, 255))
            desc = font.render(skill["description"], True, (255, 255, 255))
            screen.blit(text, (text_x, skill_boxes[i].y + 10))
            screen.blit(desc, (text_x, skill_boxes[i].y + 50))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(skill_boxes):
                    if rect.collidepoint(event.pos):
                        selected_skill = skills[i]["name"]
                        running = False

        pygame.display.flip()

    return selected_skill
