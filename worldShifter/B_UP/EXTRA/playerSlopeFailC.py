#!/usr/bin/env python

import pygame
from const import *
from spriteHandler import SpriteSheet
import time
import math

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        """
	pos   -> position tuple
	platG -> platform Group
	"""
        
	# initialise parent class
	pygame.sprite.Sprite.__init__(self)

	self.x = pos[0]
	self.y = pos[1]
        
	#emergency debug vars
	self.d1 = None
	self.d2 = None
	# state varibles
	self.idle = True
	self.walk = False
	self.fall = True

	# attributes
	self.speed = 3
	self.x_vel =0
	self.y_vel = 0
        self.jump_power = 10
        self.health = MAX_PLAYER_HEALTH 
	
	# other attributes
	self.coins = 0

	# animation indices
	self.walkPos = 0
	self.walkFact = 8 # every eigth iteration , fetch next image
	self.animSpeed = 2

        # special attributes
	self.worldShift = False # shifting the world
        self.canShift = True # atarimae darou
        
	# extract walking images
	sheet = SpriteSheet(playWalkPath)

	self.walk_r_list = list()
	self.walk_l_list = list()

	# extract left-facing images
        
	w = 66
	h = 92

	self.coords = [(0, 0, w, h), (67, 0, w, h), (134, 0, w, h), \
                  (0, 93, w, h), (67, 93, 64, h), (132, 93, 72, h), \
		  (0, 187, 70, h), (71, 187, 70, h), (142, 187, 70,h), \
		  (0, 279, 70, h), (71, 279, 70, h)]

        
	for ind in self.coords:
	    image_r = sheet.get_image(*ind).convert() # expand tuple into arugments
	    self.walk_r_list.append(image_r)
	    image_l = pygame.transform.flip(image_r, True, False)
	    self.walk_l_list.append(image_l)
        
	# startup values
	self.rightIdleImg = self.walk_r_list[0]
	self.leftIdleImg = self.walk_l_list[0]
	self.image = self.rightIdleImg
	self.direction = RIGHT
	self.rect = self.image.get_rect(topleft=pos) # set correct position

        self.OUTLIST = [False, 0.00] # isShifting, time
    def check_keys(self, keys):
        
        self.x_vel = 0

	if keys[pygame.K_RIGHT]:
	    self.walk = True
	    #self.idle = False
	    self.direction = RIGHT
	    self.x_vel  += self.speed
	
	if keys[pygame.K_LEFT]:
	    self.walk = True
	    #self.idle = False
	    self.direction = LEFT
	    self.x_vel -= self.speed
	
	if keys[pygame.K_SPACE]:
	    self.jump()
        
	if keys[pygame.K_q]:
	    if self.canShift:
	        self.OUTLIST[0] = True
		self.worldShift = True
		self.canShift = False
	    else:
	        self.OUTLIST[0] = False
        

	if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
	    self.idle = True
	    self.walk = False
	    self.x_vel = 0

  

    def animate(self, imageList, animPos,  animFact):
        if animPos % animFact == 0:    # timing matches
	    try:                       # set image to appropriate frame
	        self.image = imageList[animPos/animFact]  # change current image
	    except IndexError:
	        animPos = -self.animSpeed  # reset the counter
        animPos += self.animSpeed
	return animPos

    def jump(self):
        if not self.fall:
            self.y_vel = -self.jump_power
            self.fall = True
    
    def check_falling(self, obstacles):
        """ if the player is not in contact with an obstacle, fall """
	self.rect.move_ip((0, 1))
	if not pygame.sprite.spritecollideany(self, obstacles):
	    self.fall = True

	self.rect.move_ip((0, -1))
    
    def get_position(self, obstacles):
        if not self.fall:
	    self.check_falling(obstacles)
	else:
	    self.fall = self.check_collisions((0, self.y_vel), 1, obstacles)
	
	if self.x_vel:
	    self.check_collisions((self.x_vel, 0), 0, obstacles)

    def check_collisions(self, offset, index, obstacles):
        """ checks if a collision would occur after moving offset pixels"""
	unaltered = True
	self.rect.move_ip(offset)

	while pygame.sprite.spritecollideany(self, obstacles):
	    self.rect[index] += (1 if offset[index] < 0 else -1)
	    unaltered = False
	    # stop walking animation
	    if index == 0:
	        self.walk = False
        

	
	return unaltered
    
    def handle_slopes(self, slopeG):
        """
	(Hopefully) handles slope collisions.
	slopeG = slope sprites Group
	NOTE: slopeG must contain homogeneous slopes
	"""
	
        

        colSprite = pygame.sprite.spritecollideany(self, slopeG)
        if colSprite:
	    self.fall = False

	if colSprite and (self.rect.y < colSprite.rect.y):

	    tl = colSprite.rect.topleft # used for slope calculation only
	    br = colSprite.rect.bottomright 
	    
	    m1 = float((br[1]-tl[1])/(br[0]-tl[0]))   # y2-y1/(x2-x1)
	    angle_rad = math.atan(m1)                # from atan(m1 - m1 /(1+m1m2))
	    # The angle is normally 45 degrees 

	    if self.x_vel:
		#le = self.x_vel / abs(self.x_vel) * 4
		le = self.x_vel
	    else: 
		le = 0
		
	    x_move_len = le
	    hypot_len = (x_move_len / math.cos(angle_rad))
	    y_move_len = hypot_len * math.sin(angle_rad)
            

	    self.d1 = x_move_len
	    self.d2 = y_move_len

	    # check collision with any slope
	    
	    #self.rect.move_ip((x_move_len, y_move_len))
            # it seems that the above code is redundant; will check
	    self.rect.move_ip((-self.x_vel, 0)) # undo the shifting
	    self.rect.move_ip((x_move_len, y_move_len))

    def manage_states(self):
        
	# set appropriate animation for walking
        if self.walk and not self.fall:
	    if self.direction == RIGHT:
	        self.walkPos = self.animate(self.walk_r_list, self.walkPos, \
		                            self.walkFact)
	    elif self.direction == LEFT:
	        self.walkPos = self.animate(self.walk_l_list, self.walkPos, \
		                            self.walkFact)
	
	elif self.walk and self.fall:
	    if self.direction == RIGHT:
	        self.image = self.rightIdleImg
	    else:
	        self.image = self.leftIdleImg
	
	elif self.idle or self.fall:
	    if self.direction == RIGHT:
	        self.image = self.rightIdleImg
	    else:
	        self.image = self.leftIdleImg
	
	

    # chief method
    def update(self, keys, obstacles, slopeG):
        
	# current time
	# for toggling the self.canShift
	samaya = time.time()   
        self.OUTLIST[1] = samaya

        self.check_keys(keys)
	self.handle_slopes(slopeG)
	self.get_position(obstacles)
	self.manage_states()

	#self.x += self.x_vel
	#self.rect.x += self.x_vel

	if self.fall:
	    self.y_vel += GRAVITY
	else:
	    self.y_vel = 0
   
        self.x += self.x_vel	
	#self.rect.y += self.y_vel
	#self.y += self.y_vel

        return self.OUTLIST

    def draw(self, surface):
        surface.blit(self.image, self.rect)
       

