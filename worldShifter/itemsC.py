#!/usr/bin/env python

import pygame
from const import *

'''
@desc Module for items like coins
'''

class BaseItem(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

    def player_collision(self, player):

        return self.rect.colliderect(player.rect)

class Coin(BaseItem):

    def __init__(self, pos):

        BaseItem.__init__(self)

        self.x = pos[0]
        self.y = pos[1]

        self.value = 1
        self.consumed = False # consumed by player

        self.image = pygame.image.load(coinPath)
        self.rect = self.image.get_rect(topleft=pos)

        self.coinSound = pygame.mixer.Sound(coinSoundPath)
        self.coinSound.set_volume(0.2)
    def update(self, player):

        if self.player_collision(player):
            self.consumed = True
            self.coinSound.play()
            player.coins += self.value


class Key(BaseItem):

    def __init__(self, pos):

        BaseItem.__init__(self)

        self.pos = pos
        self.x, self.y = self.pos
        self.consumed = False
        self.value = 1

        self.image = pygame.image.load(keyPath)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, player):

        if self.player_collision(player):
            self.consumed = True
            player.keys += self.value
