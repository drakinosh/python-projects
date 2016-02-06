#!/usr/bin/env python

import pygame, sys
import spriteHandler
import playerC, platformC, normC
import enemyC, scrollerC
from const import *
import time
import HUD
import itemsC, cursorC
from levelEditor import parser
import landscapeC
import menu

ORIGIN = (SCREEN_W / 2, SCREEN_H/2)


def getCoords(liste, ind):
    
    return int(liste[ind+1]), int(liste[ind+2])


def handleQuit():
    menu.main()
    quit()

def terminate():
    pygame.quit()
    sys.exit()

def toogleItemState(item, checkList):
    """
    Toogle the state of an item based on a list of
      objects.
    Currently, it is used only for doors and switches.
    """
    for each in checkList:
        if each.action_id == item.action_id:
            if each.used:
                item.open = True
            else:
                item.open = False
                            

def add_platforms(platG, liste):
    """
    Create platforms by parsing the level data.
    NOTE: This function, ironically, does not use the 
        parser module.

    """

    w = platformC.RotPlatform.width
    nl = list()
    ind = -1
    for each in liste:
        ind += 1
        if each == 'GRASS':
            coords = getCoords(liste, ind)
            platG.add(platformC.Platform(coords, grassPath))

        elif each == "GRASSLEFT":
            coords = getCoords(liste, ind)
            platG.add(platformC.Platform(coords, grassLeftPath))
        
        elif each == "GRASSMID":
            coords = getCoords(liste, ind)
            platG.add(platformC.Platform(coords, grassMidPath))

        elif each == "GRASSRIGHT":
            coords = getCoords(liste, ind)
            platG.add(platformC.Platform(coords, grassRightPath))

        elif each == "GRASSCENTER":
            coords = getCoords(liste, ind)
            platG.add(platformC.Platform(coords, grassCenterPath))

        elif each == 'STONE':
            coords = int(liste[ind+1]), int(liste[ind+2])
            platG.add(platformC.RotPlatform(coords, stonePath, ORIGIN))
    '''
    for i in range(32):
        nl.append(normC.NormPlat((i * 50, 475)))
    '''

    normG = pygame.sprite.Group(nl)



    return platG, normG

def add_enemy(liste):
    e_list = list()
    ind = -1
    for each in liste:
        ind += 1
        if each == 'SLIME':
            enem = enemyC.Slime((int(liste[ind+1]), int(liste[ind+2])), LEFT)
            e_list.append(enem)

        elif each == 'FLY':
            enem = enemyC.Fly((int(liste[ind+1]), int(liste[ind+2])), LEFT)
            e_list.append(enem)

        elif each == 'FROG':
            coords = getCoords(liste, ind)
            enem = enemyC.Frog(coords, LEFT)
            e_list.append(enem)

    return e_list

def add_action_items(liste):
    
    s_list = list()
    ind = -1
    for each in liste:
        ind += 1
        if each == 'SWITCH':
            s = landscapeC.Switch((int(liste[ind+1]), int(liste[ind+2])), \
                                   int(liste[ind+3]))
            s_list.append(s)
    return s_list

def add_other_items(liste):
    """
    Add other items like doors and so on.
    """
    m_list = list()
    ind = -1
    for each in liste:
        ind += 1
        if each == 'DOOR':
            coords = int(liste[ind+1]), int(liste[ind+2]) 
            action_id = int(liste[ind+3])
            m = landscapeC.Door(coords, action_id)
            m_list.append(m)


    return m_list
def create_collectible_items(coll_itemG, liste):

    ind = -1
    for each in liste:
        ind += 1
        if each == 'COIN':
            coin = itemsC.Coin((int(liste[ind+1]), int(liste[ind+2])))
            coll_itemG.add(coin)

        elif each == 'KEY':
            key = itemsC.Key((int(liste[ind+1]), int(liste[ind+2])))
            coll_itemG.add(key)

    return coll_itemG

def add_slopes(slopeG):

    return slopeG

def create_main(liste):
    ind = -1
    for each in liste:
        ind += 1
        if each == 'PLAYER':
            return playerC.Player((int(liste[ind+1]), int(liste[ind+2])))

def get_coords(liste):
    ind = -1
    for each in liste:
        ind += 1
        if each == "SCREENSIZE":
            return int(liste[ind+1]), int(liste[ind+2])
def main():
    pygame.init()
    pygame.mixer.init()

    #GET THE LIST
    liste = parser.parse_level()
    
    pygame.display.set_mode(get_coords(liste))
    mainS = pygame.display.get_surface()
    platformGroup = pygame.sprite.Group()
    platformGroup, normGroup = add_platforms(platformGroup, liste)
    checkGroup = platformGroup.copy()
    checkGroup.add(normGroup)
    #playa = playerC.Player((100, 200))
    playa = create_main(liste)

    enem = add_enemy(liste)
    enemGroup = pygame.sprite.Group(enem)
    #enemGroup.add(enem)

    # Create collectible items
    coll_itemG = pygame.sprite.Group()
    coll_itemG = create_collectible_items(coll_itemG, liste)

    slopeGroup = pygame.sprite.Group()
    slopeGroup = add_slopes(slopeGroup)
     
    actionG = add_action_items(liste)
    actionG = pygame.sprite.Group(actionG)

    otherG = add_other_items(liste)
    otherG = pygame.sprite.Group(otherG)

    clock = pygame.time.Clock()

    nowTime = 0 # current time
    timeSum = 0 # sum of time
    sp_blitpos = None
    myCam = scrollerC.Camera(scrollerC.complex_camera, level_w, level_h)

    #HUD
    myBar = HUD.HealthBar((10, 0))
    myCoinHUD = HUD.itemHUD(coinHUDPath, GOLD,(10, myBar.h + 10))
    myKeyHUD = HUD.itemHUD(keyHUDPath, GREEN, (myCoinHUD.rect.width+64, myBar.h + 10))

    myCursor = cursorC.Cursor()
    pygame.mouse.set_visible(False) # hide the actual mouse
    
    #DUMMY DATA
    OUTLIST = [0, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handleQuit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playa.jump()
                elif event.key == pygame.K_z:
                    
                    for enem in enemGroup:
                        if isinstance(enem, enemyC.Frog):
                            print("{} {}", enem.y_vel, enem.mutex)

                elif event.key == pygame.K_x and playa.action_contact:
                    if playa.action_obj.type == 'SWITCH':
                        playa.action_obj.used = not playa.action_obj.used

                # DEBUG INFO
                elif event.key == pygame.K_w:
                    
                    print(" PL {}   MS {}".format(playa.rect.center,
                                                  playa.intMousePos))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                playa.shoot_fire(myCam)
                myCursor.clicked = True

        keys = pygame.key.get_pressed()
        curPos = pygame.mouse.get_pos()
        mainS.fill(BLUE)

        # Main updates
        OUTLIST = playa.update(keys, myCam, mainS, checkGroup, actionG, slopeGroup)
        myCam.update(playa)
        #playa.canShift = False # remove player's ability to shift gravity

        doRotate = OUTLIST[0]
        nowTime = OUTLIST[1] # get current time
        mainTime = time.time()
        timeSum += mainTime - nowTime

        # toogle canShift on if sufficient time has passed
        if (timeSum - (mainTime - nowTime) > 0.04):
            timeSum = 0              # reset counter
            playa.canShift = True

        platformGroup.update(mainS, doRotate)

        enemGroup.update(checkGroup, playa.powerGroup, playa)

        #check for dead enems
        for enemy in enemGroup:
            if not enemy.alive:
                enemGroup.remove(enemy)

        coll_itemG.update(playa)
        for item in coll_itemG:
            if item.consumed:
                coll_itemG.remove(item)

        actionG.update()
        otherG.update()

        switch_actlist = []
        for item in actionG:
            if item.type == "SWITCH":
                switch_actlist.append(item)

        for item in otherG:
            if item.type == "DOOR":
                toogleItemState(item, switch_actlist)
        
        # apply camera
        for each in checkGroup:
            mainS.blit(each.image, myCam.use_cam(each))
        sp_blitpos = myCam.use_cam(playa)

        for enemy in enemGroup:
            mainS.blit(enemy.image, myCam.use_cam(enemy))

        for item in coll_itemG:
            mainS.blit(item.image, myCam.use_cam(item))

        for slope in slopeGroup:
            mainS.blit(slope.image, myCam.use_cam(slope))
        
        for each in actionG:
            mainS.blit(each.image, myCam.use_cam(each))

        for each in otherG:
            mainS.blit(each.image, myCam.use_cam(each))
                 
        mainS.blit(playa.image, myCam.use_cam(playa))
        myCoinHUD.update("coins", playa, mainS)
        myKeyHUD.update("keys", playa, mainS)
        myBar.update(playa.health, mainS)
        myCursor.final(mainS, curPos)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()

