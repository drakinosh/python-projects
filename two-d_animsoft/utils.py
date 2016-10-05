#!/usr/bin/env python2

import pygame as pg
import math
import copy

def ultraCopy(bone_list):
    
    new_list = [copy.copy(bone) for bone in bone_list]

    dicto = dict(zip(bone_list, new_list))

    for each in dicto.keys():
        
        par = each.parent

        if par:
            dicto[each].parent = dicto[par]


    return dicto.values()
        
def getNextFrame(current_frame, frame_list):
    
    index = frame_list.index(current_frame)

    try:
        return frame_list[index+1]
    except:
        return current_frame

def getPrevFrame(current_frame, frame_list):
    
    #index = frame_list.index(current_frame)
    index = current_frame.number - 1

    try:
        return frame_list[index-1]
    except:
        return current_frame

def snapToParent(parent_bone, child_bone, signx, signy):
    
    del_x = signx*(child_bone.pos[0] - parent_bone.handle.pos[0])
    del_y = signy*(child_bone.pos[1] - parent_bone.handle.pos[1])

    new_pos = child_bone.handle.pos[0]+del_x,child_bone.handle.pos[1]+del_y
    child_bone.pos = parent_bone.handle.pos
    child_bone.updateHandle(new_pos)


def getDelta(pos1, pos2):
    
    return pos1[0] - pos2[0], pos1[1] - pos2[1]

def snapToParentTranslator(parent_bone, child_bone, signx, signy, initial=False):
    
    # on initial snapping, some adjustments need to be made
    if initial:
        signx = -signx

    del_x, del_y  = getDelta(child_bone.pos, parent_bone.pos)
    del_x, del_y = signx * del_x, signy * del_y
    
    new_pos = child_bone.handle.pos[0] + del_x, child_bone.handle.pos[1]+del_y
    
    child_bone.pos = parent_bone.pos
    child_bone.updateHandle(new_pos)

def distance(pos1, pos2):
    
    return math.sqrt( (pos1[0]-pos2[0])**2 + (pos1[1] - pos2[1])**2)

def getRectCoords(pos, size, circle_rad):
    
    """
    Return coordinates of the main rectangle(i.e. diaphysis) of 
    the bone by adjusting for the coordinates and size of the end-circles
    i.e. the epiphyses

    pos         -> position of bone
    circle_rad  -> atarimae darou?
    """

    left = pos[0]
    top = pos[1] - circle_rad

    width, height = size
    """
    print("GOTT: ")
    print(left, top, width, height)
    """

    return (left, top, width, height)

