import pygame
import random
import os
from settings import *

# def spawn_enemy():
def spawn_enemy(elapsed_time):
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
     # Calculate HP dynamically (e.g., base HP + increase per minute)
    # Calculate HP dynamically
    base_hp = 100
    hp_increase_rate = 100  # Extra HP per minute
    max_health = base_hp + (elapsed_time // 60000) * hp_increase_rate  # Increase HP every minute

    enemy = {
        "rect": pygame.Rect(x, y, enemy_size, enemy_size),
        "health": max_health,  # Current health starts at max health
        "max_health": max_health,  # Store the max health
        "facing_right": True  # Default to facing right
    }
    return enemy

# Load enemy animation frames
def load_animation_frames(folder, size=(40, 40)):
    """Load frames from a folder and resize to the specified size."""
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            frame = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            frames.append(pygame.transform.scale(frame, size))
    return frames

enemy_frames = load_animation_frames("enemy_frames", size=(40, 40))  # Updated size
enemy_frame_index = 0
enemy_frame_delay = 100  # Milliseconds between frames
last_frame_time = pygame.time.get_ticks()