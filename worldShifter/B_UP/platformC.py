#!/usr/bin/env python

import pygame
from const import *
import rotateC

class Platform(pygame.sprite.Sprite):
    
    width = 70
    height = 70
    
    def __init__(self, pos, origin="center"):
        # Call parent's constructor
	pygame.sprite.Sprite.__init__(self)

	self.x = pos[0]
	self.y = pos[1]

	self.original_image = pygame.image.load(grassPath).convert()
	
	# set black as transparent colorkey
	self.original_image.set_colorkey(BLACK)

	self.image = self.original_image.copy()
	self.rect = self.image.get_rect(center=pos)
	self.angle = 0
	self.speed = 3
	self.speed_ang = 90
	self.rotator = None
        
	try:
	    self.set_origin(getattr(self.rect, origin))
	except TypeError:
	    self.set_origin(origin)

	
    def set_origin(self, point):
        self.origin = list(point)
	self.rotator = rotateC.Rotator(self.rect.center, point, self.angle)

    def rotate(self):
        if self.speed_ang:
	    self.angle = (self.angle + self.speed_ang) % 360
	    new_center = self.rotator(self.angle, self.origin)
	    self.image = pygame.transform.rotate(self.original_image, self.angle)
	    self.rect = self.image.get_rect(center=new_center)

    def draw(self, screen):
        
	screen.blit(self.image, self.rect)
    
    def update(self, screen, doRotate):
        if doRotate:
            self.rotate()
	self.draw(screen)
