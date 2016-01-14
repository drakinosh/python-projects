#!/usr/bin/env python

import pygame
from const import *

class BaseEnemy(pygame.sprite.Sprite):

    def __init__(self, pos, direc, vel, gravBool):
        """
        Initialiser for BaseEnemy class.
        
        pos         -> Cartesian coordinates
        direc       -> LEFT or RIGHT
        vel         -> horizontal velocity
        gravBool    -> True if enemy experiences gravity
        """

        pygame.sprite.Sprite.__init__(self)

        self.x = pos[0]
        self.y = pos[1]

        self.direction = direc
        self.speed = vel
        self.gravBool = gravBool
        self.x_vel = (self.speed if self.direction == RIGHT else -self.speed)
        self.y_vel = 0

        self.rect = None # must assign this
        self.image = None# ditto

        self.alive = True # is alive
        self.fall = False # not falling
        self.anim = False # toggle animation


    def check_height(self, sprite):
        "Checks if a sprite is about the same depth down from the origin"
        myVal = self.rect.topleft[1] + self.rect.height
        oVal  = sprite.rect.topleft[1] + sprite.rect.height

        if abs(myVal - oVal) < TOLERANCE:
            return True
        return False

    def ground_handler(self, obstacles):

        
        for hurdle in obstacles:
            if self.check_height(hurdle):
                if self.x_vel > 0 and self.rect.right == hurdle.rect.left:
                    self.x_vel = -self.x_vel
                elif self.x_vel < 0 and self.rect.left == hurdle.rect.right:
                    self.x_vel = -self.x_vel

    def check_collision(self, sprite):
        "checks if sprite's rect intersects self's rect"
        return self.rect.colliderect(sprite.rect)

    def check_falling(self, obstacles):
        
        # For non-falling enemies, self.fall defaults to False

        if self.gravBool == False:
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

        BaseEnemy.__init__(self, pos, direc, speed, gravBool)

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

    def check_player(self, player):


        if self.check_height(player) and self.check_collision(player):
            player.health -= 0.5
        # If the player falls on you, die
        if player.y_vel > 0 and self.check_collision(player):
            self.alive = False

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
