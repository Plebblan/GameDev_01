import random
import pygame
import math
from settings import *

class FogParticle:
    def __init__(self, x, y, image):
        self.image = image.copy()
        self.image.set_alpha(120)

        self.base_x = x
        self.base_y = y

        self.phase = random.uniform(0, 6.28)
        self.amp_x = random.uniform(8, 18)
        self.amp_y = random.uniform(4, 10)
        self.speed = random.uniform(0.6, 1.1)

    def update(self):
        self.phase += 0.015 * self.speed
        self.x = self.base_x + self.amp_x * math.sin(self.phase)
        self.y = self.base_y + self.amp_y * math.cos(self.phase * 0.7)

    def draw(self, screen, fog_bound):
        rect = self.image.get_rect(center=(self.x, self.y))
        if rect.colliderect(fog_bound):
            clipped = rect.clip(fog_bound)
            area = clipped.move(-rect.x, -rect.y)
            screen.blit(self.image, clipped.topleft, area)

def create_fog_wall(fog_images,chosen_width,chosen_height):
    fog_particles = []
    lanes = [115]+[int(y * chosen_height/360) for y in BASE_Y]
    fog_bound = pygame.Rect(
        FOG_X * chosen_width/640,
        0,
        chosen_width - FOG_X * chosen_width/640,
        chosen_height
    )

    for lane_y in lanes:
        for i in range(6):
            x = int(chosen_width * (FOG_LEFT + (i + 0.5) * (1 - FOG_LEFT) / 5))
            img = random.choice(fog_images)

            #scale fog image
            scale_x = chosen_width / BASE_WIDTH
            scale_y = chosen_height / BASE_HEIGHT
            scale = random.uniform(0.7, 1.2)
            img = pygame.transform.smoothscale(
                img,
                (
                    int(img.get_width() * scale * scale_x),
                    int(img.get_height() * scale * scale_y)
                )
            )

            fog_particles.append(FogParticle(x, lane_y, img))
    return fog_particles,fog_bound