#!/usr/bin/env python2

import pygame as pg
import sys
import constants as const
import boneC
import frameC
import utils
import os

from PIL import Image, ImageSequence
import copy
import images2gif
import cPickle as cp

def framenumGen(val=1):
    
    while True:
        yield val
        val += 1

def parent(parent_bone, child_bone):
    
    child_bone.parent = parent_bone
    '''
    parent_bone.children_list.append(child_bone)
    '''

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

    bone0 = boneC.Bone(const.DEF_BONE_POS, None)

    main_bone = boneC.ChiefBone(const.DEF_CBONE_POS)

    bone_list = []
    frame_list = []

    fgen = framenumGen()

    cur_frame = frameC.Frame(fgen.next(),bone_list)

    cur_frame.bone_list.append(bone0)
    cur_frame.bone_list.append(main_bone)
    onion_frame = None
    cur_pos = pg.mouse.get_pos()


    univ_parent_no = 0      # number of bones selected for parenting
    parent_mode = False

    select_mutex = False     # to allow only one bone to be
                            # selected at a time (i.e. layering)

    frame_snap_mode = False # snapping frames

    FPS = const.FPS
    RATE = 16               # animation play framerate
    save_anim = False
    save_ind = -1

    onion_skin = True

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

                if event.key == pg.K_a:
                    new_bone = boneC.Bone(const.DEF_BONE_POS, None)
                    cur_frame.bone_list.append(new_bone)

                if event.key == pg.K_d:
                    
                    new_bone = boneC.CircleBone(const.DEF_BONE_POS, None,
                                                const.DEF_CIRCLE_RAD, const.DEF_THICKN)
                    cur_frame.bone_list.append(new_bone)
                                                    
                if event.key == pg.K_f:
                    #frame_snap_mode = not frame_snap_mode

                    # handle onionskin
                    frame_snap_mode = True

                if event.key == pg.K_e:
                    cur_frame = utils.getNextFrame(cur_frame, frame_list)

                if event.key == pg.K_w:
                    cur_frame = utils.getPrevFrame(cur_frame, frame_list)


                if event.key == pg.K_p:
                    print("Saving animation...")
                    save_anim = True

                if event.key == pg.K_t:
                    print("Some select debug stats...")
                    print("Frame snap mode {}".format(frame_snap_mode))
                    print("Select mutex {}".format(select_mutex))

                if event.key == pg.K_s:
                    
                    fname = raw_input("Provide filename: ")
                    utils.saveFramelist(fname, frame_list)

                if event.key == pg.K_l:
                    
                    fname = raw_input("Provide filename: ")
                    frame_list = utils.loadFramelist(fname)
                    cur_frame = frame_list[0]
                    print("Successful load from file %s" % fname)

        

            if event.type == pg.MOUSEBUTTONDOWN:
                
                for each in cur_frame.bone_list:
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
                
                for each in cur_frame.bone_list:
                    if each.grabbed:
                        each.grabbed = False
                        select_mutex = False

                    if each.type == const.TYPE_CHIEF_BONE and each.trans_grabbed:
                        each.trans_grabbed = False
                        select_mutex = False


        mainS.fill(const.COL_WHITE)



        # At the lowest layer, draw onionskin
        if onion_skin and not save_anim:

            if onion_frame is not None:
                for bone in onion_frame.bone_list:
                    bone.draw(mainS, True)

        # Rotate the bones, if any are grabbed
        # Also, draw the bones

        for bone in cur_frame.bone_list:
            

            # rotation for original bone
            if bone.grabbed:
                bone.rotate(cur_pos)
            else:
                if not bone.parent:
                    bone.rotating = False

            # for child bones
            if bone.parent:
                
                if bone.parent.translating:
                    
                    bone.childTranslate()
                else:
                    bone.translating = False
                
                if not bone.grabbed:
                    
                    if bone.parent.rotating:
                        bone.childRotate(bone.parent.del_angle)
                    else:
                        bone.rotating = False

                
            
            if bone.type == const.TYPE_CHIEF_BONE:
                if bone.trans_grabbed:
                    bone.translate(cur_pos)
                    bone.translating = True
                else:
                    bone.translating = False

            bone.draw(mainS)

        # Draw the bone handles on top of all others
        # only in editing mode, though
        if not save_anim:
            for bone in cur_frame.bone_list:
                bone.handle.draw(mainS)

            # Draw the translator on top of everything else
            for bone in cur_frame.bone_list:
                if bone.type == const.TYPE_CHIEF_BONE:
                    bone.translator.draw(mainS)

        # reset all parenting codes if parent_mode is toggle False
        if not parent_mode:
            for bone in cur_frame.bone_list:
                bone.parenting_code = 0

        if parent_mode and univ_parent_no == 2:
            
            for bone in cur_frame.bone_list:
                
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

        # 'mode' may be a bit misleading
        # the following conditional block instantaneously
        # saves the current frame.
        # in addition, it also assigns the current frame
        # to onion_frame

        if frame_snap_mode:

            # We need to deselect all the bones to avoid continuity
            # errors in the next frame or after playing the animation
            # IMPORTANT: select_mutex should also be set to False

            select_mutex = False
            for bone in cur_frame.bone_list:
                bone.grabbed = False

                if bone.type == const.TYPE_CHIEF_BONE:
                    bone.trans_grabbed = False
            
            # add current frame to list
            frame_list.append(cur_frame)
            onion_frame = cur_frame
            # create new frame from existing one
            # copy the list
            
            #new_bone_list = copy.deepcopy(cur_frame.bone_list)
            new_bone_list = utils.ultraCopy(cur_frame.bone_list)


            new_f = frameC.Frame(fgen.next(), new_bone_list)

            #pg.image.save(mainS, "frame.jpeg")
            

            # now this frame is the current one
            cur_frame = new_f

            frame_snap_mode = False

        # To save an animation, each frame is loaded i.e. assigned to cur_frame
        # and each frame is saved seperately
        # The whole exception-catching business is for loading
        # the fist frame.

        # Also, during saving, the animation is played 
        # by changing the FPS value
        if save_anim:
            
            if save_ind == -1:
        
                name = raw_input("name>> ")
                os.mkdir(name)
                FPS = RATE

            try:
                cur_frame = frame_list[save_ind]
                path = os.path.join(name, str(cur_frame.number)+".jpeg")

                pg.image.save(mainS, path)
                save_ind += 1

            except IndexError:
                save_ind += 1

            if save_ind - 1 == len(frame_list):
                save_anim = False
                save_ind = -1
                FPS = const.FPS

                cur_frame = frame_list[-1]

                '''
                print("Creating gif....")

                
                path = os.path.join(name, str(frame_list[0].number)+".jpeg")
                img = Image.open(path)

                frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
                

                images2gif.writeGif("anim.gif", frames, 0.5)
                '''

        clock.tick(FPS)

if __name__ == '__main__':
    main()
