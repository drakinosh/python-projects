# Player dictionary
# name corresponds to pid

import pygame as pg
import os
import const as c

class PlayerData:
    
    def __init__(self, name, jump_power, speed, cooldown):
        
        self.name = name
        self.jump_power = jump_power
        self.speed = speed
        self.cooldown = cooldown


sasuke_data = PlayerData("sasuke", 10, 5, 3)
naruto_data = PlayerData("naruto", 12, 4, 2)

pid_dicts = {3 : sasuke_data,
             1 : naruto_data
            }

def getSpeed(pid):
    
    return pid_dicts[pid].speed

def getJumpPower(pid):
    return pid_dicts[pid].jump_power

def getCoolDown(pid):
    return pid_dicts[pid].cooldown

def getRightSprites(suffix, roof, pid):
    
    images_list = []
    # extract name from corresponding data object
    name = pid_dicts[pid].name
    
    # S;N - replace this with glob

    for i in range(1, roof):
        # e.g. sasuke_ridle1.png
        img_name = name + suffix + str(i) + ".png"
        img_path = os.path.join(c.SPRITES_FOLDER, img_name) #portability no tame ni
        image = pg.image.load(img_path)
        images_list.append(image)

    return images_list

def getLeftSprites(imager_list):
    
    imagel_list = list()

    for img in imager_list:
        imgl = pg.transform.flip(img, True, False)
        imagel_list.append(imgl)

    return imagel_list

def getIdlerSprites(pid):
    suffix = "_ridle"
    roof = 7
    
    return getRightSprites(suffix, roof, pid)

def getRunrSprites(pid):
    suffix = "_rrun"
    roof = 7

    return getRightSprites(suffix, roof, pid)

def getJumprSprites(pid):
    suffix = "_rjump"
    roof = 3

    return getRightSprites(suffix, roof, pid)

def getFallrSprites(pid):
    suffix = "_rfall"
    roof = 3

    return getRightSprites(suffix, roof, pid)

def getIdlelSprites(pid):
    
    return getLeftSprites(getIdlerSprites(pid))
    
def getRunlSprites(pid):
    return getLeftSprites(getRunrSprites(pid))

def getJumplSprites(pid):
    
    return getLeftSprites(getJumprSprites(pid))

def getFalllSprites(pid):
    
    return getLeftSprites(getFallrSprites(pid))
