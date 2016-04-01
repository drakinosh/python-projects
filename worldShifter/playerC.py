#!/usr/bin/env python
import pygame
from const import *
from spriteHandler import SpriteSheet
import time
import math
import powersC


#note:
#in the attributes, those that are marked * are handled externally

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
        self.fall = False
        self.climb = False # for ladders and such
        self.climb_mobility = True # moving up  and down
        self.action_contact = False # in contact with a switch or such
        self.water_contact = False # in contact with water

        # attributes
        self.speed = 3
        self.x_vel = 0
        self.y_vel = 0
        self.jump_power = 10
        self.health = MAX_PLAYER_HEALTH
        self.ammo = 50  # No of fireballs
        self.canShoot = True # can shoot fireball

        # item-related attributes
        self.coins = 0
        self.keys = 0

        # animation indices
        self.walkPos = 0
        self.walkFact = 8 # every eigth iteration, fetch next image
        self.animSpeed = 2

        # special attributes
        self.worldShift = False # shifting the world
        self.canShift = True # atarimae darou
        self.prev_slope = False

        self.d1 = self.d2 = 0 # for debugging purposes only
        # extract walking images
        sheet = SpriteSheet(playWalkPath)

        # timers for abilities
        self.timer_fire  = 0
        self.timer_allstop = 0

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

        self.powerGroup = pygame.sprite.Group()
        self.action_obj = None  # stores currently-touching action obj


        # IGNORABLE VARS
        self.intMousePos = (0, 0)

    def check_keys(self, keys):

        self.x_vel = 0

        if keys[pygame.K_d]:
            self.walk = True
            #self.idle = False
            self.direction = RIGHT
            self.x_vel  += self.speed
            if self.climb:
                self.climb = False

        elif keys[pygame.K_a]:
            self.walk = True
            #self.idle = False
            self.direction = LEFT
            self.x_vel -= self.speed
            if self.climb:
                self.climb = False

        elif keys[pygame.K_s]:
            if self.water_contact:
                self.y_vel += WATER_DOWN_SPEED

        # for climbing
        if self.climb and self.climb_mobility:
            if keys[pygame.K_w]:
	            self.rect.move_ip((0, -2))
            elif keys[pygame.K_s]:
		        self.rect.move_ip((0, 2))


        if keys[pygame.K_q]:
            if self.canShift:
                self.OUTLIST[0] = True
                self.worldShift = True
                self.canShift = False
            else:
                self.OUTLIST[0] = False


        if not (keys[pygame.K_d] or keys[pygame.K_a]):
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


    def get_shoot_angle(self, curPos):
        " Return direction in which to shoot fireballs."
        
        """
        if self.direction == RIGHT:
            x1, y1 = self.rect.midright
        else:
            x1, y1 = self.rect.midleft
        """

        x1, y1 = self.rect.center
        x2, y2 = curPos

        x_mag, y_mag = x1-x2, y1-y2

        if x_mag != 0:
            angle = math.atan2(y_mag, x_mag)
        else:
            angle = 0


        return angle

    def is_good_angle(self, angle):
        range1 = range(318, 361)
        range2 = range(0, 37)
        range1 = [math.radians(each) for each in range1]
        range2 = [math.radians(each) for each in range2]

        if angle in range1 or angle in range2:
            return True
        return False

    def shoot_fire(self, camera):
        """
        Spew awesome fireballs in the direction of the mouse.
        This function utilises the game's camera, which is passed
          to it, to compute the position of the cursor relative to
          the player.
        """

        cursor_pos = pygame.mouse.get_pos()
        tempMouseRect = pygame.Rect(cursor_pos, (0, 0))
        tempMouseRect = camera.use_cam_rect(tempMouseRect)

        relPos = tempMouseRect.topleft

        self.intMousePos = relPos
        ang = self.get_shoot_angle(relPos)
        #ang = math.radians(170 - math.degrees(ang))
        ang = math.radians(( (math.degrees(ang)+ 180 )))
        #ang = int(ang)

        if self.canShoot and self.ammo: #and self.is_good_angle(ang):
            self.canShoot = False
            self.ammo -= 1
            self.timer_fire = time.time()

            # decide starting position of fireball

            xPos = self.rect.centerx

            fire = powersC.Fireball((xPos, self.rect.centery), ang, self.direction)
            self.powerGroup.add(fire)

    def jump(self):
        if not self.fall:
            self.y_vel = -self.jump_power
            self.fall = True

        if self.water_contact:
            self.y_vel = -self.jump_power/2
    
    def check_falling(self, obstacles):
        """ if the player is not in contact with an obstacle, fall """
        self.rect.move_ip((0, 1))
        if not pygame.sprite.spritecollideany(self, obstacles):
            if not self.climb:
	            self.fall = True

        self.rect.move_ip((0, -1))

    def get_position(self, obstacles):
        if not self.fall:
            self.check_falling(obstacles)
        else:
            self.fall = self.check_collisions((0, self.y_vel), 1, obstacles)
        
        if self.x_vel:
            self.check_collisions((self.x_vel, 0), 0, obstacles)

    # CAUTION:
    def check_collisions(self, offset, index, obstacles):
        """ checks if a collision would occur after moving offset pixels"""
        unaltered = True
        self.rect.move_ip(offset)
        while  pygame.sprite.spritecollideany(self, obstacles):

            # First of all, check if it is a motile transparent block.
            # if so, do nothin
            col_spr = pygame.sprite.spritecollideany(self, obstacles)
            if hasattr(col_spr, "inertia"):
                if col_spr.inertia:
                    break

            if self.climb:
	            self.climb_mobility = False
            else:
                self.climb_mobility = True

            self.rect[index] += (1 if offset[index] < 0 else -1)
            unaltered = False
            #print("DEBUG: PLAYERCOL, {}".format(index))

            # stop walking animation
            if index == 0:
                self.walk = False


        return unaltered
    
    def check_action_contact(self, actionObjGroup):
        """checks if self is in contact with an actionObj like a switch, button,
           lever, vechicle, or any such thing"""

        self.action_contact = False # Reset the value to prevent mishaps
        obj = pygame.sprite.spritecollideany(self, actionObjGroup)
        
        if obj:
            self.action_obj = obj
            if obj.type == "SWITCH":
                self.action_contact = True
            else:
                self.action_contact = False

    def calc_vertical(self, delX, angle):
        hypot = delX / math.cos(angle)
        delY = hypot * math.sin(angle)
        return delY

    def handle_slopes(self, slopeG):
        """
        (Hopefully) handles slope collisions.
        slopeG = slope sprites Group
        NOTE: slopeG must contain homogeneous slopes
        """



        colSprite = pygame.sprite.spritecollideany(self, slopeG)
        if colSprite: #and self.rect.y < colSprite.rect.y:
            self.fall = False

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
            y_move_len = self.calc_vertical(x_move_len, angle_rad)

            # just for debugging
            self.d1 = x_move_len
            self.d2 = y_move_len

            # Now, it is needed to move the player down till
            # he reaches the 'essence' of the slope. This is because I
            # am too lazy to implement pixel-perfect collision.
            # Since this is to be done only once, a variable will be used
            # to keep track of whether this has beend donef for one slope or not

            # tolerance for height changing
            tol = False
            if abs(colSprite.rect.topleft[1] - self.rect.bottomleft[1]) <=  10:
                tol = True
            #print "ABS ", abs(colSprite.rect.topleft[1] - self.rect.bottomleft[1])

            if not self.prev_slope and tol:
                self.prev_slope = True

                x_off_mov = colSprite.rect.topleft[0]  -  self.rect.bottomleft[0]
                y_off_mov = self.calc_vertical(x_off_mov, angle_rad)

                # handling for rightwards velocity
                if self.direction == RIGHT:
                    y_off_mov = -y_off_mov


                self.rect.move_ip((0, y_off_mov))

            # check collision with any slope

            #self.rect.move_ip((x_move_len, y_move_len))
            # it seems that the above code is redundant; will check
            self.rect.move_ip((-self.x_vel, 0)) # undo the shifting
            self.rect.move_ip((x_move_len, y_move_len))

        else:
            self.prev_slope = False

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

		# handle climbind
		if self.climb:
			self.walk = False
			self.idle = False
			self.image = (self.leftIdleImg if self.direction == LEFT else \
							self.rightIdleImg)

    def check_water(self, extraG):
        
        waterG = [each for each in extraG if each.type == "WATER"]
        waterG = pygame.sprite.Group(waterG)

        self.water_contact = pygame.sprite.spritecollideany(self, waterG)
        

    # chief method
    def update(self, keys, camera, mainS, obstacles, actionG, slopeG, extraG):

        # current time
        # for toggling the self.canShift
        samaya = time.time()
        self.OUTLIST[1] = samaya

        self.check_keys(keys)
        self.handle_slopes(slopeG)
        self.get_position(obstacles)
        self.check_action_contact(actionG)
        self.check_water(extraG)
        self.manage_states()

        #self.x += self.x_vel
        #self.rect.x += self.x_vel

        if self.fall:
            self.y_vel += GRAVITY
        else:
            self.y_vel = 0

        # MARKED
        if self.water_contact:
            UP_FORCE = self.y_vel * 0.12  +  BUOYANCY
            self.y_vel -= UP_FORCE
            
        self.x += self.x_vel
        #self.rect.y += self.y_vel
        #self.y += self.y_vel

        self.powerGroup.update(obstacles)
        for each in self.powerGroup:
            if each.used:
                self.powerGroup.remove(each)

            mainS.blit(each.image, camera.use_cam(each))

        # manage internal timers
        self.timer_allstop = time.time()
        if (self.timer_allstop - self.timer_fire) >= FIRE_TIME_LIMIT:
            self.canShoot = True

        return self.OUTLIST

    def draw(self, surface):
        surface.blit(self.image, self.rect)
