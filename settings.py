import pygame
from pygame import mixer

# Game Set up
WIDTH = 1280
HEIGHT = 720
FPS = 60
safe_margin = 50  # Allows a small buffer for bullets outside the screen

# Game variables
enemy_speed = 2
wave_interval = 5000  # Time between waves (ms)
base_wave_size = 5  # Initial wave size
scale_factor = 2  # Enemies added per minute
max_wave_size = 50  # Maximum enemies in a wave

def calculate_wave_size(base_wave_size, elapsed_time, scale_factor=2, max_wave_size=50):
    wave_size = base_wave_size + (elapsed_time // 60000) * scale_factor
    return min(wave_size, max_wave_size)

# Player Values
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 100
exp_orbs = []  # List for EXP orbs
player_max_health = 10
player_health = 10
player_angle = 0  # Initial angle the player is facing (default: 0 degrees)
player_speed = 2
bullet_speed = 5
fire_rate = 500  # Frames between shots
last_shot = 0

# Level system variables
player_level = 1
player_exp = 0
exp_to_next_level = 100  # EXP required to level up

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Abilities

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
player_img = pygame.image.load("player.png").convert_alpha()  # Replace with your sprite file
player_img = pygame.transform.scale(player_img, (60, 60))   # Resize as needed
bullet_img = pygame.image.load("bullet.png").convert_alpha()  # Replace with your sprite file
bullet_img = pygame.transform.scale(bullet_img, (30, 30))   # Resize as needed
# enemy_img = pygame.image.load("gigi.jpg").convert_alpha()   # Replace with your sprite file
# enemy_img = pygame.transform.scale(enemy_img, (20, 20))     # Resize as needed

# Camera setup
camera_offset = [0, 0]  # Offset of the camera
background_width, background_height = background_img.get_width(), background_img.get_height()

# Background Music
pygame.mixer.init()
my_sound = pygame.mixer.Sound('cirnos_theme_remix.wav')
my_sound.play(-1)
my_sound.set_volume(0.75)