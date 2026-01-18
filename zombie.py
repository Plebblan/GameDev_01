import pygame
from utils import load_zombie_frames
from abc import ABC
class Zombie(ABC):
    def __init__(self, position, size=95, directory="assets"):
        self.position = position
        self.size = size
        self.move_sprites = load_zombie_frames("assets/image/basic", "move", size)
        self.dead_sprites = load_zombie_frames("assets/image/basic", "die", size)
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 255, 0))  # Green square as placeholder
        self.moving = 0 #index for move animation
        self.dying = 0 #index for dead animation
        self.update = 0

    def draw(self, screen):
        """
        Get sprite corresponding to current frame and draw it on screen.
        
        :param self: Description
        :param screen: Description
        """
        screen.blit(self.image, (self.position[0] - self.size // 2, self.position[1] - self.size // 2)) # Center the image
    
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
            else: #dying animation
                self.image = self.dead_sprites[self.dying]
                if self.dying < len(self.dead_sprites) - 1:
                    self.dying += 1  # Advance to next dead sprite
                else:
                    self.dying = len(self.dead_sprites) - 1  # Stay on last dead sprite
            self.update = 10

    def change_state(self, state=None):
        """
        Change the state of the zombie (e.g., from moving to dying).
        
        :param self: Description
        :param state: New state for the zombie
        """
        if (self.moving >= 0):
            self.moving = -1
            self.dying = 0
        else:
            self.moving = 0
            self.dying = 0
