#!/usr/bin/env python

from const import *
import pygame

class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def use_cam(self, target):
        return target.rect.move(self.state.topleft)

    def use_cam_rect(self, tarRect):
        return tarRect.move(-self.state.topleft[0], -self.state.topleft[1])

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


# camera functions

def simple_camera(camera, target_rect):
    left, top, _, _ = target_rect
    _, _, width, height = camera
    return pygame.Rect(-left+HALF_W, -top+HALF_H, width, height)

def complex_camera(camera, target_rect):
    l, t, _, _  = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_W, -t+HALF_H, w, h

    # stop scrolling at edges
    l = min(0, l)
    l = max(-(camera.width - SCREEN_W), l)
    t = max(-(camera.height - SCREEN_H), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)
