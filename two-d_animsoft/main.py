#!/usr/bin/env python2

import pygame as pg
import sys
import constants as const
import boneC
import utils

def parent(parent_bone, child_bone):
    
    child_bone.parent = parent_bone
    parent_bone.children_list.append(child_bone)

    # fix pivot points and handle points
    if parent_bone.type == const.TYPE_CHIEF_BONE and parent_bone.SP_SEL:
        utils.snapToParentTranslator(parent_bone, child_bone, 1, -1, True)
        child_bone.wunderkind = True

    else:
        utils.snapToParent(parent_bone, child_bone, 1, -1)
    """
    del_x = (child_bone.pos[0] - parent_bone.handle.pos[0])
    del_y = -(child_bone.pos[1] - parent_bone.handle.pos[1])

    new_pos = child_bone.handle.pos[0] + del_x, child_bone.handle.pos[1] + del_y

    child_bone.pos = parent_bone.handle.pos
    child_bone.updateHandle(new_pos)
    """

    child_bone.parenting_code = 0
    parent_bone.parenting_code = 0

def main():
    
    pg.init()
    clock = pg.time.Clock()
    mainS = pg.display.set_mode(const.SCREEN_SIZE)
    pg.display.set_caption("Pivotix")

    bone0 = boneC.Bone(const.DEF_BONE_POS, None, mainS)

    main_bone = boneC.ChiefBone(const.DEF_CBONE_POS,  mainS)

    bone_list = []
    bone_list.append(bone0)
    bone_list.append(main_bone)

    cur_pos = pg.mouse.get_pos()


    univ_parent_no = 0      # number of bones selected for parenting
    parent_mode = False

    select_mutex = False     # to allow only one bone to be
                            # selected at a time (i.e. layering)
    while True:
        
        cur_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Toggle parent mode using Q

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    parent_mode = not parent_mode
                    print("MODO: {}".format(parent_mode))

                if event.key == pg.K_a:
                    new_bone = boneC.Bone(const.DEF_BONE_POS, None, mainS)
                    bone_list.append(new_bone)

            if event.type == pg.MOUSEBUTTONDOWN:
                
                for each in bone_list:
                    if each.handle.rect.collidepoint(cur_pos):
                        
                        if not select_mutex:
                            select_mutex = True
                            each.grabbed = True

                    if each.type == const.TYPE_CHIEF_BONE:
                        
                        if not select_mutex and each.translator.rect.collidepoint(cur_pos):
                            each.trans_grabbed = True

                            select_mutex = True

                    # for parenting
                    if parent_mode:
                        
                        if univ_parent_no == 0:

                            if each.pos_rect.collidepoint(cur_pos):
                                
                                univ_parent_no = 1
                                each.parenting_code = univ_parent_no

                        elif univ_parent_no == 1:
                            

                            if each.type == const.TYPE_CHIEF_BONE:
                                
                                if each.translator.rect.collidepoint(cur_pos):
                                    each.SP_SEL = True
                                    univ_parent_no = 2
                                    each.parenting_code = univ_parent_no

                            if each.handle.rect.collidepoint(cur_pos):
                                univ_parent_no = 2
                                each.parenting_code = univ_parent_no

            if event.type == pg.MOUSEBUTTONUP:
                
                for each in bone_list:
                    if each.grabbed:
                        each.grabbed = False
                        select_mutex = False

                    if each.type == const.TYPE_CHIEF_BONE and each.trans_grabbed:
                        each.trans_grabbed = False
                        select_mutex = False


        mainS.fill(const.COL_BLUE)

        # Rotate the bones, if any are grabbed
        # Also, draw the bones
        for bone in bone_list:
            
            if bone.grabbed:
                bone.rotate(cur_pos)


            if bone.type == const.TYPE_CHIEF_BONE and bone.trans_grabbed:
                bone.translate(cur_pos)

            bone.draw()

        # Draw the bone handles on top of all others
        for bone in bone_list:
            bone.handle.draw()

        # Draw the translator on top of everything else
        for bone in bone_list:
            if bone.type == const.TYPE_CHIEF_BONE:
                bone.translator.draw()

        # reset all parenting codes if parent_mode is toggle False
        if not parent_mode:
            for bone in bone_list:
                bone.parenting_code = 0

        if parent_mode and univ_parent_no == 2:
            
            for bone in bone_list:
                
                if bone.parenting_code == 1:
                    
                    child_b = bone

                if bone.parenting_code == 2:
                    
                    parent_b = bone

            #if the child bone already has a parent, cancel
            
            if not child_b.parent: 
                parent(parent_b, child_b)

            univ_parent_no = 0
            parent_mode = False


                

        pg.display.update()
        clock.tick(const.FPS)

if __name__ == '__main__':
    main()
