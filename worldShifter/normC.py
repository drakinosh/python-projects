#!/usr/bin/env python

# normal platforms / non-rotating platforms

import const, pygame

class NormPlat(pygame.sprite.Sprite):

    def __init__(self, pos):

        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(pos, (50, 25))
        self.image = pygame.Surface((50, 25))
        self.image.fill(const.BLACK)
        self.plat_type = "GROUND"
        self.type = "BLOCK"

    def draw(self, screen):
        screen.blit(self.image, self.rect)
