import pygame
import math
from menu import main_menu
from settings import *
from enemy_spawner import *
from skills import skill_selection
from weapon_selection import weapon_selection
from map_selection import *
from pause_screen import *

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

def rotate_image(image, angle):
    """Rotate an image around its center."""
    return pygame.transform.rotate(image, -math.degrees(angle))

def draw_weapon_info(screen, weapon_name, x, y):
    """Display current weapon info."""
    weapon_text = f"Weapon: {weapon_name}"
    weapon_surface = font.render(weapon_text, True, WHITE)
    screen.blit(weapon_surface, (x, y))

def move_towards(enemy, target, speed):
    """Move an enemy (dictionary with a rect) towards a target at a given speed."""
    rect = enemy["rect"]  # Extract the rect from the dictionary
    dx, dy = target[0] - rect.x, target[1] - rect.y
    dist = math.sqrt(dx**2 + dy**2)
    if dist != 0:
        dx /= dist  # Normalize dx
        dy /= dist  # Normalize dy
    rect.x += int(dx * speed)
    rect.y += int(dy * speed)
    
    # Update facing direction
    if dx > 0:
        enemy["facing_right"] = True
    elif dx < 0:
        enemy["facing_right"] = False

# Infinite background tiling
def draw_background():
    start_x = int(camera_offset[0] // background_width)
    start_y = int(camera_offset[1] // background_height)

    for x in range(start_x, start_x + WIDTH // background_width + 2):
        for y in range(start_y, start_y + HEIGHT // background_height + 2):
            tile_x = x * background_width - int(camera_offset[0])
            tile_y = y * background_height - int(camera_offset[1])
            screen.blit(background_img, (tile_x, tile_y))

def draw_health_bar(x, y, width, height, current_health, max_health, border_color=WHITE, fill_color=RED, text_color=WHITE):
    """Draw a static-sized health bar with a health label inside."""
    # Draw the border
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)  # 2px border
    # Calculate the fill width
    fill_width = int((current_health / max_health) * (width - 4))  # Subtract 4 for border
    # Draw the filled portion
    pygame.draw.rect(screen, fill_color, (x + 2, y + 2, fill_width, height - 4))  # Adjust for border
    
    # Add health text inside the bar
    health_font = pygame.font.SysFont(None, 24)
    health_text = f"{current_health}/{max_health}"
    text_surface = health_font.render(health_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def draw_exp_bar(x, y, width, height, current_exp, max_exp, level, border_color=WHITE, fill_color=(0, 255, 0)):
    """Draw an EXP bar with level text inside."""
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)  # Draw the border
    fill_width = int((current_exp / max_exp) * (width - 4))  # Calculate fill width
    pygame.draw.rect(screen, fill_color, (x + 2, y + 2, fill_width, height - 4))  # Draw the fill

    # Draw level text
    level_font = pygame.font.SysFont(None, 24)  # Smaller font size
    level_text = f"Level {level}"
    text_surface = level_font.render(level_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def calculate_enemy_speed(base_speed, elapsed_time, scale_factor=0.02):
    return base_speed + (elapsed_time // 1000) * scale_factor

    
facing_right = True  # Track the direction the player is facing

#timer
level_duration = 10 * 60 * 1000  # 10 minutes in milliseconds
start_time = pygame.time.get_ticks()  # Record the starting time

paused = False

# Main game loop
if __name__ == "__main__":
    main_menu(screen)
    selected_weapon = weapon_selection(screen, font)  # Call weapon selection
    print(f"Selected Weapon: {selected_weapon}")  # Debugging/logging

    selected_map = map_selection(screen, font)  # Call map selection
    print(f"Selected Map: {selected_map}")  # Debugging/logging

     # Load the selected map's background
    if selected_map == "Grasslands":
        background_img = pygame.image.load("asset/Grass_Sample.png").convert()
    elif selected_map == "Desert":
        background_img = pygame.image.load("asset/desert.jpg").convert()
    elif selected_map == "Dungeon":
        background_img = pygame.image.load("asset/dungeon.jpeg").convert()

    background_width, background_height = background_img.get_width(), background_img.get_height()
    
    # Apply weapon attributes
    fire_rate = weapon_stats[selected_weapon]["fire_rate"]
    bullet_damage = weapon_stats[selected_weapon]["damage"]
    bullet_spread = weapon_stats[selected_weapon]["spread"]
    bullet_count = weapon_stats[selected_weapon]["bullet_count"]


running = True
pygame.time.set_timer(pygame.USEREVENT, wave_interval)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Detect Escape key to pause the game
                result = pause_screen(screen, font)  # Trigger pause screen
                if result == "menu":  # If Return to Menu is chosen
                    main_menu(screen)  # Return to main menu
                    break  # Break out of the current game loop to go back to menu
                elif result == "resume":  # If Resume is chosen
                    paused = False  # Resume the game
            
            
        if event.type == pygame.USEREVENT:  # Wave spawn event
            elapsed_time = pygame.time.get_ticks() - start_time  # Time elapsed since the game started
            wave_size = calculate_wave_size(base_wave_size, elapsed_time, scale_factor, max_wave_size)
        
            for _ in range(wave_size):  # Spawn enemies based on the wave size
                enemies.append(spawn_enemy(elapsed_time))
                
    if not paused:
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

        # Fire bullets based on selected weapon
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
                angle = math.atan2(dy, dx)  # Calculate the angle for rotation
                
                # Fire bullets based on weapon attributes
                for _ in range(bullet_count):
                    spread_angle = random.uniform(-bullet_spread, bullet_spread)
                    spread_dx = (
                        direction[0] * math.cos(math.radians(spread_angle))
                        - direction[1] * math.sin(math.radians(spread_angle))
                    )
                    spread_dy = (
                        direction[0] * math.sin(math.radians(spread_angle))
                        + direction[1] * math.cos(math.radians(spread_angle))
                    )
                    bullet_rect = pygame.Rect(player_pos[0], player_pos[1], 10, 10)
                    bullets.append({
                        "rect": bullet_rect,
                        "direction": (spread_dx, spread_dy),
                        "damage": bullet_damage,
                        "angle": angle + math.radians(spread_angle)  # Store the angle with spread applied
                    })

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


    bullets_to_remove = []

    for bullet in bullets:
        # Move the bullet
        bullet["rect"].x += bullet["direction"][0] * bullet_speed
        bullet["rect"].y += bullet["direction"][1] * bullet_speed

        # Draw the bullet on the screen
        bullet_screen_x = bullet["rect"].x - camera_offset[0]
        bullet_screen_y = bullet["rect"].y - camera_offset[1]
        rotated_bullet = rotate_image(bullet_img, bullet["angle"])  # Rotate based on the angle
        rotated_rect = rotated_bullet.get_rect(center=(bullet_screen_x + 5, bullet_screen_y + 5))  # Adjust center
        screen.blit(rotated_bullet, rotated_rect.topleft)
        for enemy in enemies[:]:
            for enemy in enemies:
                if bullet["rect"].colliderect(enemy["rect"]):
                    #print(f"Bullet hit! Damage: {bullet['damage']}, Enemy health before: {enemy['health']}")
                    enemy["health"] -= bullet["damage"]
                    #print(f"Enemy health after: {enemy['health']}")
                    if enemy["health"] <= 0:
                        #print(f"Enemy destroyed! Remaining health: {enemy['health']}")
                        enemies.remove(enemy)
                        player_exp += enemy.get("exp", 10)  # Award EXP when killing the enemy
                    bullets_to_remove.append(bullet)  # Mark bullet for removal
                    break
                
        # Check if the bullet is off-screen (depending on screen width/height)
        if (bullet["rect"].x < camera_offset[0] or bullet["rect"].x > camera_offset[0] + WIDTH or
        bullet["rect"].y < camera_offset[1] or bullet["rect"].y > camera_offset[1] + HEIGHT):
            bullets_to_remove.append(bullet)  # Mark bullet for removal

    # Remove bullets after the iteration
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    current_time = pygame.time.get_ticks()  # Current game time
    elapsed_time = current_time - start_time  # Time elapsed since level start
    time_remaining = max(0, level_duration - elapsed_time)  # Remaining time

    # Display the timer on the screen
    minutes = time_remaining // 60000
    seconds = (time_remaining % 60000) // 1000
    timer_text = f"{minutes:02}:{seconds:02}"
    font = pygame.font.SysFont(None, 50)  # Adjust font size as needed
    timer_surface = font.render(timer_text, True, (255, 255, 255))
    timer_rect = timer_surface.get_rect(center=(WIDTH // 2, 30))
    screen.blit(timer_surface, timer_rect)

    # Dynamically calculate enemy speed
    current_enemy_speed = calculate_enemy_speed(enemy_speed, elapsed_time)

    # Use a copy of the list to avoid iteration issues when removing enemies
    for enemy in enemies[:]:
        move_towards(enemy, player_pos, enemy_speed)
        enemy_screen_x = enemy["rect"].x - camera_offset[0]
        enemy_screen_y = enemy["rect"].y - camera_offset[1]

        # Flip the sprite if the enemy is facing left
        current_frame = enemy_frames[enemy_frame_index]
        if not enemy["facing_right"]:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, (enemy_screen_x, enemy_screen_y))

        # Check collision with the player
        if enemy["rect"].colliderect(player_rect):
            enemies.remove(enemy)  # Remove enemy
            player_health -= 1     # Decrement player health
            print(f"Player hit! Health: {player_health}")  # Debugging line


    # Handle leveling up
    if player_exp >= player_level * 50:  # Example leveling curve
        player_exp -= player_level * 50
        player_level += 1

        # Call the skill selection screen
        chosen_skill = skill_selection(screen, font)

        # Apply the selected skill
        if chosen_skill == "Speed":
            player_speed += 0.5
        elif chosen_skill == "Attack Speed":
            fire_rate = max(100, fire_rate - 50)  # Reduce fire rate (faster attacks)
        elif chosen_skill == "Health":
            player_max_health += 2  # Increase max health
            player_health = player_max_health  # Refill health to the new max

    # Display stats
    draw_health_bar(10, 10, 200, 20, player_health, player_max_health)
    draw_exp_bar(10, 40, 200, 20, player_exp, player_level * 50, player_level)

    if player_health <= 0:
        draw_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED)
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False

    if time_remaining <= 0:
        font = pygame.font.SysFont(None, 80)
        complete_text = font.render("LEVEL COMPLETE!", True, (0, 255, 0))
        screen.blit(complete_text, (WIDTH // 2 - 200, HEIGHT // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)

    # Draw weapon info on HUD
    draw_weapon_info(screen, selected_weapon, 10, 70)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
