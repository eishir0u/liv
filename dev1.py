import pygame
import math
from menu import main_menu
from settings import *
from enemy_spawner import *
from skills import skill_selection

# Initialize Pygame
pygame.init()

# set clock for fps
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# Functions
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def move_towards(rect, target, speed):
    """Move a rectangle towards a target at a given speed with normalized diagonal movement."""
    dx, dy = target[0] - rect.x, target[1] - rect.y
    dist = math.sqrt(dx**2 + dy**2)
    if dist != 0:
        dx /= dist  # Normalize dx
        dy /= dist  # Normalize dy
    rect.x += int(dx * speed)
    rect.y += int(dy * speed)

# Infinite background tiling
def draw_background():
    start_x = int(camera_offset[0] // background_width)
    start_y = int(camera_offset[1] // background_height)

    for x in range(start_x, start_x + WIDTH // background_width + 2):
        for y in range(start_y, start_y + HEIGHT // background_height + 2):
            tile_x = x * background_width - int(camera_offset[0])
            tile_y = y * background_height - int(camera_offset[1])
            screen.blit(background_img, (tile_x, tile_y))

def spawn_exp_orb(position):
    """Creates an EXP orb at the given position."""
    orb = {
        "rect": pygame.Rect(position[0], position[1], 10, 10),  # Size of the orb
        "color": (255, 255, 0)  # Yellow for visibility
    }
    exp_orbs.append(orb)

facing_right = True  # Track the direction the player is facing

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
        facing_right = False  # Face left
    if keys[pygame.K_d]:
        move_x = 1
        facing_right = True  # Face right

    if move_x != 0 or move_y != 0:
        magnitude = math.sqrt(move_x**2 + move_y**2)
        move_x /= magnitude
        move_y /= magnitude


    player_pos[0] += move_x * player_speed
    player_pos[1] += move_y * player_speed

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

    # # Define the player rect for collision detection
    player_rect = pygame.Rect(
        player_pos[0] - player_img.get_width() // 2,
        player_pos[1] - player_img.get_height() // 2,
        player_img.get_width(),
        player_img.get_height(),
    )


    # Render the player
    player_render = player_img
    if not facing_right:
        player_render = pygame.transform.flip(player_img, True, False)  # Flip horizontally
    player_render_rect = player_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(player_render, player_render_rect.topleft)


    for bullet in bullets[:]:
        bullet["rect"].x += bullet["direction"][0] * 10
        bullet["rect"].y += bullet["direction"][1] * 10
        bullet_screen_x = bullet["rect"].x - camera_offset[0]
        bullet_screen_y = bullet["rect"].y - camera_offset[1]
        screen.blit(bullet_img, (bullet_screen_x, bullet_screen_y))

        for enemy in enemies[:]:
            if bullet["rect"].colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)

                # Spawn an EXP orb at the enemy's position
                orb_rect = pygame.Rect(enemy.x, enemy.y, 10, 10)
                exp_orbs.append({"rect": orb_rect, "color": (0, 255, 0)})
                break

    current_time = pygame.time.get_ticks()
    if current_time - last_frame_time >= enemy_frame_delay:
        enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)
        last_frame_time = current_time

    for enemy in enemies[:]:  # Use a copy of the list to avoid iteration issues when removing enemies
        move_towards(enemy, player_pos, enemy_speed)
        enemy_screen_x = enemy.x - camera_offset[0]
        enemy_screen_y = enemy.y - camera_offset[1]
        screen.blit(enemy_frames[enemy_frame_index], (enemy_screen_x, enemy_screen_y))

        # Check collision with the player
        if enemy.colliderect(player_rect):
            enemies.remove(enemy)  # Remove enemy
            player_health -= 1     # Decrement player health
            print(f"Player hit! Health: {player_health}")  # Debugging line

    # Draw Exp Orb
    for orb in exp_orbs[:]:  # Iterate through a copy of the list
        orb_screen_x = orb["rect"].x - camera_offset[0]
        orb_screen_y = orb["rect"].y - camera_offset[1]
        pygame.draw.ellipse(screen, (0, 0, 255), (orb_screen_x - 2, orb_screen_y - 2, 14, 14))
        pygame.draw.ellipse(screen, orb["color"], (orb_screen_x, orb_screen_y, 10, 10))

        # Check if player collects the orb
        if player_rect.colliderect(orb["rect"]):
            exp_orbs.remove(orb)  # Remove the orb
            player_exp += 10      # Increment player EXP
            print(f"EXP collected! Current EXP: {player_exp}")  # Debugging line

    # Handle leveling up
    if player_exp >= player_level * 50:  # Example leveling curve
        player_exp -= player_level * 50
        player_level += 1

        # Call the skill selection screen
        chosen_skill = skill_selection(screen, font)

        # Apply the selected skill
        if chosen_skill == "Speed":
            player_speed += 1
        elif chosen_skill == "Attack Speed":
            fire_rate = max(100, fire_rate - 50)  # Reduce fire rate (faster attacks)
        elif chosen_skill == "Health":
            player_health += 2

    # Display stats
    draw_text(f"Health: {player_health}", 10, 10)
    draw_text(f"Level: {player_level}", 10, 40)
    draw_text(f"EXP: {player_exp}/{player_level * 50}", 10, 70)

    if player_health <= 0:
        draw_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
