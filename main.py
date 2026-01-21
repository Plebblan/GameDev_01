import pygame
import random
from settings import *
from menu import menu
from zombie import *
from fog_particles import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((640, 360))
(chosen_width, chosen_height), difficulty = menu(screen)
screen = pygame.display.set_mode((chosen_width, chosen_height))
pygame.display.set_caption("Zombie Whacker")
clock = pygame.time.Clock()

hammer = Hammer(pygame.mouse.get_pos(), (40 * chosen_width/BASE_WIDTH, 40 * chosen_width/BASE_WIDTH))

pygame.mouse.set_visible(False)

# Load background
background = pygame.image.load(
    "assets/image/background.png"
).convert()
background = pygame.transform.scale(background, (chosen_width, chosen_height))
screen.blit(background, (0, 0)) 
pygame.display.flip()

# Load fog
fog_images = [
    pygame.image.load(f"assets/image/fog/fog_{i}.png").convert_alpha()
    for i in range(1, 9)
]
fog_particles = []
lanes = BASE_Y

for lane_y in lanes:
    for i in range(5):
        x = int(chosen_width * (FOG_LEFT + (i + 0.5) * (1 - FOG_LEFT) / 5))
        img = random.choice(fog_images)

        scale = random.uniform(0.7, 1.2)
        img = pygame.transform.smoothscale(
            img,
            (int(img.get_width() * scale),
             int(img.get_height() * scale))
        )

        fog_particles.append(FogParticle(x, lane_y, img))

# Music tracks
music_tracks = [
    "assets/sound/Tracks/21. Loonboon IN-GAME.ogg",
    "assets/sound/Tracks/25. Ultimate Battle IN-GAME.ogg",
    "assets/sound/Tracks/29. Brainiac Maniac IN-GAME.ogg"
]
groan_tracks = [
    pygame.mixer.Sound("assets/sound/Effect/groan.ogg"),
    pygame.mixer.Sound("assets/sound/Effect/groan2.ogg"),
    pygame.mixer.Sound("assets/sound/Effect/groan3.ogg"),
    pygame.mixer.Sound("assets/sound/Effect/groan4.ogg"),
    pygame.mixer.Sound("assets/sound/Effect/groan5.ogg"),
    pygame.mixer.Sound("assets/sound/Effect/groan6.ogg")
]

score = 0
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
num = 0
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.change_state()
            mouse_pos = event.pos
            for zom in zomb:
                if zom.moving >= 0 and zom.is_hit(mouse_pos, BASE_HITBOX * chosen_width/BASE_WIDTH):
                    hammer.bonk.play()
                    score += 1
                    num += zom.change_state("die")
                    print(f"Hit! Score: {score}")
    # Draw background every frame
    screen.blit(background, (0, 0))

    #play random groans
    if num > 0:
        magic = random.randint(1, 75)
        if magic == 1:
            chosen_groan = random.choice(groan_tracks)
            chosen_groan.play()
    for z in zomb:
        num += z.spawn(resolution=(chosen_width, chosen_height))
        z.move(-0.5, 0)
        z.draw(screen)
    #draw fog screen
    for fog in fog_particles:
        fog.update()
        fog.draw(screen)

    hammer.move(pygame.mouse.get_pos())
    hammer.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()