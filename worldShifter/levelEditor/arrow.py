#!/usr/bin/env python

import pygame
from ed_const import *

class Arrow(pygame.sprite.Sprite):

    def __init__(self, pos, direc, dummy, lev_width, mainS):

        self.pos = pos
        self.lw = lev_width
        self.direc = direc
        self.dummy = dummy
        self.mainS = mainS

        self.speed = (10 if direc == RIGHT else -10)

        imgPath = (arrowRightPath if direc == RIGHT else arrowLeftPath)
        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect(topleft=pos)


    def update(self, curPos, clicked):
        """
        clicked: bool; mouse button pressed
        """

        # If the player clicks on the arrow, move
        # the dummy left/right but don't let it go
        # too far off

        if self.direc == LEFT:
            cond = (self.dummy.x > HALF_W)
        else:
            cond = (self.dummy.x < (self.lw - HALF_W))

        if self.rect.collidepoint(curPos) and clicked and cond:
            self.dummy.rect.move_ip((self.speed, 0))
            self.dummy.x += self.speed
            self.mainS.blit(self.image, self.rect)
            return self.speed
        self.mainS.blit(self.image, self.rect)
        return 0
