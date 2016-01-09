#!/usr/bin/env python

import os

SCREEN_W = 500
SCREEN_H = 500
HALF_W = int(SCREEN_W/2)
HALF_H = int(SCREEN_H/2)
level_w = 1600
level_h = 500

#enemyTypes
SQUISHY = "squishy"
SLOPE = "slope"
# Colours

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# directions
LEFT = "lefT"
RIGHT = "right"

#others
TOLERANCE = 10
FIRE_TIME_LIMIT = 2 # seconds till player can fire again

#paths
cursorPath = os.path.join("images", "cursor_small.png")

jumpPath = os.path.join("images", "p1_jump.png")
playWalkPath = os.path.join("images", "p1_walk.png")
dirtPath = os.path.join("images", "dirt.png")
grassPath = os.path.join("images", "grass.png")
grassSlopePath = os.path.join("images", "grassHillRight.png")
stonePath = os.path.join("images", "stone.png")

slime1Path = os.path.join("images", "slimeWalk1.png")
slime2Path = os.path.join("images", "slimeWalk2.png")

coinPath = os.path.join("images", "coinGoldNew.png")
coinHUDPath = os.path.join("images", "hud_coins.png")
keyPath = os.path.join("images", "keyGreen.png")
keyHUDPath = os.path.join("images", "hud_keyGreen.png")

firePath = os.path.join("images", "fireball.png")

ropePath = os.path.join("images", "ropeVertical.png")
ropeJoinPath = os.path.join("images", "ropeAttached.png")
boardDownPath = os.path.join("images", "springBoardDown.png")
boardUpPath = os.path.join("images", "springBoardUp.png")

switchLeftPath = os.path.join("images", "switchLeft.png")
switchRightPath = os.path.join("images", "switchRight.png")

doorClosedPath = os.path.join("images", "door_closedMid.png")
doorOpenPath = os.path.join("images", "door_openMid.png")

#Sound paths
coinSoundPath = os.path.join("other_resources", "coin.ogg")

GRAVITY = 0.25
MAX_PLAYER_HEALTH = 1000



# Paths needed for frontend
STARTBUT_PATH = os.path.join("images", "but_start.png")
EDITBUT_PATH = os.path.join("images", "but_edit.png")
 
