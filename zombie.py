import pygame
import random
from utils import *
from abc import ABC
from settings import *

class Hammer(ABC):
    def __init__(self, position = (0, 0), size=(BASE_HAMMER, BASE_HAMMER), directory="assets/image/hammer"):
        self.frames = load_hammer_frames(directory, size)
        self.position = position
        self.state = 0
        self.swing = pygame.mixer.Sound("assets/sound/Effect/swing.ogg")
        self.bonk = pygame.mixer.Sound("assets/sound/Effect/bonk.ogg")

    def draw(self, screen):
        curr = self.frames[self.state]
        cur_rect = curr.get_rect(center=self.position)
        screen.blit(self.frames[self.state], cur_rect)
        if self.state == len(self.frames) - 1:
            self.state = 0
        if self.state > 0:
            self.state += 1
    
    def change_state(self):
        self.swing.play()
        if (self.state == 0):
            self.state += 1
    
    def move(self, pos):
        self.position = pos

class Zombie(ABC):
    def __init__(self, position= BASE_X, line=1, resolution=(BASE_WIDTH, BASE_HEIGHT), directory="assets/image/basic"):
        """
        Initialize a Zombie instance.
        
        :param self: Description
        :param position: x position of zombie
        :param line: y line of zombie (1 - 5)
        :param resolution: current screen resolution
        :param directory: Description
        """
        self.position = (self.scale(resolution, BASE_X), self.scale(resolution, BASE_Y[line - 1]))
        self.size = self.scale(resolution, BASE_SIZE)
        self.move_sprites = load_zombie_frames(directory, "move", self.size)
        self.dead_sprites = load_zombie_frames(directory, "die", self.size)
        self.image = pygame.Surface((self.size, self.size))
        self.moving = -1 #index for move animation
        self.dying = -1 #index for dead animation
        self.update = 0

    def draw(self, screen):
        """
        Get sprite corresponding to current frame and draw it on screen.
        
        :param self: Description
        :param screen: Description
        """
        if self.dying == -1:
            return
        screen.blit(self.image, (self.position[0] - self.size // 2, self.position[1] - self.size))

    def scale(self, resolution, value):
        """
        Scale a value based on current resolution.
        
        :param self: Description
        :param resolution: current screen resolution
        :param value: value to be scaled
        """
        value = int(value * resolution[0] / BASE_WIDTH)
        return value
    
    def move(self, dx, dy):
        if self.moving >= 0:
            self.position = (self.position[0] + dx, self.position[1] + dy)
        else: 
            self.position = (self.position[0] + dx / 4, self.position[1] + dy)
        self.update-=1
        if self.update < 0:
            if self.moving >= 0:
                self.image = self.move_sprites[self.moving]
                if self.moving < len(self.move_sprites) - 1:
                    self.moving += 1  # Advance to next move sprite
                else:
                    self.moving = 0  # Loop back to first move sprite
            elif self.dying >= 0: #dying animation
                self.image = self.dead_sprites[self.dying]
                if self.dying < len(self.dead_sprites) - 1:
                    self.dying += 1  # Advance to next dead sprite
                else:
                    self.dying = -1
            self.update = 3

    def change_state(self, state=None):
        """
        Change the state of the zombie (e.g., from moving to dying).
        
        :param self: Description
        :param state: New state for the zombie
        """
        if state == "walk":
            self.moving = 0
            self.dying = 0
            return 1
        elif state == "die":
            self.moving = -1
            self.dying = 0
            return -1
        else:
            return 0
            self.moving = 0
            self.dying = 0
    
    def is_hit(self, mouse_pos, hm_hitbox):
        cur = (self.position[0] - self.size // 2, self.position[1] - self.size)
        hm_LD  = mouse_pos[0] - cur[0] - hm_hitbox // 2, mouse_pos[1] - cur[1] - hm_hitbox // 2
        hammer_rect = pygame.Rect(hm_LD[0], hm_LD[1], hm_hitbox / 2, hm_hitbox / 2)
        bounding_rect = self.image.get_bounding_rect()
        # return hm_LD[0] + hm_hitbox - 10 > bounding_rect[0] and bounding_rect[0] + bounding_rect[2] > hm_LD[0] - 10 and hm_LD[1] + hm_hitbox > bounding_rect[1] and bounding_rect[1] + bounding_rect[3] > hm_LD[1]
        return hammer_rect.colliderect(bounding_rect)
    
    def spawn(self, resolution=(BASE_WIDTH, BASE_HEIGHT)):
        if self.moving == -1 and self.dying == -1:
            magic = random.randint(1, 10)
            if magic in range(1, 6):
                self.position = (self.scale(resolution, BASE_X), self.scale(resolution, BASE_Y[magic - 1]))
                return self.change_state("walk")
            else:
                return 0
        return 0