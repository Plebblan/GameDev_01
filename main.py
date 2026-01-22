import os
import pygame
import random
import threading
from settings import *
from menu import *
from classes import *
from fog_particles import *
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((640, 360))
(chosen_width, chosen_height), difficulty = menu(screen)
screen = pygame.display.set_mode((chosen_width, chosen_height))
pygame.display.set_caption("Zombie Whacker")
clock = pygame.time.Clock()
font = pygame.font.Font("assets/font/Brianne_s_hand.ttf", 36)
text_surface = font.render("Loading", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(chosen_width // 2, chosen_height // 2))

#Put loading screen here:
finish_loading = False
def load():
    global hammer, hm_hitbox, pow, pow_timer, pow_pos, background, fog_images, fog_particles, fog_bound, groan_tracks, score, zomb, num, finish_loading

#preload sprites
zombie_scaled_size = BASE_SIZE * chosen_width / BASE_WIDTH
hammer_frame = load_hammer_frames("assets/image/hammer",size=(BASE_HAMMER * chosen_width/BASE_WIDTH,BASE_HAMMER * chosen_width/BASE_WIDTH))
zombie_mov_frame = load_zombie_frames("assets/image/basic","move", zombie_scaled_size)
zombie_die_frame = load_zombie_frames("assets/image/basic","die", zombie_scaled_size)

dancer_mov_frame = load_zombie_frames("assets/image/dancer","move", zombie_scaled_size)
dancer_die_frame = load_zombie_frames("assets/image/dancer","die", zombie_scaled_size)
creep_mov_frame = load_zombie_frames("assets/image/creep_backup","move", zombie_scaled_size)
creep_die_frame = load_zombie_frames("assets/image/creep_backup","die", zombie_scaled_size)

hammer = Hammer(hammer_frame,pygame.mouse.get_pos(), (BASE_HAMMER * chosen_width/BASE_WIDTH, BASE_HAMMER * chosen_width/BASE_WIDTH))
hm_hitbox = int(BASE_HITBOX * chosen_width / BASE_WIDTH)

#init pow effect
pow = pygame.image.load("assets/image/pow.png").convert_alpha()
pow = pygame.transform.smoothscale(
        pow,
        ((BASE_SIZE*0.7*chosen_width/640),
        (BASE_SIZE*0.7*chosen_width/640)))
pow = tint_add(pow, (200, 170, 60))
pow_timer = 0
pow_pos = (0, 0)

pygame.mouse.set_visible(False)

# Load fog
fog_images = [
    pygame.image.load(f"assets/image/fog/fog_{i}.png").convert_alpha()
    for i in range(1, 9)
]
fog_particles,fog_bound = create_fog_wall(fog_images,chosen_width,chosen_height)

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

zomb = [Zombie(zombie_mov_frame,zombie_die_frame,line=1, resolution=(chosen_width, chosen_height)),
        Zombie(zombie_mov_frame,zombie_die_frame,line=2, resolution=(chosen_width, chosen_height)),
        Zombie(zombie_mov_frame,zombie_die_frame,line=3, resolution=(chosen_width, chosen_height)),
        Zombie(zombie_mov_frame,zombie_die_frame,line=4, resolution=(chosen_width, chosen_height)),
        Zombie(zombie_mov_frame,zombie_die_frame,line=5, resolution=(chosen_width, chosen_height)),
        Dancer(dancer_mov_frame,dancer_die_frame,creep_mov_frame,creep_die_frame,line=3, resolution=(chosen_width, chosen_height))]

num = 0



# Load background
background = pygame.image.load(
    "assets/image/background.png"
).convert()
background = pygame.transform.scale(background, (chosen_width, chosen_height))

#Signal loading screen ready to play
finish_loading = True

loading = threading.Thread(target=load)
loading.start()

screen.blit(background, (0, 0)) 
pygame.display.flip()

score = 0
# Pick and play random track
chosen_track = random.choice(music_tracks)
pygame.mixer.music.load(chosen_track)
pygame.mixer.music.play(-1)  # loop forever
pygame.mixer.music.set_volume(0.5)

# Main loop
running = True
health = 5
while running:
    if not finish_loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #loading screen
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(60)
        continue
    if health == 0:
        #display end screen
        end_surface = pygame.image.load("assets/image/menu.png").convert_alpha()
        tb_w, tb_h = end_surface.get_size()
        end_surface = pygame.transform.smoothscale(
            end_surface,
            (int(tb_w * TEXTBOX_SCALE * chosen_width / BASE_WIDTH), int(tb_h * TEXTBOX_SCALE * chosen_width / BASE_WIDTH))
        )
        end_rect = end_surface.get_rect(center=(chosen_width // 2, chosen_height // 2))
        screen.blit(end_surface, end_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    health = 5
                    #reset zombies' state
        pygame.display.flip()
        clock.tick(60)
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.change_state()
            mouse_pos = event.pos
            for zom in zomb:
                if (zom.moving >= 0 or isinstance (zom, Dancer)) and zom.is_hit(mouse_pos, BASE_HITBOX * chosen_width/BASE_WIDTH):
                    score += 1
                    hammer.bonk.play()
                    pow_timer = 6
                    pow_pos = mouse_pos
                    if not isinstance (zom, Dancer):
                        num += zom.change_state("die")
                    elif zom.moving == -1:
                        num -= 1
                    print(f"Hit! Score: {score}")
    # Draw background every frame
    screen.blit(background, (0, 0))

    #play random groans
    if num > 0:
        magic = random.randint(1, 360)
        if magic == 1:
            chosen_groan = random.choice(groan_tracks)
            chosen_groan.play()
    for z in zomb:
        num += z.spawn(resolution=(chosen_width, chosen_height))
        hehe = z.move(-0.5, 0)
        if hehe is not None and hehe < 0:
            num -= 1
            score += hehe if isinstance(z, Dancer) else -1
            print(f"U got invaded! Score: {score}")
            health -= 1
            if health <= 0: 
                continue
        z.draw(screen)
    #draw fog screen
    for fog in fog_particles:
        fog.update()
        fog.draw(screen,fog_bound)

    hammer.move(pygame.mouse.get_pos())
    hammer.draw(screen)

    if pow_timer > 0:
        rect = pow.get_rect(center=pow_pos)
        screen.blit(pow, rect)
        pow_timer -= 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()