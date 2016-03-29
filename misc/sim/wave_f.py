#!/usr/bin/env python

'''
@desc A wave simulator that simulates particles
      in wave motion using mathematical functions.
'''

import pygame
import math
import time
import sys 
import random as r
#CONSTANTS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
x = range(0, 255)

SURPRISE = (r.choice(x), r.choice(x), r.choice(x))

COLOUR = SURPRISE

SCREENSIZE = (640, 480)
FPS = 60

C_AMP = 75
C_FREQ = 2
C_WAVELENGTH = 400

class Dummy:
    
    def __init__(self, pos):
        
	self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

class Particle:
    
    def __init__(self, pos, amp, freq, wavelength):
        """
	Initialiser.
	pos - position on screen
	amp - amplitude of corresponding wave
	freq - frequency of wave
	wavelength - atarimae darou?

	FMLA: y = a.sin(wt - 2*pi*x/lambda)

	"""
        
	self.pos = pos
	self.x = self.pos[0]
	self.y = self.pos[1]
        self.mean_y = self.y
	self.radius = 10
        self.colour = COLOUR

	# Compute no of cycles
	self.c_s = False # cycle start
	self.c_t = False # cycle terminate
        self.c_n = 0

	self.a = amp
	self.f = freq
	self.w = 2 * math.pi * freq # angular frequency(omega)
	self.l = wavelength
	self.phi = (2 * math.pi * self.x) / (self.l) # phase difference(phi)
        
	self.y_disp = 0 # y-displacement from mean position
        
	self.dummy = Dummy(pos)
	self.rect = pygame.Rect(pos[0], pos[1], self.radius, self.radius)


    def calculate_position(self, t):
        """
	This function calculates the vertical
	position after time t.
	"""

	self.y_disp = self.a * math.sin((self.w * t) - self.phi)
       	
	#note; since the particles slide off and 
	#pygame does not accept floating point values(obviously, for pixels),
	#the following is an attempt to fix this
        ''' 
	if self.y_disp > self.a:
	    self.y_disp = self.a
	    self.c_n += 0.5

	elif self.y_disp < -self.a:
	    self.y_disp = -self.a
	    self.c_n += 0.5
        '''
	# The dummy object is for 'snapping' the corresponding
	# particle to its mean position.
	# Although this may affect the accuracy of the wave motion, it 
	# keeps the particles from sliding off.

        if self.rect.colliderect(self.dummy.rect):
	    self.y = self.mean_y

	self.y += int(self.y_disp) # update position

    def update(self, mainS, t):
        
	self.calculate_position(t)

        # draw self
	pygame.draw.circle(mainS, self.colour, (self.x, self.y), self.radius)


def main():

    time1 = time.time() # 'zero' time 
    
    pygame.init()
    mainS = pygame.display.set_mode(SCREENSIZE)
    clock = pygame.time.Clock()

    # create particles
    part_list = []

    for i in range(60, 600, 20):
        particle = Particle((i, 300), C_AMP, C_FREQ, C_WAVELENGTH)
	part_list.append(particle)

    # mainloop
    while True:
        
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        pygame.quit()
		sys.exit()
	    
	    if event.type == pygame.KEYDOWN:
	        if event.key == pygame.K_z:
		    print part_list[0].y_disp, part_list[0].phi
                elif event.key == pygame.K_x:
		    l = len(part_list)
		    sub_l = part_list[l/2: l/2 + 5]

		    for each in sub_l:
		        each.colour = WHITE


	time2 = time.time()
	t = time2 - time1
	t = t / 100

	mainS.fill(BLACK)
        
	for particle in part_list:
	    particle.update(mainS, t)
	
	pygame.display.update()
	clock.tick(FPS)


if __name__ == '__main__':
    print "AMP: %d \nFREQ: %d \nWAVELEN: %d \n" % (\
          C_AMP, C_FREQ, C_WAVELENGTH)

    main()

