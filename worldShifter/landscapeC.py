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
    
    def __init__(self, pos, action_id):
        
        Base.__init__(self, pos, switchLeftPath)
        
        self.used = False # the switch is unused
        self.type = "SWITCH"
        self.action_id = action_id

    def update(self):
        
        if self.used == True:
            self.image = pygame.image.load(switchRightPath)
        else:
            self.image = pygame.image.load(switchLeftPath)


class Door(Base):
    
    def __init__(self, pos, action_id):
        """
        Create a new Door object.
            pos is the position.
            aciton_id is a number common to a Door and its
              corresponding switch.
        """
        
        Base.__init__(self, pos, doorClosedPath)

        self.open = False   # closed by default
        self.type = "DOOR"
        self.action_id = action_id

    def update(self):
        
        if self.open:
            self.image = pygame.image.load(doorOpenPath)
        else:
            self.image = pygame.image.load(doorClosedPath)

