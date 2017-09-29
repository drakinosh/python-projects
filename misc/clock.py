#!/usr/bin/env python

#A program that creates a digital clock to display
#The current time.

#A program by Sanskar Chand, 16.5 Years old
#2015-05-27 C.E., Wednesday, 0405(GMT+5:45)
#Written at the moment of near-completion.

import pygame, sys
import datetime

screen_h = 160
screen_w = 400

#Colours
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SILVER = (192, 192, 192)
DEFCOL = BLUE
OFFSET = 100

#THE LAYOUT OF THE CLOCK IS:
'''
    0
  1   3
    2
  4   6
    5
'''
pygame.init()

#Width and height of horizontal piece
w= 15
h=45

myDisp = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("DIGITARU CLOCK - Sanskar Chand")

#Represents width and height values for vertical and horizontal 'bits'
li = [[h,w], [w,h], [h,w], [w, h], [w,h], [h,w], [w, h]]


#Boolean values for each bit in a number, serially
valDict = {
          '0':[True, True, False, True, True, True, True],
          '1':[False, False, False, True, False, False, True],
          '2':[True, False, True, True, True, True, False],
          '3':[True, False, True, True, False, True, True],
          '4':[False, True, True, True, False, False, True],
          '5':[True, True,True, False, False, True, True],
          '6':[True, True, True, False, True, True, True],
          '7':[True, False, False, True, False, False, True],
          '8':[True, True, True, True, True, True, True],
          '9':[True, True, True, True, False, True, True]}

#params: The x and y coordinates of each 'bit' in order
#Only the x-values need to be changed for each digit
#So, this is the base
params = [[w,0], [0,w], [w, w+h], [w+h, w], [0, 2*w+h],
          [w, 2*w+h+h], [w+h, 2*w+h]]

clock = pygame.time.Clock()

myDisp.fill(BLACK)


def displayLet(digit, level):
    '''Displays the given digit with a x-coordinate offset
       measured by levell'''
    valList = valDict[digit]

    for x in range(7):
        checker = valList[x]
        if checker:
            colour = DEFCOL
        else:
            colour = BLACK

        pygame.draw.rect(myDisp, colour, [params[x][0] + (level*OFFSET),\
                         params[x][1], li[x][0], li[x][1]])


def parseTime(string):
    i = -1
    for each in string:
        i += 1

        displayLet(each, i)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Get the time in army format
    timenow = datetime.datetime.now()
    army = timenow.strftime("%H") + timenow.strftime("%M")

    parseTime(army)

    pygame.display.update()
    clock.tick(60)
