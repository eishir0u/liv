import pygame

# Game Set up
WIDTH = 1280
HEIGHT = 720
FPS = 60
safe_margin = 50  # Allows a small buffer for bullets outside the screen

# Game variables
enemy_speed = 2
wave_interval = 5000  # Time between waves (ms)

# Player Values
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 50
player_health = 10
player_angle = 0  # Initial angle the player is facing (default: 0 degrees)
player_speed = 2
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

# Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("liv")

# Sprite setup
# Load sprites
background_img = pygame.image.load("Grass_Sample.png").convert()
player_img = pygame.image.load("gigi.jpg").convert_alpha()  # Replace with your sprite file
player_img = pygame.transform.scale(player_img, (30, 30))   # Resize as needed
bullet_img = pygame.image.load("gigi.jpg").convert_alpha()  # Replace with your sprite file
bullet_img = pygame.transform.scale(bullet_img, (10, 10))   # Resize as needed
enemy_img = pygame.image.load("gigi.jpg").convert_alpha()   # Replace with your sprite file
enemy_img = pygame.transform.scale(enemy_img, (20, 20))     # Resize as needed

# Camera setup
camera_offset = [0, 0]  # Offset of the camera
background_width, background_height = background_img.get_width(), background_img.get_height()