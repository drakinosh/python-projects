#!/usr/bin/env python

import math

class Rotator(object):
    def __init__(self, center, origin, image_angle=0):
        """ rotator class """
        x_rel = center[0] - origin[0]
        y_rel = center[1] - origin[1]

        self.radius = math.hypot(x_rel, y_rel)
        self.start_angle = math.atan2(-y_rel, x_rel) - math.radians(image_angle)

    def __call__(self, angle, origin):
        """ returns new positions after rotation"""
        new_angle = math.radians(angle) + self.start_angle
        new_x = origin[0] + self.radius * math.cos(new_angle)
        new_y = origin[1] - self.radius * math.sin(new_angle)
        return (new_x, new_y)
