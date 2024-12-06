import pygame
def map_selection(screen, font):
    background = pygame.image.load("selectionbg.jpg").convert()  # Replace with your image file
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    # Load map previews (replace with your images)
    maps = [
        {"name": "Grasslands", "image": pygame.image.load("Grass_Sample.png").convert()},
        {"name": "Desert", "image": pygame.image.load("desert.jpg").convert()},
        {"name": "Dungeon", "image": pygame.image.load("dungeon.jpeg").convert()},
    ]

    # Scale images to preview size
    preview_width, preview_height = 300, 200
    for map_option in maps:
        map_option["image"] = pygame.transform.scale(map_option["image"], (preview_width, preview_height))

    # Define box dimensions for map previews
    box_width = preview_width + 20
    box_height = preview_height + 60
    box_margin = 40
    total_width = len(maps) * (box_width + box_margin) - box_margin
    start_x = (screen.get_width() - total_width) // 2
    start_y = screen.get_height() // 2 - box_height // 2

    # Create map selection boxes
    map_boxes = []
    for i, map_option in enumerate(maps):
        x = start_x + i * (box_width + box_margin)
        y = start_y
        rect = pygame.Rect(x, y, box_width, box_height)
        map_boxes.append(rect)

    # Map selection loop
    selected_map = None
    running = True
    while running:
        # Draw background
        screen.blit(background, (0, 0))  # Draw background image

        # Render map selection boxes
        for i, map_option in enumerate(maps):
            box_color = (200, 200, 200)  # Default box color
            if map_boxes[i].collidepoint(pygame.mouse.get_pos()):
                box_color = (100, 255, 100)  # Highlighted color
            pygame.draw.rect(screen, box_color, map_boxes[i], border_radius=10)

            # Draw the map image
            image_x = map_boxes[i].x + 10
            image_y = map_boxes[i].y + 10
            screen.blit(map_option["image"], (image_x, image_y))

            # Draw the map name
            text_surface = font.render(map_option["name"], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(map_boxes[i].centerx, map_boxes[i].bottom - 20))
            screen.blit(text_surface, text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(map_boxes):
                    if rect.collidepoint(event.pos):
                        selected_map = maps[i]["name"]  # Save selected map name
                        running = False  # Exit map selection loop

        pygame.display.flip()

    return selected_map
