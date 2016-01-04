#!/usr/bin/env python

import pygame

class Dummy(pygame.sprite.Sprite):

    def __init__(self, pos):

        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.x, self.y = pos

        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(topleft=pos)
