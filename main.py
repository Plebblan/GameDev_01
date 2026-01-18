import pygame
import random
from settings import *
from menu import menu
from zombie import Zombie

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((640, 360))
(chosen_width, chosen_height), difficulty = menu(screen)
screen = pygame.display.set_mode((chosen_width, chosen_height))
pygame.display.set_caption("Zombie Whacker")
clock = pygame.time.Clock()

# Load background
background = pygame.image.load(
    "assets/image/background.png"
).convert()
background = pygame.transform.scale(background, (chosen_width, chosen_height))

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

zomb = [Zombie(line=1, resolution=(chosen_width, chosen_height)),
        Zombie(line=2, resolution=(chosen_width, chosen_height)),
        Zombie(line=3, resolution=(chosen_width, chosen_height)),
        Zombie(line=4, resolution=(chosen_width, chosen_height)),
        Zombie(line=5, resolution=(chosen_width, chosen_height))]
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #get mouse position
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse clicked at: {mouse_pos}")

    # Draw background every frame
    screen.blit(background, (0, 0))

    for z in zomb:
        z.move(-0.5, 0)
        z.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()