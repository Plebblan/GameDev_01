import random
import pygame
import math
from settings import *

class FogParticle:
    def __init__(self, x, y, image):
        self.image = image.copy()
        self.image.set_alpha(100)

        self.base_x = x
        self.base_y = y

        self.phase = random.uniform(0, 6.28)
        self.amplitude = random.uniform(2, 6)
        self.speed = random.uniform(0.2, 0.6)

    def update(self):
        self.phase += 0.02 * self.speed
        self.x = self.base_x + self.amplitude * math.sin(self.phase)
        self.y = self.base_y + self.amplitude * 0.5 * math.cos(self.phase)

    def draw(self, screen):
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)