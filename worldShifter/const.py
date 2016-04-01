#!/usr/bin/env python

import os

#DEBUG VARS
GLOBAL_DEBUG = False

SCREEN_W = 500
SCREEN_H = 500
HALF_W = int(SCREEN_W/2)
HALF_H = int(SCREEN_H/2)
level_w = 1600
level_h = 500

# -- enemyTypes

# SQUISHY: Can be 'squished' if player jumps on it
SQUISHY = "squishy"

SLOPE = "slope"

WATER_DOWN_SPEED = 0.12

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
AI_THRESHOLD_DIFF = 150

LOS_HEIGHT = 4
LOS_WIDTH = AI_THRESHOLD_DIFF
#paths
cursorPath = os.path.join("images", "cursor_small.png")

jumpPath = os.path.join("images", "p1_jump.png")
playWalkPath = os.path.join("images", "p1_walk.png")
dirtPath = os.path.join("images", "dirt.png")
grassPath = os.path.join("images", "grass.png")
grassLeftPath = os.path.join("images", "grassLeft.png")
grassMidPath = os.path.join("images", "grassMid.png")
grassRightPath = os.path.join("images", "grassRight.png")
grassCenterPath = os.path.join("images", "grassCenter.png")

grassSlopePath = os.path.join("images", "grassHillRight.png")
stonePath = os.path.join("images", "stone.png")

waterPath = os.path.join("images", "liquidWater.png")
waterTopPath = os.path.join("images", "liquidWaterTop.png")
waterTopMidPath = os.path.join("images", "liquidWaterTop_mid.png")

slime1Path = os.path.join("images", "slimeWalk1.png")
slime2Path = os.path.join("images", "slimeWalk2.png")
fly1Path = os.path.join("images", "flyFly1.png")
fly2Path = os.path.join("images", "flyFly2.png")
frogLeapLeftPath= os.path.join("images", "frog_leap.png")
frogSquatLeftPath = os.path.join("images", "frog.png")

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
BUOYANCY = 0.5

# Paths needed for frontend
STARTBUT_PATH = os.path.join("images", "but_start.png")
EDITBUT_PATH = os.path.join("images", "but_edit.png")
 
