#!/usr/bin/env python2

import pygame as pg
import constants as const

class PivotHandle(object):
    
    def __init__(self, bone, pos): 
        self.bone = bone
        #self.mainS = mainS
        self.pos = pos

        self.getRect()

    def __copy__(self):
        
        cls = self.__class__
        result =  cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def getRect(self):

        self.rect = pg.Rect(self.pos[0] - const.RED_RAD,
                            self.pos[1] - const.RED_RAD,
                            const.RED_RAD * 2, const.RED_RAD * 2)


    def update(self, newPos):
        
        self.pos = newPos
        self.getRect()

    def draw(self, mainS):
        
        pg.draw.circle(mainS, const.COL_RED, self.pos, const.RED_RAD)

        if const.DEBUG:
            pg.draw.rect(mainS, const.COL_GREEN, self.rect, 2)



class Translator:
    
    def __init__(self, bone, pos):
        
        self.bone  = bone
        self.pos = pos
        self.getRect()


    def getRect(self):
        
        self.rect = pg.Rect(self.pos[0] - const.YEL_RAD,
                            self.pos[1] - const.YEL_RAD,
                            2 * const.YEL_RAD, 2 * const.YEL_RAD)

    def update(self, newPos):
        
        self.pos = newPos
        self.getRect()

    def draw(self, mainS):
        
        pg.draw.circle(mainS, const.COL_YELLOW, self.pos, const.YEL_RAD)

        if const.DEBUG:
            pg.draw.rect(mainS, const.COL_GREEN, self.rect, 2)

        
