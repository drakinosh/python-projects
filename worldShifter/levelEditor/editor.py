#!/usr/bin/env python

import pygame
import sys
import pickle as p
import clickable_item as ci_C
import icon
from ed_const import *
import parser
import scrollerC
import dummy, arrow
import menu

def handleQuit():
    menu.main()

class Chief:

    def __init__(self, lev_width):

        self.lev_width = lev_width
        self.mainS = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.mouse_state = SAFE
        self.itemGroup = pygame.sprite.Group()
        self.borderRectList = list()
        self.iconGroup = pygame.sprite.Group()
        self.itemExistGroup = pygame.sprite.Group()

        self.cam = scrollerC.Camera(scrollerC.complex_camera, \
                                   lev_width, SCREEN_H - PANEL_H)
        self.straw_man = dummy.Dummy((HALF_W, HALF_W)) # DUMMY FOR CAMERA

        self.right_arrow = arrow.Arrow((SCREEN_W - 40 , 5), RIGHT,\
                                       self.straw_man, self.lev_width, self.mainS)
        self.left_arrow = arrow.Arrow((0, 5), LEFT,\
                                       self.straw_man, self.lev_width,  self.mainS)


        self.curPos = (0, 0)

        self.clock = pygame.time.Clock()
        self.create_panels()
        self.create_icons()

        pygame.init()

    def create_panels(self):

        top_panel_rect = pygame.Rect(0, 0, \
                                         SCREEN_W, PANEL_H)
        self.borderRectList.append(top_panel_rect)

    def create_item(self, itemType, isSelected):

        # Only one player there must be - Yoda
        if itemType == PLAYER:
            for item in self.itemGroup:
                if item.itemType == PLAYER:
                    print "PLAYER ALREADY EXISTS"
                    return

        image = imgDict[itemType]
        item = ci_C.Item(itemType, CREATE_POS, image, self.mainS)
        item.selected = isSelected
        self.itemGroup.add(item)

    def create_icons(self):

        grassIcon = icon.Icon(GRASS, grassIconPath, tint_grassIconPath, \
                              (55, 25), self.mainS)
        coinIcon = icon.Icon(COIN ,coinIconPath, tint_coinIconPath, \
                             (100, 25), self.mainS)
        slimeIcon = icon.Icon(SLIME, slimeIconPath, tint_slimeIconPath, \
                             (140, 25), self.mainS)
        stoneIcon = icon.Icon(STONE, stoneIconPath, tint_stoneIconPath, \
                             (55, 75), self.mainS)
        playerIcon = icon.Icon(PLAYER, playerIconPath, tint_playerIconPath, \
                               (SCREEN_W/2, 25) , self.mainS)
        switchIcon = icon.Icon(SWITCH, switchIconPath, tint_switchIconPath, \
                             (205, 75), self.mainS)

        self.iconGroup.add(grassIcon)
        self.iconGroup.add(coinIcon)
        self.iconGroup.add(slimeIcon)
        self.iconGroup.add(stoneIcon)
        self.iconGroup.add(playerIcon)
        self.iconGroup.add(switchIcon)

    def draw_grid(self, offset):
        """
        draw grids on the screen.
        the items snap to the grids
        """

        # draw vertical lines
        for x in range(0, self.lev_width, GRID_W):

            pygame.draw.line(self.mainS, GREY, (x - offset,0), (x - offset, SCREEN_H))

        # draw horizontal lines
        for y in range(0, SCREEN_H, GRID_H):
            pygame.draw.line(self.mainS, GREY, (0,y), (self.lev_width, y))

    def maintain_list(self):
        """
        Does a series of checks to ensure that
        all is well in the list/group of 'written'
        items
        """
        for item in self.itemGroup:
            if not item.selected:
                self.itemExistGroup.add(item)

    def check_mouse_state(self):
        "checks if the mouse is in a SAFE zone"
        self.mouse_state = SAFE

        for rect in self.borderRectList:
            if rect.collidepoint(self.curPos):
                self.mouse_state = RESTRICTED

    def check_icons(self):

        check_val = 0
        check_num = 0

        for icon in self.iconGroup:
            check_num += 1
            if not icon.selected:
                check_val += 1
        cond = (check_val == check_num) # no icons are selected

        for icon in self.iconGroup:

            if icon.rect.collidepoint(self.curPos) and \
              self.mouse_state == RESTRICTED:
                if not icon.selected and cond:
                    icon.selected = True
                    self.create_item(icon.itemType, True)
                else:
                    icon.selected = False

    def dump_data(self):

        itemDict = dict()

        for item in self.itemExistGroup:
            itemDict[item.itemType] = list()

        for item in self.itemExistGroup:
            itemDict[item.itemType].append((item.rect.x, item.rect.y - PANEL_H))

        with open(itemDictFile, 'w') as myFile:
            p.dump(itemDict, myFile)
        parser.write_level()

    def mainloop(self):
        offset = 0 # total offset for grid
        right_off = 0 # right_arrow's offset
        left_off = 0 # left_arrow's offset

        while True:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    handleQuit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    for item in self.itemGroup:
                        if item.selected and self.mouse_state == SAFE:
                            item.selected = False

                    self.check_icons()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        print "OFFSET = ", offset

                    if event.key == pygame.K_q:
                        print "DATA DUMPED!"
                        self.dump_data()
                        handleQuit()
            # Calculate horizontal grid offset

            self.cam.update(self.straw_man)
            self.curPos = pygame.mouse.get_pos()
            self.mainS.fill(WHITE)
            self.draw_grid(offset)
            self.maintain_list()
            self.check_mouse_state()

            self.itemGroup.update(offset, self.mouse_state)
            for each in self.itemGroup:
                self.mainS.blit(each.image, self.cam.use_cam(each))

            for rect in self.borderRectList:
                pygame.draw.rect(self.mainS, GREY, rect)

            right_off = self.right_arrow.update(self.curPos, clicked)
            left_off = self.left_arrow.update(self.curPos, clicked)

            if (right_off + left_off != 0):
                offset +=  right_off + left_off

            self.iconGroup.update()
            pygame.display.update()
            self.clock.tick(FPS)

def main():
    lw = raw_input("ENTER LEVEL WIDTH: ")
    lw = int(lw)

    assert lw >= SCREEN_W, "TOO SMALL"

    inst = Chief(lw)
    inst.mainloop()

if __name__ == '__main__':
    main()
