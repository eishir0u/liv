# Game Set up
WIDTH = 1280
HEIGHT = 720
FPS = 60
safe_margin = 50  # Allows a small buffer for bullets outside the screen


# Player Values
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 50
player_health = 10
player_angle = 0  # Initial angle the player is facing (default: 0 degrees)
player_speed = 5
bullet_speed = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Abilities
fire_rate = 360  # Frames between shots
last_shot = 0

# Bullet list
bullets = []

# Enemy list
enemies = []