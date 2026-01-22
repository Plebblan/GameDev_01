# Base resolution (DO NOT change at runtime)
BASE_WIDTH = 640
BASE_HEIGHT = 360
BASE_Y = [130, 178, 225, 270, 320]
BASE_X = 518
BASE_SIZE = 60
BASE_HAMMER = 40
BASE_HITBOX = 30
HURT_BASE = 110
HEALTH_COORD = (140, 70)
BASE_HEALTH = 100

# Default window resolution (will be overwritten by menu)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

#Fog bounds
FOG_LEFT = 0.79
FOG_RIGHT = 1.10
FOG_X = 120

# Frame rate
FPS = 60

def scale_x(x):
    return int(x * SCREEN_WIDTH / BASE_WIDTH)

def scale_y(y):
    return int(y * SCREEN_HEIGHT / BASE_HEIGHT)