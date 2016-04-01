#!/usr/bin/env python
import os 
#FILEPATHS
CURPATH = os.path.dirname(__file__)
itemDictFile = os.path.join(CURPATH, "ITEM_DICT_FILE.pickle")
levelFile = os.path.join(CURPATH, "level_dump.lvf")


#DIMENSIONS 
SCREEN_H = 650
SCREEN_W = 500
GRID_H, GRID_W = 70, 70
PANEL_H = SCREEN_H - 500
CREATE_POS = (GRID_W, GRID_H * 2 )

HALF_W = int(SCREEN_W / 2)
HALF_H = int((SCREEN_H - PANEL_H) / 2)

#MAIN CONSTS
FPS = 50
RIGHT = "RIGHT"
LEFT = "LEFT"

#MOUSE STATES
SAFE = "SAFE"    # mouse is in safe zone
RESTRICTED = "RESTRICTED" # mouse is in restricted zone i.e. in panel-areas

#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (185, 185, 185)

#IMAGE PATHS

# for compatibility with imports
ACT_PATH = os.path.join(os.path.dirname(__file__), "img")

#--IMAGES--

#--Platform tiles--

grassBigImgPath = os.path.join(ACT_PATH, "grass.png")
grassIconPath = os.path.join(ACT_PATH, "grass_icon.png")
tint_grassIconPath = os.path.join(ACT_PATH, "grass_icon_tint.png")
grassLeftImgPath = os.path.join(ACT_PATH, "grassLeft.png")
grassLeftIconPath = os.path.join(ACT_PATH, "grassLeft_icon.png")
tint_grassLeftIconPath = os.path.join(ACT_PATH, "grassLeft_icon_tint.png")
grassMidImgPath = os.path.join(ACT_PATH, "grassMid.png")
grassMidIconPath = os.path.join(ACT_PATH, "grassMid_icon.png")
tint_grassMidIconPath = os.path.join(ACT_PATH, "grassMid_icon_tint.png")
grassRightImgPath = os.path.join(ACT_PATH, "grassRight.png")
grassRightIconPath = os.path.join(ACT_PATH, "grassRight_icon.png")
tint_grassRightIconPath = os.path.join(ACT_PATH, "grassRight_icon_tint.png")
grassCenterImgPath = os.path.join(ACT_PATH, "grassCenter.png")
grassCenterIconPath = os.path.join(ACT_PATH, "grassCenter_icon.png")
tint_grassCenterIconPath = os.path.join(ACT_PATH, "grassCenter_icon_tint.png")

waterImgPath = os.path.join(ACT_PATH, "liquidWater.png")
waterIconPath = os.path.join(ACT_PATH, "liquidWater_icon.png")
tint_waterIconPath = os.path.join(ACT_PATH, "liquidWater_icon_tint.png")


stoneBigImgPath = os.path.join(ACT_PATH, "stone.png")
stoneIconPath = os.path.join(ACT_PATH, "stone_icon.png")
tint_stoneIconPath = os.path.join(ACT_PATH, "stone_icon_tint.png")
coinImgPath = os.path.join(ACT_PATH, "coinGoldNew.png")
coinIconPath = os.path.join(ACT_PATH, "coin_icon.png")
tint_coinIconPath = os.path.join(ACT_PATH, "coin_icon_tint.png")
playerImgPath = os.path.join(ACT_PATH, "player.png")
playerIconPath = os.path.join(ACT_PATH, "player_icon.png")
tint_playerIconPath = os.path.join(ACT_PATH, "player_icon_tint.png")
slimeImgPath = os.path.join(ACT_PATH, "slime.png")
slimeIconPath = os.path.join(ACT_PATH, "slime_icon.png")
tint_slimeIconPath = os.path.join(ACT_PATH, "slime_icon_tint.png")
flyImgPath = os.path.join(ACT_PATH, "fly.png")
flyIconPath = os.path.join(ACT_PATH, "fly_icon.png")
tint_flyIconPath = os.path.join(ACT_PATH, "fly_icon_tint.png")

frogImgPath = os.path.join(ACT_PATH, "frog.png")
frogIconPath = os.path.join(ACT_PATH, "frog_icon.png")
tint_frogIconPath = os.path.join(ACT_PATH, "frog_icon_tint.png")

switchImgPath = os.path.join(ACT_PATH, "switch.png")
switchIconPath = os.path.join(ACT_PATH, "switch_icon.png")
tint_switchIconPath = os.path.join(ACT_PATH, "switch_icon_tint.png")
doorImgPath = os.path.join(ACT_PATH, "door.png")
doorIconPath = os.path.join(ACT_PATH, "door_icon.png")
tint_doorIconPath = os.path.join(ACT_PATH, "door_icon_tint.png")

arrowRightPath = os.path.join(ACT_PATH, "arr_right.png")
arrowLeftPath = os.path.join(ACT_PATH, "arr_left.png")
# item types
GRASS = "GRASS"
GRASSLEFT = "GRASSLEFT"
GRASSMID = "GRASSMID"
GRASSRIGHT = "GRASSRIGHT"
GRASSCENTER = "GRASSCENTER"
STONE = "STONE"
WATER = "WATER"
COIN = "COIN"
SLIME = "SLIME"
FLY = "FLY"
FROG = "FROG"
PLAYER = "PLAYER"
SWITCH = "SWITCH"
DOOR = "DOOR"

itemTypeList = [GRASS, GRASSLEFT, GRASSMID, GRASSRIGHT,
                GRASSCENTER, STONE, WATER, COIN, SLIME, FLY, FROG,
                PLAYER, SWITCH, DOOR
               ]

actionItemList = [DOOR, SWITCH]


# Dictionary mapping item type to image path
imgDict = {GRASS: grassBigImgPath, \
           GRASSLEFT: grassLeftImgPath, \
           GRASSMID: grassMidImgPath, \
           GRASSRIGHT: grassRightImgPath, \
           GRASSCENTER: grassCenterImgPath, \
           STONE: stoneBigImgPath, \
           WATER: waterImgPath, \
           COIN: coinImgPath, \
           SLIME: slimeImgPath, \
           FLY: flyImgPath, \
           FROG: frogImgPath, \
           PLAYER: playerImgPath, \
           SWITCH: switchImgPath, \
           DOOR: doorImgPath
          }
