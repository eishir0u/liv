import pygame

def skill_selection(screen, font):
    # Skills
    skills = [
        {"name": "Speed", "description": "Increase player speed."},
        {"name": "Attack Speed", "description": "Reduce fire rate."},
        {"name": "Health", "description": "Increase player health."}
    ]

    # Define skill box dimensions
    skill_box_width = 400
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
        screen.fill((0, 0, 0))  # Clear the screen

        # Render skill boxes and text
        for i, skill in enumerate(skills):
            color = (200, 200, 200)  # Default color
            if skill_boxes[i].collidepoint(pygame.mouse.get_pos()):
                color = (100, 100, 255)  # Highlighted color
            pygame.draw.rect(screen, color, skill_boxes[i], border_radius=10)
            text = font.render(skill["name"], True, (255, 255, 255))
            desc = font.render(skill["description"], True, (255, 255, 255))
            screen.blit(text, (skill_boxes[i].x + 10, skill_boxes[i].y + 10))
            screen.blit(desc, (skill_boxes[i].x + 10, skill_boxes[i].y + 50))

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
