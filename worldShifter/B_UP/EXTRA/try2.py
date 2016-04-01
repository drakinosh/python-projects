#!/usr/bin/env python

import pygame, sys
import spriteHandler
import playerC, platformC, normC
from const import *
import time

SIZE_TUPLE = (500, 500)
ORIGIN = (250, 250)

def terminate():
    pygame.quit()
    sys.exit()

def add_platforms(platG):
    w = platformC.Platform.width
    plat1 = platformC.Platform((200, 400), ORIGIN)
    plat2 = platformC.Platform((275, 400), ORIGIN)

    liste = list()

    for i in range(0, SIZE_TUPLE[0] / 25 ):
        liste.append(normC.NormPlat((i * 25, SIZE_TUPLE[1] - 25)))


    normG = pygame.sprite.Group(liste)

 
    platG.add(plat1)
    platG.add(plat2)

    return platG, normG
    

def main():
    pygame.init() 
    pygame.display.set_mode(SIZE_TUPLE)
    mainS = pygame.display.get_surface()
    platformGroup = pygame.sprite.Group()
    platformGroup, normGroup = add_platforms(platformGroup)
    checkGroup = platformGroup.copy()
    checkGroup.add(normGroup)
    playa = playerC.Player((200, 200))
    clock = pygame.time.Clock()

    nowTime = 0 # current time
    timeSum = 0 # sum of time

    while True:
        for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        terminate()
	    elif event.type == pygame.KEYDOWN:
	        if event.key == pygame.K_SPACE:
		    playa.jump()

        keys = pygame.key.get_pressed()

        mainS.fill(BLUE)
	OUTLIST = playa.update(keys, checkGroup)
	#playa.canShift = False # remove player's ability to shift gravity
	playa.draw(mainS)

	doRotate = OUTLIST[0]
        nowTime = OUTLIST[1] # get current time
	mainTime = time.time()
	timeSum += mainTime - nowTime
        
	#print "TIMERAME ", timeSum - (mainTime - nowTime)
	# toogle canShift on if sufficient time has passed
        if (timeSum - (mainTime - nowTime) > 0.04):
	    timeSum = 0              # reset counter
	    playa.canShift = True

        platformGroup.update(mainS, doRotate)
	normGroup.draw(mainS)
	pygame.display.update()
	clock.tick(60)


main()
        
        
        

