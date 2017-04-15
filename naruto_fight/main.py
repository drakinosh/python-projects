#!/usr/bin/env python2

import pygame as pg
import player
import blocks
import const as c
import sys

def handleQuit():
    pg.quit()
    sys.exit()


def main():
    
    pg.init()
    pg.mixer.init()

    pg.display.set_mode((c.SCREEN_W, c.SCREEN_H))
    mainS = pg.display.get_surface()
    obsGroup = pg.sprite.Group()

    clock = pg.time.Clock()

    sasuke = player.Player(3, (200, 200), c.RIGHT)

    # Create lots of blocks
    for i in range(0, c.SCREEN_W, 50):
        block = blocks.Block((i, c.SCREEN_H-50))
        obsGroup.add(block)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                handleQuit()

        keys = pg.key.get_pressed()
        mainS.fill(c.BLUE)
        sasuke.update(obsGroup, keys, mainS)

        pg.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
