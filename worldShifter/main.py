#!/usr/bin/env python

import pygame

class Button(pygame.sprite.Sprite):
    
    def __init__(self, pos, action):
        
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.action = action

        self.rect = pygame
