#!/usr/bin/env python

import pygame
from const import *
from spriteHandler import SpriteSheet
import time

class BaseEnemy(pygame.sprite.Sprite):

    def __init__(self, pos, direc, vel, yvel, gravBool):
        """
        Initialiser for BaseEnemy class.
        
        pos         -> Cartesian coordinates
        direc       -> LEFT or RIGHT
        vel         -> horizontal velocity
        yvel        -> max vertical velocity
        gravBool    -> True if enemy experiences gravity
        """

        pygame.sprite.Sprite.__init__(self)

        self.x = pos[0]
        self.y = pos[1]

        self.direction = direc
        self.speed = vel
        self.y_speed = yvel
        self.gravBool = gravBool
        self.x_vel = (self.speed if self.direction == RIGHT else -self.speed)
        self.y_vel = 0

        self.rect = None # must assign this
        self.image = None# ditto

        self.alive = True # is alive
        self.haveDied = False   # just died
        self.fall = False # not falling
        self.anim = False # toggle animation


    def check_height(self, sprite):
        "Checks if a sprite is about the same depth down from the origin"
        
        
        #myVal = self.rect.topleft[1] + self.rect.height
        #oVal  = sprite.rect.topleft[1] + sprite.rect.height

        myVal = self.rect.midleft[1]
        oVal = sprite.rect.midleft[1]

        # Theory:
        # The difference in y-coords between the midpoints should not 
        # be greater than half the height of the larger rect.

        if self.rect.height < sprite.rect.height:
            biggerRect = sprite.rect
        else:
            biggerRect = self.rect

        benchHeight = biggerRect.height / 2.0 

        # Note: It is crucial to remember that, in game programming,
        # the Y-axis is positive downwards.

        if abs(myVal - oVal) < benchHeight:
            return True
        return False

    def ground_handler(self, obstacles):

        
        for hurdle in obstacles:
            if self.check_height(hurdle):
                if self.x_vel > 0 and self.rect.right == hurdle.rect.left:
                    self.x_vel = -self.x_vel
                    if self.gravBool:
                        self.fall = True
                        print("YEACH")

                elif self.x_vel < 0 and self.rect.left == hurdle.rect.right:
                    self.x_vel = -self.x_vel
                    if self.gravBool:
                        self.fall = True
                        print("YEACH")

    def check_collision(self, sprite):
        "checks if sprite's rect intersects self's rect"
        return self.rect.colliderect(sprite.rect)

    def check_falling(self, obstacles):
        
        # For non-falling enemies, self.fall defaults to False

        if self.gravBool == False:
            self.fall = False
            return

        if pygame.sprite.spritecollideany(self, obstacles):
            
            self.fall = False
            return

        self.rect.move_ip((0, 1))

        if not pygame.sprite.spritecollideany(self, obstacles):
            self.fall = True
        else:
            self.fall = False

        self.rect.move_ip((0, -1))
        

     

    def move(self):
        if not self.fall:
            self.rect.move_ip((self.x_vel, 0))


class SimpleEnemy(BaseEnemy):
    """
    A class of enemies whose movements are restricted to 
      left-and-right motion and which have only two images
      for each direction.
    """

    def __init__(self, pos, direc, speed, enemType, 
                 leftImg1Path, leftImg2Path, gravBool):

        BaseEnemy.__init__(self, pos, direc, speed, 0, gravBool)

        self.enemType = enemType
        self.gravBool = gravBool
        # load all necessary images
        self.leftWalk1 = pygame.image.load(leftImg1Path).convert()
        self.rightWalk1 = pygame.transform.flip(self.leftWalk1, True, False).convert()
        self.leftWalk2 = pygame.image.load(leftImg2Path).convert()
        self.rightWalk2 = pygame.transform.flip(self.leftWalk2, True, False).convert()

        self.leftImgList = [self.leftWalk1, self.leftWalk2]
        self.rightImgList = [self.rightWalk1, self.rightWalk2]

        for image in self.leftImgList + self.rightImgList:
            image.set_colorkey(BLACK)

        self.image = (self.rightWalk1 if self.direction == RIGHT \
                      else self.leftWalk1)
        self.rect = self.image.get_rect(topleft=pos)
        self.x += self.rect.x
        self.y += self.rect.y

        # create animation indices
        self.aniPos = 0
        self.aniSpeed = 1
        self.aniFact = 8

    def animate(self, imageList, aniPos, aniSpeed, aniFact):
        if aniPos % aniFact == 0:
            try:
                self.image = imageList[aniPos / aniFact]
            except IndexError:
                aniPos = -aniSpeed
        aniPos += aniSpeed
        return aniPos

    
    def die(self):
        
        if not self.haveDied:
            
            if self.gravBool:
                self.alive = False
            else:
                self.gravBool = True

            self.haveDied = True    # never enter this branch again
    
    def check_player(self, player):


        if self.check_height(player) and self.check_collision(player):
            player.health -= 0.5
        
        # If the player falls on you, die
        if player.y_vel > 0 and self.check_collision(player):
            
            self.die()

    def handle_all(self):
        if self.x_vel > 0:
            self.direction = RIGHT
        else:
            self.direction = LEFT

        imageList = (self.leftImgList if self.direction == LEFT \
                       else self.rightImgList)
        if not self.fall:
            self.aniPos = self.animate(imageList, self.aniPos, self.aniSpeed,\
                                       self.aniFact)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, obstacles, hazards, player):
        if self.fall:
            self.y_vel += GRAVITY
            self.rect.move_ip((0, self.y_vel))
        self.check_player(player)
        self.ground_handler(obstacles)
        self.check_falling(obstacles)
        if pygame.sprite.spritecollideany(self, hazards): 
            self.die()


        # flies and the like should die only after hitting the 
        # ground with a thump

        if self.haveDied and not self.fall:
            self.alive = False

        self.move()
        self.handle_all()


class Slime(SimpleEnemy):
    
    def __init__(self, pos, direc):
        
        SimpleEnemy.__init__(self, pos, direc, 2, SQUISHY,
                             slime1Path, slime2Path, True)


class Fly(SimpleEnemy):
    
    def __init__(self, pos, direc):
        
        SimpleEnemy.__init__(self, pos, direc, 4, SQUISHY,
                             fly1Path, fly2Path, False)



class Frog(BaseEnemy):
    
    def __init__(self, pos, direc):
        
        BaseEnemy.__init__(self, pos, direc, 3, 5, True)
        
        self.leaping = False
        self.leap_start = False     # has started to leap
        self.can_leap = True

        self.leapLeftImg = pygame.image.load(frogLeapLeftPath).convert() 
        self.leapRightImg = pygame.transform.flip(self.leapLeftImg, True, False)
        self.squatLeftImg = pygame.image.load(frogSquatLeftPath).convert()
        self.squatRightImg = pygame.transform.flip(self.squatLeftImg, True, False)

        self.all_images = [self.squatLeftImg, self.squatRightImg,
                           self.leapLeftImg, self.leapRightImg]

        for image in self.all_images:
            image.set_colorkey(BLACK)

        if self.direction == LEFT:
            self.image = self.squatLeftImg
        else:
            self.image = self.squatRightImg

        self.rect = self.image.get_rect(topleft=pos)
        self.time_limit = 1.5
        self.t1 = None
        self.t2 = None
        self.mutex = False  # to lock times

    def move(self):
        
        if self.leaping:
            self.rect.move_ip((self.x_vel , 0))

        self.rect.move_ip((0, self.y_vel))

     
    def handle_all(self):
        
        if self.x_vel > 0:
            self.direction = RIGHT
            self.image = self.squatRightImg

            if self.leaping:
                self.image = self.leapRightImg

        elif self.x_vel < 0:
            
            self.direction = LEFT
            self.image = self.squatLeftImg

            if self.leaping:
                self.image = self.leapLeftImg

        # Limit the jumping of the frog
        if self.t1:
            self.t2 = time.time()
            if (self.t2 - self.t1) >= self.time_limit:
                self.can_leap = True
                self.t1 = None
                self.mutex = True
        
        else:
            self.mutex = False

    def update(self, obstacles, hazard, player):  


        if self.fall:
            self.y_vel += GRAVITY
            self.can_leap = False

        else:     # fell to the ground
            self.leaping = False
            self.y_vel = 0

            if not self.t1 and not self.mutex:
                self.t1 = time.time()
                self.can_leap = False
                self.mutex = False
        '''
        if self.leap_start:    
            self.y_vel = -self.y_speed
            self.leap_start = False
            self.leaping = True
        '''

        # Make the frog leap everytime it can
        if not self.leaping and self.can_leap:
            self.leap_start = True
            print("TOBIRU!")
        
        if self.leap_start:    
            self.y_vel = -self.y_speed
            self.leap_start = False
            self.leaping = True

        self.move()

        self.ground_handler(obstacles)
        self.check_falling(obstacles)
        self.handle_all()


#-- Advanced enemies ---

class AdvancedEnemy(pygame.sprite.Sprite):
    
    def __init__(self, pos, spriteSheetPath, imgCoordList):
        """
        Initialise an instance of AdvancedEnemy

        pos             -> initial position of enemy
        spriteSheetPath -> path to sprite sheet
        imgCoordList    -> list containing coords of images in spritesheet
            It shoud be of the form:
                (x, y, width, height)
        """


        self.pos = pos

        self.sheet = SpriteSheet(spriteSheetPath)

        self.walk_r_list = list()
        self.walk_l_list = list()





