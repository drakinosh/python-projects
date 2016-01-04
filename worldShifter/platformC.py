#!/usr/bin/env python

import pygame
from const import *
import rotateC

class Platform(pygame.sprite.Sprite):

    def __init__(self, pos, imgPath):

        pygame.sprite.Sprite.__init__(self)

        self.x, self.y = pos
        self.type = "BLOCK"
        self.plat_type = "SIMPLE"
        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen):

        screen.blit(self.image, self.rect)



class RotPlatform(pygame.sprite.Sprite):

    width = 70
    height = 70

    def __init__(self, pos, imgPath,  origin="center"):
        # Call parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.x = pos[0]
        self.y = pos[1]

        self.original_image = pygame.image.load(imgPath).convert()

        # set black as transparent colorkey
        self.original_image.set_colorkey(BLACK)
        self.type = "BLOCK"
	self.plat_type = "BLOCK"
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.angle = 0
        self.speed = 3
        self.vel_ang = 9
        self.speed_ang = 90
        self.rot = 0
        self.rotator = None
        self.shouldRotate = False # decide whether to rotate or not
        self.iter_comp = False # have completed one rotation
        self.inertia = False # player has activated rotation

        try:
            self.set_origin(getattr(self.rect, origin)) # using default args
        except TypeError:
            self.set_origin(origin) # argument is given by caller


    def set_origin(self, point):
        self.origin = list(point)
        self.rotator = rotateC.Rotator(self.rect.center, point, self.angle)

    def rotate(self):
        if self.rot != self.speed_ang:
            self.rot += self.vel_ang
            self.angle = (self.angle + self.vel_ang) % 360
            new_center = self.rotator(self.angle, self.origin)
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=new_center)
        else:
            self.rot = 0
            self.iter_comp = True
            self.inertia = False

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def update(self, screen, doRotate):
        if doRotate:
            self.shouldRotate = True
            self.inertia = True

        elif not doRotate and self.inertia:
            if not self.iter_comp:
                self.shouldRotate = True
        else:
            self.shouldRotate = False


        if self.shouldRotate:
            self.rotate()

class Slope(pygame.sprite.Sprite):

    def __init__(self, pos):

        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.image = pygame.image.load(grassSlopePath)
        self.plat_type = SLOPE
        self.rect = self.image.get_rect(topleft=pos)
