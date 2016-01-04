#!/usr/bin/env python

import pygame
from const import *

'''
@desc Class for stuff like ladders, ropes, elevators,
      vehicles, and such
'''

class Base(pygame.sprite.Sprite):

    def __init__(self, pos, imgPath):
        
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.x, self.y = pos

        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect(topleft=pos)
    
    def check_player_collision(self, player):
        return self.rect.colliderect(player.rect)


class Rope(Base):
	
	def __init__(self, pos, imgPath):
	    Base.__init__(self, pos, imgPath)
	
	def update(self, player):

	    if self.check_player_collision(player):
	        player.climb = True
	    

class Switch(Base):
    
    def __init__(self, pos):
        
        Base.__init__(self, pos, switchLeftPath)
        
        self.used = False # the switch is unused
        self.type = "SWITCH"

    def update(self):
        
        if self.used == True:
            self.image = pygame.image.load(switchRightPath)
        else:
            self.image = pygame.image.load(switchLeftPath)
