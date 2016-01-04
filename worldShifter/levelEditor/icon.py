#!/usr/bin/env python

import pygame
from ed_const import *

class Icon(pygame.sprite.Sprite):

    def __init__(self, itemType, imgPath, tintPath,  pos, mainS):

        pygame.sprite.Sprite.__init__(self)

        self.n_image = pygame.image.load(imgPath)
        self.h_image = pygame.image.load(tintPath)
        self.pos = pos
        self.mainS = mainS
        self.itemType = itemType

        self.image = self.n_image
        self.rect = self.image.get_rect(topleft=pos)

        self.selected = False

    def update(self):

        if self.selected:
            self.image = self.h_image
        else:
            self.image = self.n_image

        self.mainS.blit(self.image, self.rect)
