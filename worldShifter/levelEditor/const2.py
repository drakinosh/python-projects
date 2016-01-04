#!/usr/bin/env python

import os

#FILEPATHS
CURPATH = os.path.dirname(__file__)

itemDictFile = os.path.join(CURPATH, "ITEM_DICT_FILE.pickle")
levelFile = os.path.join(CURPATH, "level_dump.lvf")


#DIMENSIONS
SCREEN_H = 600
SCREEN_W = 500
GRID_H, GRID_W = 70, 70
PANEL_H = 100
CREATE_POS = (GRID_W, GRID_H * 2 )

#MAIN CONSTS
FPS = 50


#MOUSE STATES
SAFE = "SAFE"    # mouse is in safe zone
RESTRICTED = "RESTRICTED" # mouse is in restricted zone i.e. in panel-areas

#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (185, 185, 185)

#IMAGE PATHS

grassBigImgPath = os.path.join("img", "grass.png")
grassIconPath = os.path.join("img", "grass_icon.png")
tint_grassIconPath = os.path.join("img", "grass_icon_tint.png")
coinImgPath = os.path.join("img", "coinGoldNew.png")
coinIconPath = os.path.join("img", "coin_icon.png")
tint_coinIconPath = os.path.join("img", "coin_icon_tint.png")
playerImgPath = os.path.join("img", "player.png")
playerIconPath = os.path.join("img", "player_icon.png")
tint_playerIconPath = os.path.join("img", "player_icon_tint.png")

# item types
GRASS = "GRASS"
COIN = "COIN"
PLAYER = "PLAYER"

# Dictionary mapping item type to image path
imgDict = {GRASS: grassBigImgPath, \
           COIN: coinImgPath, \
           PLAYER: playerImgPath}
