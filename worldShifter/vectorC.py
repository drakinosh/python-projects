"""
Class Vector
"""

import math

class Vector:
    
    def __init__(self, pos, mag, direc):
        
        """
        Initialiser.
        pos   -> a tuple consisting of an x and a y coordinate.
        mag   -> magnitude of vector
        direc -> direction the vector is pointing to
        """

        self.pos = pos
        self.mag = mag
        self.direc = direc
        self.x = pos[0]
        self.y = pos[1]

    def __add__(self, vec2):
        pass

