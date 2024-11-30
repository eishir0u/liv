import pygame
import random
import math
import os
from menu import main_menu
from settings import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("liv")

# Game variables
clock = pygame.time.Clock()
enemy_speed = 2
wave_interval = 5000  # Time between waves (ms)

# Load sprites
background_img = pygame.image.load("Grass_Sample.png").convert()
player_img = pygame.image.load("gigi.jpg").convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))  # Larger player size
bullet_img = pygame.image.load("gigi.jpg").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (10, 10))  # Resize bullets

# Fonts
font = pygame.font.SysFont(None, 36)

# Load enemy animation frames
def load_animation_frames(folder):
    """Load frames from a folder."""
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            frame = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            frames.append(pygame.transform.scale(frame, (30, 30)))  # Increased enemy size
    return frames

enemy_frames = load_animation_frames("enemy_frames")  # Folder containing animation frames
enemy_frame_index = 0
enemy_frame_delay = 100  # Milliseconds between frames
last_frame_time = pygame.time.get_ticks()

# Functions
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def spawn_enemy():
    """Spawns an enemy at a random edge of the world (not screen)."""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH) + camera_offset[0]
        y = -30 + camera_offset[1]
    elif side == "bottom":
        x = random.randint(0, WIDTH) + camera_offset[0]
        y = HEIGHT + 30 + camera_offset[1]
    elif side == "left":
        x = -30 + camera_offset[0]
        y = random.randint(0, HEIGHT) + camera_offset[1]
    else:  # "right"
        x = WIDTH + 30 + camera_offset[0]
        y = random.randint(0, HEIGHT) + camera_offset[1]
    return pygame.Rect(x, y, 30, 30)  # Adjusted for larger enemies

def move_towards(rect, target, speed):
    """Move a rectangle towards a target at a given speed."""
    dx, dy = target[0] - rect.x, target[1] - rect.y
    dist = math.sqrt(dx**2 + dy**2)
    if dist != 0:
        rect.x += int(dx / dist * speed)
        rect.y += int(dy / dist * speed)

# Camera setup
camera_offset = [0, 0]  # Offset of the camera
background_width, background_height = background_img.get_width(), background_img.get_height()

# Infinite background tiling
def draw_background():
    start_x = int(camera_offset[0] // background_width)
    start_y = int(camera_offset[1] // background_height)

    for x in range(start_x, start_x + WIDTH // background_width + 2):
        for y in range(start_y, start_y + HEIGHT // background_height + 2):
            tile_x = x * background_width - int(camera_offset[0])
            tile_y = y * background_height - int(camera_offset[1])
            screen.blit(background_img, (tile_x, tile_y))

# Game variables
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
bullets = []
enemies = []
player_health = 10
safe_margin = 50
fire_rate = 300  # Milliseconds
last_shot = 0
player_angle = 0

# Main game loop
if __name__ == "__main__":
    main_menu(screen)

running = True
pygame.time.set_timer(pygame.USEREVENT, wave_interval)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            for _ in range(5):  # Spawn a wave of enemies
                enemies.append(spawn_enemy())

    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    if keys[pygame.K_w]:
        move_y = -1
    if keys[pygame.K_s]:
        move_y = 1
    if keys[pygame.K_a]:
        move_x = -1
    if keys[pygame.K_d]:
        move_x = 1

    if move_x != 0 or move_y != 0:
        magnitude = math.sqrt(move_x**2 + move_y**2)
        move_x /= magnitude
        move_y /= magnitude
        player_angle = math.degrees(math.atan2(-move_y, move_x))

    player_pos[0] += move_x * player_speed
    player_pos[1] += move_y * player_speed

    # Automatic fire
    if pygame.time.get_ticks() - last_shot >= fire_rate:
        last_shot = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_x = mouse_x + camera_offset[0]
        target_y = mouse_y + camera_offset[1]
        dx = target_x - player_pos[0]
        dy = target_y - player_pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            direction = (dx / distance, dy / distance)
            bullet_rect = pygame.Rect(player_pos[0], player_pos[1], 10, 10)
            bullets.append({"rect": bullet_rect, "direction": direction})

    camera_offset[0] = player_pos[0] - WIDTH // 2
    camera_offset[1] = player_pos[1] - HEIGHT // 2

    screen.fill(BLACK)
    draw_background()

    rotated_player = pygame.transform.rotate(player_img, player_angle)
    player_rect = rotated_player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(rotated_player, player_rect.topleft)

    # Update bullets
    for bullet in bullets[:]:
        bullet["rect"].x += bullet["direction"][0] * 10
        bullet["rect"].y += bullet["direction"][1] * 10
        bullet_screen_x = bullet["rect"].x - camera_offset[0]
        bullet_screen_y = bullet["rect"].y - camera_offset[1]
        screen.blit(bullet_img, (bullet_screen_x, bullet_screen_y))

        # Check for collision with enemies
        for enemy in enemies[:]:
            if bullet["rect"].colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Update enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_frame_time >= enemy_frame_delay:
        enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)
        last_frame_time = current_time

    for enemy in enemies[:]:
        move_towards(enemy, player_pos, enemy_speed)
        enemy_screen_x = enemy.x - camera_offset[0]
        enemy_screen_y = enemy.y - camera_offset[1]
        screen.blit(enemy_frames[enemy_frame_index], (enemy_screen_x, enemy_screen_y))

        # Check for collision with player
        if enemy.colliderect(player_rect):
            enemies.remove(enemy)
            player_health -= 1  # Enemy damages the player on collision

    draw_text(f"Health: {player_health}", 10, 10)

    if player_health <= 0:
        draw_text("Game Over!", WIDTH // 2 - 100, HEIGHT // 2, RED)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
