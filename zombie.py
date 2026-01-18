import pygame
from utils import load_zombie_frames
from abc import ABC
from settings import BASE_X, BASE_Y, BASE_HEIGHT, BASE_WIDTH, BASE_SIZE
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
        self.moving = 0 #index for move animation
        self.dying = 0 #index for dead animation
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
        self.position = (self.position[0] + dx, self.position[1] + dy)
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
            self.moving = 1
            self.dying = 0
        elif state == "die":
            self.moving = -1
            self.dying = 0
        else:
            return
            self.moving = 0
            self.dying = 0
    
    def is_hit(self, mouse_pos):
        cur = (self.position[0] - self.size // 2, self.position[1] - self.size)
        if mouse_pos[0] - cur[0] <= self.size and mouse_pos[0] - cur[0] >= 0 and mouse_pos[1] - cur[1] <= self.size and mouse_pos[1] - cur[1] >= 0:
            pos_in_ret =  mouse_pos[0] - cur[0], mouse_pos[1] - cur[1]
            mask = pygame.mask.from_surface(self.image)
            if mask.get_at(pos_in_ret):
                return True
        return False
        