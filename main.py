import pygame
import random
from settings import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack Clicker")
clock = pygame.time.Clock()

# Load background
background = pygame.image.load(
    "assets/image/background.png"
).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Music tracks
music_tracks = [
    "assets/sound/Tracks/21. Loonboon IN-GAME.mp3",
    "assets/sound/Tracks/25. Ultimate Battle IN-GAME.mp3",
    "assets/sound/Tracks/29. Brainiac Maniac IN-GAME.mp3"
]

# Pick and play random track
chosen_track = random.choice(music_tracks)
pygame.mixer.music.load(chosen_track)
pygame.mixer.music.play(-1)  # loop forever
pygame.mixer.music.set_volume(0.5)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background every frame
    screen.blit(background, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()