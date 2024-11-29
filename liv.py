import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 704, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("liv")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
clock = pygame.time.Clock()
FPS = 60
player_speed = 5
bullet_speed = 7
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

# Player setup
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 30
player_health = 10
player_angle = 0  # Angle the player is facing

# Bullet list
bullets = []

# Enemy list
enemies = []

# Abilities
fire_rate = 120  # Frames between shots
last_shot = 0

# Fonts
font = pygame.font.SysFont(None, 36)

# Functions
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def spawn_enemy():
    """Spawns an enemy at a random edge of the screen."""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH)
        y = -20
    elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT + 20
    elif side == "left":
        x = -20
        y = random.randint(0, HEIGHT)
    else:  # "right"
        x = WIDTH + 20
        y = random.randint(0, HEIGHT)
    return pygame.Rect(x, y, 20, 20)

def move_towards(rect, target, speed):
    """Move a rectangle towards a target at a given speed."""
    dx, dy = target[0] - rect.x, target[1] - rect.y
    dist = math.sqrt(dx**2 + dy**2)
    if dist != 0:
        rect.x += int(dx / dist * speed)
        rect.y += int(dy / dist * speed)

# Main game loop
running = True
pygame.time.set_timer(pygame.USEREVENT, wave_interval)
while running:

    screen.blit(background_img, (0, 0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            # Spawn a wave of enemies
            for _ in range(5):
                enemies.append(spawn_enemy())

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Update player angle to face the mouse cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx, dy = mouse_x - player_pos[0], mouse_y - player_pos[1]
    player_angle = math.degrees(math.atan2(-dy, dx))  # Negative dy to correct direction

    # Shooting bullets
    if pygame.time.get_ticks() - last_shot > fire_rate:
        last_shot = pygame.time.get_ticks()
        # Create bullet heading toward the mouse cursor
        angle_rad = math.radians(player_angle)
        bullet_dx = math.cos(angle_rad) * bullet_speed
        bullet_dy = -math.sin(angle_rad) * bullet_speed
        bullets.append({
            "rect": pygame.Rect(player_pos[0], player_pos[1], 10, 10),
            "dx": bullet_dx,
            "dy": bullet_dy
        })

    # Move bullets
    for bullet in bullets[:]:
        bullet["rect"].x += bullet["dx"]
        bullet["rect"].y += bullet["dy"]
        if bullet["rect"].bottom < 0 or bullet["rect"].top > HEIGHT or \
           bullet["rect"].right < 0 or bullet["rect"].left > WIDTH:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        move_towards(enemy, player_pos, enemy_speed)
        # Check collision with player
        if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(enemy):
            player_health -= 1
            enemies.remove(enemy)
        # Check collision with bullets
        for bullet in bullets[:]:
            if enemy.colliderect(bullet["rect"]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Draw player (rotated to face the mouse)
    rotated_player = pygame.transform.rotate(player_img, player_angle)
    player_rect = rotated_player.get_rect(center=(player_pos[0], player_pos[1]))
    screen.blit(rotated_player, player_rect.topleft)

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_img, bullet["rect"].topleft)

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_img, enemy.topleft)

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
