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
import ed_GUI

#Import vars
# MODE - NEW OR EDIT
# Change MODE to change mode of editing

MODE = "NEW"

def switchGenerator():  
    """Return a unique ID for a switch object."""

    num = 1
    while True:
        yield num
        num += 1


def doorGenerator():
    """switchGenerator() for doors."""

    num = 1
    while True:
        yield num
        num += 1

def handleQuit():
    menu.main() #sys.exit() # This will kill the interpreter
    quit()

class Chief:

    def __init__(self, lev_width):

        self.lev_width = lev_width
        self.mainS = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.mouse_state = SAFE
        self.itemGroup = pygame.sprite.Group()
        self.borderRectList = list()
        self.iconGroup = pygame.sprite.Group()
        self.itemExistGroup = pygame.sprite.Group() # final group; written to the level file

        self.cam = scrollerC.Camera(scrollerC.complex_camera, \
                                   lev_width, SCREEN_H - PANEL_H)
        self.straw_man = dummy.Dummy((HALF_W, HALF_W)) # DUMMY FOR CAMERA

        self.right_arrow = arrow.Arrow((SCREEN_W - 40 , 5), RIGHT,\
                                       self.straw_man, self.lev_width, self.mainS)
        self.left_arrow = arrow.Arrow((0, 5), LEFT,\
                                       self.straw_man, self.lev_width,  self.mainS)


        self.curPos = (0, 0)

        self.clock = pygame.time.Clock()
        self.switch_gen = switchGenerator()
        self.door_gen = doorGenerator()
        # FLAGS
        self.DOORFLAG = False   #a switch has been placed

        
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
                    print ("PLAYER ALREADY EXISTS")
                    return

        # Only one door for one switch . If there is no switch ,
        # doors cannot be created.

        if not self.DOORFLAG and itemType == DOOR:
            print("CANNOT PUT A DOOR BEFORE A SWITCH")
            return

        if self.DOORFLAG and itemType != DOOR:
            print("NEXT ITEM MUST BE A DOOR")
            return

        if itemType == SWITCH:
            self.DOORFLAG = True # a switch has been placed
        if itemType == DOOR:
            self.DOORFLAG = False


        image = imgDict[itemType]
        item = ci_C.Item(itemType, CREATE_POS, image, self.mainS)

        # Add special attributes for certain items

        if itemType == SWITCH:
            item.special_attrib = self.switch_gen.next()
        if itemType == DOOR:
            item.special_attrib = self.door_gen.next()

        item.selected = isSelected
        self.itemGroup.add(item)

    def delete_item(self, item):
        """Delete an item."""

        self.itemGroup.remove(item)

        if item in self.itemExistGroup:
            self.itemExistGroup.remove(item)

        # If the item is a door or a switch, special
        # procedures are required.

        # First, the flags are reset and the generator
        # of the complementary item is also incremented
        
        if item.itemType == DOOR:
            self.DOORFLAG = True   
            self.switch_gen.next() 

        elif item.itemType == SWITCH:
            self.DOORFLAG = False
            self.door_gen.next()
    
    def create_icons(self):

        grassIcon = icon.Icon(GRASS, grassIconPath, tint_grassIconPath, \
                             (55, 25), self.mainS)
        grassLeftIcon = icon.Icon(GRASSLEFT, grassLeftIconPath, \
                                 tint_grassLeftIconPath, \
                                 (100, 25), self.mainS)
        grassMidIcon = icon.Icon(GRASSMID, grassMidIconPath, \
                                 tint_grassMidIconPath, \
                                 (140, 25), self.mainS)
        grassRightIcon = icon.Icon(GRASSRIGHT, grassRightIconPath, \
                                  tint_grassRightIconPath, \
                                  (180, 25), self.mainS)
        grassCenterIcon = icon.Icon(GRASSCENTER, grassCenterIconPath, \
                                   tint_grassCenterIconPath, \
                                   (180, 75), self.mainS)

        coinIcon = icon.Icon(COIN ,coinIconPath, tint_coinIconPath, \
                            (240, 25), self.mainS)
        slimeIcon = icon.Icon(SLIME, slimeIconPath, tint_slimeIconPath, \
                             (280, 25), self.mainS)
        flyIcon = icon.Icon(FLY, flyIconPath, tint_flyIconPath, \
                             (320, 25), self.mainS)

        stoneIcon = icon.Icon(STONE, stoneIconPath, tint_stoneIconPath, \
                             (55, 75), self.mainS)
        
        playerIcon = icon.Icon(PLAYER, playerIconPath, tint_playerIconPath, \
                             (360, 25) , self.mainS)
        switchIcon = icon.Icon(SWITCH, switchIconPath, tint_switchIconPath, \
                             (215, 75), self.mainS)
        doorIcon = icon.Icon(DOOR, doorIconPath, tint_doorIconPath, \
                             (275, 75), self.mainS)

        self.iconGroup.add(grassIcon)
        self.iconGroup.add(grassLeftIcon)
        self.iconGroup.add(grassMidIcon)
        self.iconGroup.add(grassRightIcon)
        self.iconGroup.add(grassCenterIcon)
        self.iconGroup.add(coinIcon)
        self.iconGroup.add(slimeIcon)
        self.iconGroup.add(flyIcon)
        self.iconGroup.add(stoneIcon)
        self.iconGroup.add(playerIcon)
        self.iconGroup.add(switchIcon)
        self.iconGroup.add(doorIcon)

    def draw_grid(self, offset):
        """
        Draw grids on the screen.
        The items snap to the grids.
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
        """Dumps item data on a specified file. This method
        is responsible for creating level files. 
        Currently, the following item data are dumped:
            1. X-coordinate of item
            2. Y-coordinate of item
            3. Special attributes of item, if any.(None by default)
        """

        itemDict = dict()

        for item in self.itemExistGroup:
            itemDict[item.itemType] = list()

        for item in self.itemExistGroup:
            itemDict[item.itemType].append(
              (item.rect.x, item.rect.y - PANEL_H, item.special_attrib))

        itemDict["LEVELWIDTH"] = self.lev_width
        with open(itemDictFile, 'w') as myFile:
            p.dump(itemDict, myFile)
        parser.write_level()

    def mainloop(self):
        """
        The Mainloop for the editor.
        (offset) is a tuple that stores the total x and y offsets
            for the editor.
        (clicked) is a variable that stores the state of the mouse
        
        The other varaibles are self-explanatory.
        """

        offset = [0, 0]  # total offset for grid
        right_off = 0 # right_arrow's offset
        left_off = 0 # left_arrow's offset

        while True:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    handleQuit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # left button
                        clicked = True
                        for item in self.itemGroup:
                            if item.selected and self.mouse_state == SAFE:
                                item.selected = False

                        self.check_icons()
                    
                    elif event.button == 3: # right click
                        
                        # Deletes a temporary item
                        for item in self.itemGroup:
                            if item.selected and self.mouse_state == SAFE:
                                self.delete_item(item)
                       
                        # Selects and deletes a 'written' item
                        for perm_item in self.itemExistGroup:
                            # We need to apply the camera to the cursor first
                            newCurPos = (self.curPos[0]+offset[0], self.curPos[1])

                            if perm_item.rect.collidepoint(newCurPos):
                                self.delete_item(perm_item)

                       

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
            self.draw_grid(offset[0])
            self.maintain_list()
            self.check_mouse_state()

            self.itemGroup.update(offset[0], self.mouse_state)
            for each in self.itemGroup:
                self.mainS.blit(each.image, self.cam.use_cam(each))

            for rect in self.borderRectList:
                pygame.draw.rect(self.mainS, GREY, rect)

            right_off = self.right_arrow.update(self.curPos, clicked)
            left_off = self.left_arrow.update(self.curPos, clicked)
            
            # Adjust horizontal offset
            if (right_off + left_off != 0):
                offset[0] +=  right_off + left_off

            self.iconGroup.update()
            pygame.display.update()
            self.clock.tick(FPS)

def editLevel(fileName):
    data_list = parser.read_level_file(fileName)

    for token in data_list:
        if token == "LEVELWIDTH":
            lw = data_list[data_list.index("LEVELWIDTH")+1]


    inst = Chief(int(lw))
    
    # Recreate an editable level from the given file

    ind = -1
    for itemType in data_list:
        ind += 1
        if itemType in itemTypeList:
            # Need to account for panel when 
            # extracting coordinates
            pos = int(data_list[ind+1]), int(data_list[ind+2]) + PANEL_H
            item = ci_C.Item(itemType, pos, imgDict[itemType],
                             inst.mainS)

            # for action items, add action ids
            if itemType in actionItemList:
                item.special_attrib = int(data_list[ind+3])

            inst.itemGroup.add(item)
            inst.itemExistGroup.add(item)
    inst.mainloop()

def newLevel(lw):

    assert lw >= SCREEN_W, "TOO SMALL"
    inst = Chief(lw)
    inst.mainloop()
 
def main():
    
    ed_GUI.main()


if __name__ == '__main__':
    main()
