#!/usr/bin/env python

import pygame, os
import const

class SpriteSheet:

    def __init__(self, sheetPath):

        self.sheet = pygame.image.load(sheetPath)

    def get_image(self, x, y, width, height):
        "get an image by giving the corrent co-ords and parameter"

        new_image = pygame.Surface([width, height])

        # copy image
        new_image.blit(self.sheet, (0, 0), (x, y, width, height))

        # assume black works as transparent colour
        new_image.set_colorkey(const.BLACK)

        return new_image
