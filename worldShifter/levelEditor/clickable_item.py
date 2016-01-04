#!/usr/bin/env python

import pygame
from ed_const import *

'''
This class includes items that are draggable
by the cursor. Platorms, the player, and so on
are draggable in the level editor.

The de-selection of items will be (tabun) handled
by the main program.
'''

class Item(pygame.sprite.Sprite):

    def __init__(self, itemType, pos, imagePath, mainS):


        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.image = pygame.image.load(imagePath)
        self.mainS = mainS
        self.itemType = itemType

        self.selected = False # whether it is 'grabbed' by the cursor
        self.rect = self.image.get_rect(topleft=pos)

    def grid_new_pos(self, coords, offset):
        """
        Checks if coords(usually cursor coords) is at an
        appropriate distance away from self.
        Returns appropriat offset to snap self to the
        new grid position.
        """
        x_off = y_off = 0

        x_dist = coords[0] - self.rect.center[0] + offset
        y_dist = coords[1] - self.rect.center[1]

        x_sign = (-1 if x_dist < 0 else 1)
        y_sign = (-1 if y_dist < 0 else 1)


        x_off = x_dist - x_sign * (abs(x_dist) % GRID_W)
        y_off = y_dist - y_sign * (abs(y_dist) % GRID_H)
        return x_off, y_off


    def update(self, offset, mouse_state):
        """
        offset accounts for the scrolling of the
        screen
        """
        curPos = pygame.mouse.get_pos()

        if self.selected and mouse_state == SAFE:
            offset_tuple = self.grid_new_pos(curPos, offset)
            new_tup = [0, 0]
            new_tup[0] = self.pos[0] + offset_tuple[0]
            new_tup[1] = self.pos[1] + offset_tuple[1]
            new_tup = tuple(new_tup)
            self.pos = new_tup

        self.rect.x, self.rect.y = self.pos
