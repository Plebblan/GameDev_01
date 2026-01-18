# Base resolution (DO NOT change at runtime)
BASE_WIDTH = 640
BASE_HEIGHT = 360

# Default window resolution (will be overwritten by menu)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

# Frame rate
FPS = 60

# Gameplay
MOLE_SIZE = 100
MOLE_SHOW_TIME = 800  # ms

def scale_x(x):
    return int(x * SCREEN_WIDTH / BASE_WIDTH)

def scale_y(y):
    return int(y * SCREEN_HEIGHT / BASE_HEIGHT)