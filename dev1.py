import pygame
import random
import math
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
player_img = pygame.image.load("gigi.jpg").convert_alpha()  # Replace with your sprite file
player_img = pygame.transform.scale(player_img, (30, 30))   # Resize as needed
bullet_img = pygame.image.load("gigi.jpg").convert_alpha()  # Replace with your sprite file
bullet_img = pygame.transform.scale(bullet_img, (10, 10))   # Resize as needed
enemy_img = pygame.image.load("gigi.jpg").convert_alpha()   # Replace with your sprite file
enemy_img = pygame.transform.scale(enemy_img, (20, 20))     # Resize as needed

# Fonts
font = pygame.font.SysFont(None, 36)

# Functions
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# def spawn_enemy():
def spawn_enemy():
    """Spawns an enemy at a random edge of the world (not screen)."""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH) + camera_offset[0]
        y = -20 + camera_offset[1]
    elif side == "bottom":
        x = random.randint(0, WIDTH) + camera_offset[0]
        y = HEIGHT + 20 + camera_offset[1]
    elif side == "left":
        x = -20 + camera_offset[0]
        y = random.randint(0, HEIGHT) + camera_offset[1]
    else:  # "right"
        x = WIDTH + 20 + camera_offset[0]
        y = random.randint(0, HEIGHT) + camera_offset[1]
    return pygame.Rect(x, y, 20, 20)


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
    # Ensure integer division for start_x and start_y
    start_x = int(camera_offset[0] // background_width)
    start_y = int(camera_offset[1] // background_height)

    # Ensure all calculations use integers
    for x in range(start_x, start_x + WIDTH // background_width + 2):
        for y in range(start_y, start_y + HEIGHT // background_height + 2):
            tile_x = x * background_width - int(camera_offset[0])
            tile_y = y * background_height - int(camera_offset[1])
            screen.blit(background_img, (tile_x, tile_y))

# Main game loop
if __name__ == "__main__":
    # Display the main menu first
    main_menu(screen)
running = True
pygame.time.set_timer(pygame.USEREVENT, wave_interval)
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            for _ in range(5):  # Spawn a wave of enemies
                enemies.append(spawn_enemy())

    # Player movement
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

    # Normalize diagonal movement
    if move_x != 0 or move_y != 0:
        magnitude = math.sqrt(move_x**2 + move_y**2)
        move_x /= magnitude
        move_y /= magnitude
        
        if move_x != 0 or move_y != 0:
            player_angle = math.degrees(math.atan2(-move_y, move_x))  # Negative because screen y-axis is inverted

    # Apply movement
    player_pos[0] += move_x * player_speed
    player_pos[1] += move_y * player_speed

    # Shooting bullets
    if pygame.time.get_ticks() - last_shot >= fire_rate:
        last_shot = pygame.time.get_ticks()

        # Get mouse position relative to the screen
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse position to world coordinates using the camera offset
        target_x = mouse_x + camera_offset[0]
        target_y = mouse_y + camera_offset[1]

        # Calculate direction from player (in world coordinates) to the target
        dx = target_x - player_pos[0]
        dy = target_y - player_pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            direction = (dx / distance, dy / distance)  # Normalize direction
            bullet_rect = pygame.Rect(player_pos[0], player_pos[1], 10, 10)  # Spawn bullet in world coordinates
            bullets.append({"rect": bullet_rect, "direction": direction})
    
    # Update camera offset
    camera_offset[0] = player_pos[0] - WIDTH // 2
    camera_offset[1] = player_pos[1] - HEIGHT // 2


    # Clear screen and draw background
    screen.fill(BLACK)
    draw_background()

    # Draw player
    rotated_player = pygame.transform.rotate(player_img, player_angle)
    player_rect = rotated_player.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centered on screen
    screen.blit(rotated_player, player_rect.topleft)

    # Update bullets
    for bullet in bullets[:]:
        bullet["rect"].x += bullet["direction"][0] * bullet_speed
        bullet["rect"].y += bullet["direction"][1] * bullet_speed

    # Remove bullets outside the camera's view
    camera_left = camera_offset[0] - safe_margin
    camera_top = camera_offset[1] - safe_margin
    camera_right = camera_offset[0] + WIDTH + safe_margin
    camera_bottom = camera_offset[1] + HEIGHT + safe_margin

    for bullet in bullets[:]:
        bullet_x = bullet["rect"].x
        bullet_y = bullet["rect"].y

        if not (camera_left <= bullet_x <= camera_right and camera_top <= bullet_y <= camera_bottom):
            bullets.remove(bullet)

    # Adjust for camera offset when drawing bullets
    for bullet in bullets:
        bullet_screen_x = bullet["rect"].x - camera_offset[0]
        bullet_screen_y = bullet["rect"].y - camera_offset[1]
        screen.blit(bullet_img, (bullet_screen_x, bullet_screen_y))

        
    # Move and update enemies
    for enemy in enemies:
        move_towards(enemy, player_pos, enemy_speed)

        # Adjust for camera offset and draw
        enemy_screen_x = enemy.x - camera_offset[0]
        enemy_screen_y = enemy.y - camera_offset[1]
        screen.blit(enemy_img, (enemy_screen_x, enemy_screen_y))

        # Check collision with player
        if enemy.colliderect(player_rect):
            enemies.remove(enemy)
            player_health -= 1

    # Check for collisions between bullets and enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            # Only check nearby enemies (distance threshold)
            if abs(bullet["rect"].x - enemy.x) < 50 and abs(bullet["rect"].y - enemy.y) < 50:
                if bullet["rect"].colliderect(enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break  # Stop checking this bullet

            
    # Display player health
    draw_text(f"Health: {player_health}", 10, 10)

    # End game if health is zero
    if player_health <= 0:
        draw_text("Game Over!", WIDTH // 2 - 100, HEIGHT // 2, RED)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
