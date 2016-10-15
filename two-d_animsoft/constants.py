#!/usr/bin/env python2

#MAIN

DEBUG = False
SCREEN_SIZE = (500, 500)

# Default values
DEF_BONE_RAD = 12
DEF_BONE_SIZE = (40, 2 * DEF_BONE_RAD) # length, width
DEF_BONE_POS = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

DEF_THICKN = 12
DEF_CIRCLE_RAD = 32

DEF_CBONE_POS = DEF_BONE_POS[0] - 40, DEF_BONE_POS[1] - 40
RED_RAD = 6
YEL_RAD = 6


# Type strings
TYPE_BONE = "TYPE_BONE"
TYPE_CHIEF_BONE = "TYPE_CHIEF_BONE"
TYPE_CIRCLE_BONE = "TYPE_CIRCLE_BONE"

#Colours
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_BLUE = (0, 0, 255)
COL_BLACK = (0, 0, 0)
COL_WHITE = (255, 255, 255)
COL_GREY = (127, 127, 127)
COL_YELLOW = (255, 255, 0)

COL_ONION = COL_GREY

FPS = 60
