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