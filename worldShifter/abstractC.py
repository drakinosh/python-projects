"""
This module contains asbstract objects such as:
    line-of-sight objects, counters, and so on.
"""
import pygame
from const import *

class LOS:
    
    def __init__(self, pos, direc):
        
        self.pos = pos
        self.direc = direc

        self.rect = pygame.Rect(pos, (LOS_WIDTH, LOS_HEIGHT))
        
        if self.direc == RIGHT:
            self.rect.topleft = pos
        else:
            self.rect.topright = pos

    def check_LOS_collision(self, player, mainS, cam):
        
        if GLOBAL_DEBUG:
            r2 = cam.use_cam_rect(self.rect)
            pygame.draw.rect(mainS, GREEN, r2)
        return self.rect.colliderect(player.rect)

