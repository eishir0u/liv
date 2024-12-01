import pygame
import random
from settings import *

# # def spawn_enemy():
# def spawn_enemy():
#     """Spawns an enemy at a random edge of the world (not screen)."""
#     side = random.choice(["top", "bottom", "left", "right"])
#     if side == "top":
#         x = random.randint(0, WIDTH) + camera_offset[0]
#         y = -20 + camera_offset[1]
#     elif side == "bottom":
#         x = random.randint(0, WIDTH) + camera_offset[0]
#         y = HEIGHT + 20 + camera_offset[1]
#     elif side == "left":
#         x = -20 + camera_offset[0]
#         y = random.randint(0, HEIGHT) + camera_offset[1]
#     else:  # "right"
#         x = WIDTH + 20 + camera_offset[0]
#         y = random.randint(0, HEIGHT) + camera_offset[1]
#     return pygame.Rect(x, y, 20, 20)

def spawn_enemy():
    """Spawns an enemy at a random edge of the world."""
    enemy_size = 40  # Adjust size dynamically if needed
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH) + camera_offset[0]
        y = -enemy_size + camera_offset[1]
    elif side == "bottom":
        x = random.randint(0, WIDTH) + camera_offset[0]
        y = HEIGHT + enemy_size + camera_offset[1]
    elif side == "left":
        x = -enemy_size + camera_offset[0]
        y = random.randint(0, HEIGHT) + camera_offset[1]
    else:  # "right"
        x = WIDTH + enemy_size + camera_offset[0]
        y = random.randint(0, HEIGHT) + camera_offset[1]
    return pygame.Rect(x, y, enemy_size, enemy_size)