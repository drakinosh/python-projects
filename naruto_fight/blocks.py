import pygame as pg
import const as c

class Block(pg.sprite.Sprite):
    
    def __init__(self, pos):

        pg.sprite.Sprite.__init__(self)

        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

        self.w = 50
        self.h = 50

        self.visible = False
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
