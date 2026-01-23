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
end_bg = pygame.image.load("assets/image/back.png").convert_alpha()
(chosen_width, chosen_height), difficulty = menu(screen,end_bg)
screen = pygame.display.set_mode((chosen_width, chosen_height))
pygame.display.set_caption("Zombie Whacker")
clock = pygame.time.Clock()
font = pygame.font.Font("assets/font/Brianne_s_hand.ttf", 36)
text_surface = font.render("Loading", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(chosen_width // 2, chosen_height // 2))
# Load background
background = pygame.image.load(
    "assets/image/background.png"
).convert()
background = pygame.transform.scale(background, (chosen_width, chosen_height))
# Load end screen
end_bg = pygame.transform.scale(end_bg,(chosen_width,chosen_height))
end_scale = 0.05      # start very small
end_alpha = 0        # invisible
state = "playing"

#dimming the background for loading + ending scenes
dim = pygame.Surface(background.get_size())
dim.set_alpha(150)
dim.fill((0, 0, 0))

end_surface = pygame.image.load("assets/image/YOULOSE.png").convert_alpha()
tb_w, tb_h = end_surface.get_size()
end_surface = pygame.transform.smoothscale(
    end_surface,
    (int(tb_w * 0.65 * TEXTBOX_SCALE * chosen_width / BASE_WIDTH), int(tb_h * 0.65 * TEXTBOX_SCALE * chosen_width / BASE_WIDTH))
)
end_rect = end_surface.get_rect(center=(chosen_width // 2, chosen_height // 2))

#loading procedure
finish_loading = False
def load():
    global hammer, hm_hitbox, pow, pow_timer, pow_pos, fog_images, fog_particles, fog_bound, groan_tracks, score, zomb, num, finish_loading, music_tracks, health_bar, health_coord
    global clock_img, clock_rect, start_time, clock_font, death_time, final_time
    #preload sprites
    zombie_scaled_size = BASE_SIZE * chosen_width / BASE_WIDTH
    hammer_frame = load_hammer_frames("assets/image/hammer",size=(BASE_HAMMER * chosen_width/BASE_WIDTH,BASE_HAMMER * chosen_width/BASE_WIDTH))
    zombie_mov_frame = load_zombie_frames("assets/image/basic","move", zombie_scaled_size)
    zombie_die_frame = load_zombie_frames("assets/image/basic","die", zombie_scaled_size)

    dancer_mov_frame = load_zombie_frames("assets/image/dancer","move", zombie_scaled_size)
    dancer_die_frame = load_zombie_frames("assets/image/dancer","die", zombie_scaled_size)
    creep_mov_frame = load_zombie_frames("assets/image/creep_backup","move", zombie_scaled_size)
    creep_die_frame = load_zombie_frames("assets/image/creep_backup","die", zombie_scaled_size)
    health_bar = load_hammer_frames("assets/image/healthbar", size=(BASE_HEALTH * chosen_width/BASE_WIDTH, BASE_HEALTH * chosen_width/BASE_WIDTH))
    health_coord = health_bar[0].get_rect(center=(HEALTH_COORD[0] * chosen_width / BASE_WIDTH, HEALTH_COORD[1] * chosen_width / BASE_WIDTH))

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

    # Load and record start timer
    clock_img = pygame.image.load("assets/image/clock.png").convert_alpha()
    cw, ch = clock_img.get_size()
    clock_img = pygame.transform.smoothscale(
        clock_img,
        (int(cw * 0.15 * chosen_width/640), int(ch * 0.15 * chosen_width/640))
    )
    clock_font_size = int(clock_img.get_height() * 0.24)
    clock_font = pygame.font.Font("assets/font/Brianne_s_hand.ttf", clock_font_size)

    clock_rect = clock_img.get_rect(
    topright=(chosen_width + clock_img.get_width()//6, -clock_img.get_height()//6)
    )

    start_time = pygame.time.get_ticks()

    # Pick and play random track
    chosen_track = random.choice(music_tracks)
    pygame.mixer.music.load(chosen_track)
    pygame.mixer.music.play(-1)  # loop forever
    pygame.mixer.music.set_volume(0.5)
    #Signal loading screen ready to play
    finish_loading = True

loading = threading.Thread(target=load)
loading.start()
score = 0

# Main loop
running = True
health = 5
while running:
    if not finish_loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #loading screen
        screen.blit(background, (0, 0))
        screen.blit(dim, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(60)
        continue
        
    if state != "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if state == "death_wait":
                    state = "score"

                elif state == "score":
                    # RESET GAME
                    state = "playing"
                    health = 5
                    score = 0
                    num = 0
                    start_time = pygame.time.get_ticks()
                    chosen_track = random.choice(music_tracks)
                    pygame.mixer.music.load(chosen_track)
                    pygame.mixer.music.play(-1)

                    #RESET ZOMBIES
                    for z in zomb:
                        z.reset()

        # DRAW STATES
        if state == "death_anim":
            screen.blit(background, (0, 0))
            screen.blit(dim, (0, 0))

            end_scale += (1 - end_scale) * 0.12
            end_alpha = min(255, end_alpha + 6)

            w = int(end_surface.get_width() * end_scale)
            h = int(end_surface.get_height() * end_scale)
            anim = pygame.transform.smoothscale(end_surface, (w, h))
            anim.set_alpha(end_alpha)
            rect = anim.get_rect(center=(chosen_width//2, chosen_height//2))
            screen.blit(anim, rect)

            if end_scale > 0.98:
                state = "death_wait"

        elif state == "death_wait":
            screen.blit(background, (0, 0))
            screen.blit(dim, (0, 0))
            screen.blit(end_surface, end_surface.get_rect(center=(chosen_width//2, chosen_height//2)))

        elif state == "score":
            screen.blit(end_bg, (0, 0))

            final_score = final_time * 10 + score * 20
            screen.blit(font.render(f"Score: {final_score}", True, (255,230,120)),
                        (chosen_width//2 - 80, chosen_height//2))

        pygame.display.flip()
        clock.tick(60)
        continue

    total = (pygame.time.get_ticks() - start_time) // 1000
    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    timer_text = font.render(time_str, True, (220, 200, 80))
    timer_rect = timer_text.get_rect(center=clock_rect.center)
    if health <= 0 and state == "playing":
        state = "death_anim"
        end_scale = 0.05
        end_alpha = 0
        death_time = pygame.time.get_ticks()
        final_time = (death_time - start_time) // 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hammer.change_state()
            mouse_pos = event.pos
            for zom in zomb:
                if (zom.moving >= 0 or isinstance (zom, Dancer)) and zom.is_hit(mouse_pos, BASE_HITBOX * chosen_width/BASE_WIDTH):
                    score += 10
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
    match health:
        case 5:
            screen.blit(health_bar[0], health_coord)
        case 4: 
            screen.blit(health_bar[1], health_coord)
        case 3: 
            screen.blit(health_bar[2], health_coord)
        case 2: 
            screen.blit(health_bar[3], health_coord)
        case 1: 
            screen.blit(health_bar[4], health_coord)
    #play random groans
    if num > 0:
        magic = random.randint(1, 300)
        if magic <= len(groan_tracks):
            groan_tracks[magic - 1].play()
    for z in zomb:
        num += z.spawn(resolution=(chosen_width, chosen_height))
        hehe = z.move(-1, 0)
        if hehe is not None and hehe < 0:
            num -= 1
            print(f"U got invaded! Score: {score}")
            health -= 1
            if health <= 0: 
                continue
        z.draw(screen)
    #draw fog screen
    for fog in fog_particles:
        fog.update()
        fog.draw(screen,fog_bound)

    #draw clock
    screen.blit(clock_img, clock_rect)
    timer_text = clock_font.render(time_str, True, (220, 200, 80))
    timer_rect = timer_text.get_rect(center=clock_rect.center)
    screen.blit(timer_text, timer_rect)

    hammer.move(pygame.mouse.get_pos())
    hammer.draw(screen)

    if pow_timer > 0:
        rect = pow.get_rect(center=pow_pos)
        screen.blit(pow, rect)
        pow_timer -= 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()