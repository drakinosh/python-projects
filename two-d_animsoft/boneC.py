#!/usr/bin/env python

import pygame as pg
import constants as const
import utils
import miscC
import math

class Bone:
    
    def __init__(self, pos, parent_bone, mainS):
        
        # step1: handle everything parent-child related
        self.parent = parent_bone
        self.children_list = list()

        if self.parent:
            self.parent.children_list.append(self)

        self.parenting_code = 0   # parenting code for joining bones

        self.wunderkind = False  # True if attached to translator
        # step2: define all necessary paramters

        self.size = const.DEF_BONE_SIZE
        self.bone_rad = const.DEF_BONE_RAD
        self.pos = pos
        self.angle = 0       # rotation angle  
        self.del_angle = 0

        self.type = const.TYPE_BONE

        self.grabbed = False    # grabbed by the cursor
        self.selected = False   # selected by cursor for possible parenting

        self.rect_coords = utils.getRectCoords(self.pos, self.size,
                                                self.bone_rad)

        self.mainS = mainS

        self.handle_pos = (self.pos[0] + self.size[0], self.pos[1])

        # unpack returned tuple
        self.rekkuto = pg.Rect(*self.rect_coords)
        
        self.handle = miscC.PivotHandle(self, self.handle_pos, mainS)
        self.pivot_point = self.pos

        self.getPosRect()

    def getPosRect(self):
        
        self.pos_rect = pg.Rect(self.pos[0]-self.bone_rad, self.pos[1]-self.bone_rad,
                                2 * self.bone_rad, 2 * self.bone_rad)

    def rotate(self, new_handle_pos, angle=None):
        
        if angle is not None:
            ang = angle
        else:
            del_y = new_handle_pos[1] - self.pivot_point[1]
            del_x = new_handle_pos[0] - self.pivot_point[0]
            ang = math.atan2(del_y, del_x)

        self.del_angle = self.angle - ang
        self.angle = ang

        if const.DEBUG:
            print("Angle ha {}".format(math.degrees(ang)))

        # note: kore ha nantoka shiro!
        # this approximation may screw things up

        new_x = self.size[0] * math.cos(self.angle)
        new_y = self.size[0] * math.sin(self.angle)
        

        #print("DEL {}".format((del_x, del_y)))

        new_x, new_y = int(new_x), int(new_y)

        self.handle.rect.move(new_x, new_y)

        self.updateHandle((self.pivot_point[0] + new_x, self.pivot_point[1] + new_y))


        self.propagateRotation(self.del_angle)

    def propagateRotation(self, del_ang):
        
        if self.children_list:
            for child in self.children_list:
                
                # do not rotate a special child
                if child.wunderkind:
                    continue        

                # assign new position
                child.pos = self.handle.pos

                # actually propagate rotation
                child.rotate(None, child.angle - del_ang)

                new_del = child.del_angle - del_ang
                # propagate to grandchildren, too
                child.propagateRotation(new_del)

    def propagateTranslation(self):
        
        if self.children_list:
            for child in self.children_list:
                
                if not child.wunderkind:
                    utils.snapToParent(self, child, -1, -1)
                else:
                    utils.snapToParentTranslator(self, child, -1, -1)


                # propagate to grandchildren, too

                child.propagateTranslation()
                

    def updateHandle(self, coords):

        self.handle_pos  = coords
        self.handle.update(self.handle_pos)

        # also update pivot points
        self.pivot_point = self.pos
        self.getPosRect()

    def drawExtra(self):
        
        self.handle.draw()

    def draw(self):

        self.circle1 = pg.draw.circle(self.mainS, const.COL_BLACK, self.pos,
                                      self.bone_rad)
        #self.rect = pg.draw.rect(self.mainS, const.COL_BLACK, self.rekkuto)

        pg.draw.line(self.mainS, const.COL_BLACK, self.pos, self.handle_pos,
                     self.bone_rad * 2)

        self.circle2 = pg.draw.circle(self.mainS, const.COL_BLACK, 
                                     self.handle_pos,
                                     self.bone_rad)



class ChiefBone(Bone):
    
    def __init__(self, pos, mainS):
        
        Bone.__init__(self, pos, None, mainS)

        self.type = const.TYPE_CHIEF_BONE
        self.translator = miscC.Translator(self, self.pos, self.mainS)

        self.trans_grabbed = False  # grabbed for translation
        self.SP_SEL = False         # Special select

    def translate(self, curPos):
    
        del_x = self.pos[0] - curPos[0]
        del_y = self.pos[1] - curPos[1]

        del_x, del_y = -del_x, -del_y

        self.pos = curPos

        new_pos = self.handle.pos[0] + del_x, self.handle_pos[1] + del_y

        self.translator.update(self.pos)

        self.updateHandle(new_pos)

        self.propagateTranslation()


    def drawExtra(self):
        
        self.translator.draw()
        self.handle.draw()

