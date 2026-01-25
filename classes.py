import pygame
import random
from utils import *
from abc import ABC
from settings import *

dirt_sprites = []
zom_frame = None

Time_update = 0.5

SCALE_DANCER_OVER_BASIC = 0.6

class Hammer(ABC):
    def __init__(self, frames, position = (0, 0), size=(BASE_HAMMER, BASE_HAMMER)):
        self.frames = frames
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
    def __init__(self, mov, die, position= BASE_X, line=1, resolution=(BASE_WIDTH, BASE_HEIGHT), speed=1):
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
        self.move_sprites = mov
        self.dead_sprites = die
        self.image = pygame.Surface((self.size, self.size))
        self.moving = -1 #index for move animation
        self.dying = -1 #index for dead animation
        self.update = 0
        self.resolution = resolution
        self.speed = speed

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
        value = value * resolution[0] / BASE_WIDTH
        return value
    
    def move(self, dx, dy):
        if self.moving >= 0:
            self.position = (self.position[0] + self.scale(self.resolution, dx) * self.speed, self.position[1] + dy * self.speed)
            if self.position[0] <= HURT_BASE * self.resolution[0] / BASE_WIDTH:
                self.change_state("hurt")
                return -1
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
            self.update = int(Time_update / (-self.scale(self.resolution, dx)/self.speed))

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
        elif state == "hurt":
            self.moving = -1
            self.dying = -1
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
    
    def reset(self):
        self.change_state("hurt")
class Creep(Zombie):
    def __init__(self, mov, die, position=BASE_X, line=1, resolution=(BASE_WIDTH, BASE_HEIGHT), speed=0.6):
        super().__init__(mov, die, position, line, resolution, speed)
        self.summoned_flag = True
        self.summon_sprites = create_summon_sprites(self.size)
        self.summon_idx = -1

    def is_summoned(self):
        return self.summoned_flag
    
    def move(self, dx, dy):
        if self.summoned_flag == False:
            pass
        elif self.moving >= 0:
            self.position = (self.position[0] + self.scale(self.resolution, dx) * self.speed, self.position[1] + dy * self.speed)
            if self.position[0] <= HURT_BASE * self.resolution[0] / BASE_WIDTH:
                self.change_state("hurt")
                return -1
        self.update-=1
        if self.update < 0:
            if self.summoned_flag == False and self.summon_idx >= 0:
                self.image = self.summon_sprites[int(self.summon_idx)]
                if self.summon_idx < len(self.summon_sprites) - 1:
                    self.summon_idx += 0.5
                else:
                    self.summon_idx = -1  
                    self.summoned_flag = True
                    self.change_state("walk")
            elif self.moving >= 0:
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
            self.update = int(Time_update / (-self.scale(self.resolution, dx)/self.speed))

    def draw(self, screen):
        if self.dying == -1:
            return
        else:
            screen.blit(self.image, (self.position[0] - self.size // 2, self.position[1] - self.size))
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
            self.summoned_flag = True
            self.moving = -1
            self.dying = 0
            return -1
        elif state == "summon":
            self.summoned_flag = False
            self.summon_idx = 0
            self.moving = 0
            self.dying = 0
        elif state == "hurt":
            self.summoned_flag = True
            self.moving = -1
            self.dying = -1
        else:
            return 0
            self.moving = 0
            self.dying = 0

    def set(self, position, idx = 0):
        if idx == 0:
            self.position = position[0], position[1] - self.scale(self.resolution, BASE_Y[1]-BASE_Y[0])
            return self.position[1] > self.scale(self.resolution, BASE_Y[0]-10)
        elif idx == 1:
            self.position = position[0], position[1] + self.scale(self.resolution, BASE_Y[1]-BASE_Y[0])
            return self.position[1] < self.scale(self.resolution, BASE_Y[4]+10)
        elif idx == 2:
            self.position = position[0] + self.scale(self.resolution, BASE_SIZE*1.5), position[1]
            return self.position[0] < self.scale(self.resolution, BASE_WIDTH + 10)
        else:
            self.position = position[0] - self.scale(self.resolution, BASE_SIZE*1.5), position[1]
            return self.position[0] > 0

        
class Dancer(Zombie):
    def __init__(self, mov, die, sub_mov, sub_die, position=BASE_X, line=1, resolution=(BASE_WIDTH, BASE_HEIGHT), speed=0.5):
        super().__init__(mov, die, position, line, resolution, speed)
        self.creeps = [Creep(sub_mov, sub_die, position, line + 1, resolution), 
                  Creep(sub_mov, sub_die, position, line - 1, resolution), 
                  Creep(sub_mov, sub_die, position + self.scale(resolution, BASE_SIZE*1.2), line, resolution), 
                  Creep(sub_mov, sub_die, position - self.scale(resolution, BASE_SIZE*1.2), line, resolution)
                  ]
        self.summon_creep = []
        self.summon_flag = False
        self.cd = 0
        self.up_to_len = True

    def summon(self):
        if self.cd > 0:
            self.cd -= 1
            return
        self.cd = 2
        if self.moving == -1:
            return
        for idx, creep in enumerate(self.creeps):
            if idx not in self.summon_creep:
                value = creep.set(self.position, idx)
                if value:
                    self.summon_creep  += [idx]
                    creep.change_state("summon")
                    self.summon_flag = True

    def move(self, dx, dy):
        ret = 0
        if self.moving >= 0:
            self.position = (self.position[0] + self.scale(self.resolution, dx)/(self.speed*(2*int(not self.up_to_len)) + 1), self.position[1] + dy) if not self.summon_flag and self.moving < 63 and not (28 <= self.moving <= 47) else self.position
            if self.position[0] <= HURT_BASE * self.resolution[0] / BASE_WIDTH:
                self.change_state("hurt")
                ret -=1
        self.update -= 1
        if self.update < 0:
            if self.summon_flag and self.moving >= 0:
                None
            elif self.moving >= 0:
                self.image = self.move_sprites[self.moving]
                if self.moving == 32 :
                    self.summon()
                if self.moving < len(self.move_sprites) - 1 and self.up_to_len:
                    self.moving += 1  # Advance to next move sprite
                elif self.moving >= 0:
                    self.up_to_len = False if self.moving > 0 else True
                    if not self.up_to_len:
                        self.moving -= 1  # Loop back to first move sprite
            elif self.dying >= 0: #dying animation
                self.image = self.dead_sprites[self.dying]
                if self.dying < len(self.dead_sprites) - 1:
                    self.dying += 1  # Advance to next dead sprite
                else:
                    self.dying = -1
            self.update = int((Time_update/SCALE_DANCER_OVER_BASIC) / (-self.scale(self.resolution, dx)/self.speed))
        for idx, creep in enumerate(self.creeps):
            if creep.move(dx, dy) == -1:
                ret -= 1
                self.summon_creep.remove(idx)
        return ret

    def draw(self, screen):
        for creep in self.creeps:
            creep.draw(screen)
        if self.dying == -1:
            return
        self.summon_flag = not all(creep.is_summoned() for creep in self.creeps)
        real_image = pygame.transform.flip(self.image, True, False) if 0 <= self.moving < 31 else self.image
        boundind_rect = real_image.get_bounding_rect()
        rect = real_image.get_rect()
        real_image = real_image.subsurface((boundind_rect[0], rect[1], boundind_rect[2], rect[3])).copy()
        screen.blit(real_image, (self.position[0] - self.size // 2, self.position[1] - self.size))

    def is_hit(self, mouse_pos, hm_hitbox):
        cur = (self.position[0] - self.size // 2, self.position[1] - self.size)
        hm_LD  = mouse_pos[0] - cur[0] - hm_hitbox // 2, mouse_pos[1] - cur[1] - hm_hitbox // 2
        hammer_rect = pygame.Rect(hm_LD[0], hm_LD[1], hm_hitbox / 2, hm_hitbox / 2)
        bounding_rect = self.image.get_bounding_rect()
        value = hammer_rect.colliderect(bounding_rect)
        if self.moving == -1 and value:
            value = False
        if value and self.moving != -1:
            self.change_state("die")
        dead_list = []
        for idx in self.summon_creep:
            var = self.creeps[idx].is_hit(mouse_pos, hm_hitbox)
            if var:
                self.creeps[idx].change_state("die")
                value = True
                dead_list += [idx]
        self.summon_creep = [idx for idx in self.summon_creep if idx not in dead_list] 
        return value
        
    def spawn(self, resolution=(BASE_WIDTH, BASE_HEIGHT)):
        if len(self.summon_creep) > 0:
            return 0
        if self.moving == -1 and self.dying == -1:
            magic = random.randint(1, 10)
            if magic in range(1, 6):
                self.position = (self.scale(resolution, BASE_X), self.scale(resolution, BASE_Y[magic - 1]))
                return self.change_state("walk")
            else:
                return 0
        return 0
    
    def reset(self):
        self.change_state("hurt")
        self.summon_creep.clear()
        for creep in self.creeps:
            creep.change_state("hurt")
