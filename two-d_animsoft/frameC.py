#!/usr/bin/env python2

import pygame as pg

class Frame:
    
    def __init__(self, mainS, number, bone_list):
        
        self.bone_list = bone_list
        self.number = number
        self.mainS = mainS
