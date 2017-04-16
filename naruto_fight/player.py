import pygame as pg
import const as c
import playerHandler as ph
import weapons as w

class Player(pg.sprite.Sprite):
    
    def __init__(self, pid, pos, direc):
        """
        pos -> position
        pid -> player's id -- identifies character
        """

        pg.sprite.Sprite.__init__(self)
        
        self.pos = pos
        self.x, self.y = pos
        self.health = c.MAX_HEALTH
        self.chakra = c.MAX_CHAKRA
        self.kunai = c.MAX_KUNAICOUNT
        self.pid = pid
        self.direc = direc

        # get sprites list
        self.idlel_sprites = ph.getIdlelSprites(self.pid)
        self.idler_sprites = ph.getIdlerSprites(self.pid)
        self.walkl_sprites = ph.getRunlSprites(self.pid)
        self.walkr_sprites = ph.getRunrSprites(self.pid)
        self.jumpr_sprites = ph.getJumprSprites(self.pid)
        self.jumpl_sprites = ph.getJumplSprites(self.pid)
        self.fallr_sprites = ph.getFallrSprites(self.pid)
        self.falll_sprites = ph.getFalllSprites(self.pid)
        self.punchr_sprites = ph.getPunchrSprites(self.pid)
        self.punchl_sprites = ph.getPunchlSprites(self.pid)
        self.throwr_sprites = ph.getThrowrSprites(self.pid)
        self.throwl_sprites = ph.getThrowlSprites(self.pid)

        # doesn't matter
        #self.image = self.idler_sprites[0]
        self.image = self.punchl_sprites[1] # biggest iamge

        self.rect = self.image.get_rect(topleft=pos)

        # weapons thrown list
        # The player is responsible for updating(drawing)
        # the weapons he uses

        self.weapons_list = []

        # Movement
        self.speed = ph.getSpeed(self.pid)
        self.x_vel = 0
        self.y_vel = 0

        self.jump_power = ph.getJumpPower(self.pid)
        
        # state attribs
        self.idle = True
        self.attack = False
        self.walk = False
        self.fall = False
        self.throw = False

    
        # other attribs
        self.cooldown = ph.getCoolDown(self.pid)
        self.canThrow = True # Kunai
        self.canJustu = True # I hereby declare that justu is a ver
        self.canHit = True  # physical attacks like punches

        self.walkPos = c.WALK_POS
        self.walkFact = c.WALK_FACT
        self.animSpeed = c.ANIM_SPEED

        self.idlePos = c.IDLE_POS
        self.idleFact = c.IDLE_FACT

        self.punchPos = 0
        self.punchFact = 12 # slow

        # other poses
        self.jumpPos = 0
        self.fallPos = 0
        self.airFact = 16
        self.throwPos = 0
        self.throwFact = 12

        self.a_mutex = False # adjusting left punch
        self.t_mutex = False
        # remains true only white punching
        self.fin = False   # just finished punching
        self.t_fin = False

    def animate(self, imageList, animPos, animFact):
        
        if animPos % animFact == 0:
            try:
                self.image = imageList[animPos/animFact]
            except IndexError:
                animPos = -self.animSpeed
        animPos += self.animSpeed
        return animPos

    def throwAnimate(self, imageList, animPos, animFact):
        
        # First, adjust for the left direc
        if self.t_mutex:
            self.t_mutex = False # adjust only once
        if animPos % animFact == 0:
            try:
                self.image = imageList[animPos/animFact]
            except IndexError:
                animPos = -self.animSpeed
                self.throw = False

                if self.direc == c.LEFT:
                    self.t_fin = True

        animPos += self.animSpeed
        return animPos


    def hitAnimate(self, imageList, animPos, animFact):
        
        # if adjusting mutex is on, turn it off
        if self.a_mutex:
            self.a_mutex = not self.a_mutex

        if animPos % animFact == 0:
            try:
                self.image = imageList[animPos/animFact]
            except IndexError:
                animPos = -self.animSpeed
                self.attack = False     #stop after one loop

                if self.direc == c.LEFT:
                    self.fin = True

        animPos += self.animSpeed
        return animPos



    def jump(self):
        
        if not self.fall:
            self.y_vel = -self.jump_power
            self.fall = True

    def getThrowPos(self):
        """Position of placement of thrown weapons"""

        if self.direc == c.RIGHT:
            return self.rect.midright
        return self.rect.midleft


    def check_keys(self, keys):
        
        self.x_vel = 0

        #NOTABENE
        #move state management to manage_states

        if keys[pg.K_d]:
            
            if not self.fall:
                self.walk = True

            self.direc = c.RIGHT
            self.x_vel += self.speed
        
        elif keys[pg.K_a]:
            
            if not self.fall:
                self.walk = True
            self.direc = c.LEFT
            self.x_vel -= self.speed

        # jumping
        if keys[pg.K_w]:
            self.jump()

        # attack
        #WARNING
        #only hit if idle to avoid conflicts with throw
        # and vice-versa
        if keys[pg.K_z]:
            
            if not self.fall and self.canHit and self.idle:
                self.attack = True
                self.canHit = False

                if self.direc == c.LEFT:
                    self.a_mutex = True
        else:   
            # release if not in the middle of an attacl
            if not self.attack:
                self.canHit = True

        # can hit again only after releasing

        # kunai action
        if keys[pg.K_c]:
            if not self.fall and self.canThrow and self.idle:

                # Distract!
                self.throw = True
                self.canThrow = False
                kunai = w.Kunai(self.getThrowPos(),  self.direc)
                self.weapons_list.append(kunai)

                if self.direc == c.LEFT:
                    self.t_mutex = True


        else:
            if not self.throw:
                self.canThrow = True

        if not (keys[pg.K_d] or keys[pg.K_a]):
            self.walk = False

    def check_falling(self, obstacles):
        
        self.rect.move_ip((0, 1))

        obs_cond = pg.sprite.spritecollideany(self, obstacles)
        if not obs_cond:
            self.fall = True
        
        self.rect.move_ip((0, -1))

    def get_position(self, obstacles):
        
        if not self.fall:
            self.check_falling(obstacles)
        else:
            obs_col_cond = self.check_collisions((0, self.y_vel), 1 , obstacles)
            self.fall = obs_col_cond

        # check state
        if self.x_vel:
            self.check_collisions((self.x_vel, 0), 0, obstacles)

    
    def check_collisions(self, offset, index, obstacles):
        """checks if a collision would occur after moving offset pixels"""
        unaltered  = True
        self.rect.move_ip(offset)

        while pg.sprite.spritecollideany(self, obstacles):
            
            
            self.rect[index] += (1 if offset[index] < 0 else -1)
            unaltered = False

            # stop waling
            if index == 0:
                self.walk = False

        return unaltered

    def manage_states(self):
        
        # attacking takes precedence over walking
        if not self.walk and not self.fall and not self.attack and not self.throw:
            self.idle = True
        else:
            self.idle = False
        # ~A ^ ~B <=> ~(A V B)

        # if in the air and moving horizontally, disable running
        # animation
        if self.fall and self.x_vel != 0:
            self.walk = False

        # falling
        if self.fall and self.y_vel > 0 :
            if self.direc == c.RIGHT:
                self.fallPos = self.animate(self.fallr_sprites, self.fallPos,
                                    self.airFact)
            else:
                self.fallPos = self.animate(self.falll_sprites, self.fallPos,
                                    self.airFact)
        # jumping
        if self.jump and self.y_vel < 0:
            if self.direc == c.RIGHT:
                self.jumpPos = self.animate(self.jumpr_sprites, self.jumpPos,
                                    self.airFact)
            else:
                self.jumpPos = self.animate(self.jumpl_sprites, self.jumpPos,
                                    self.airFact)

        if self.walk:
            if self.direc == c.RIGHT:
                self.walkPos = self.animate(self.walkr_sprites, self.walkPos,
                                    self.walkFact)
            elif self.direc == c.LEFT:
                self.walkPos = self.animate(self.walkl_sprites, self.walkPos,
                                    self.walkFact)

        if self.idle:
            if self.direc == c.RIGHT:
                self.idlePos = self.animate(self.idler_sprites, self.idlePos,
                                    self.idleFact)
            else:
                self.idlePos = self.animate(self.idlel_sprites, self.idlePos,
                                    self.idleFact)

        # attack anim
        # while attacking, shift image so that the positions align
        # just once

        #WARNING
        if self.a_mutex: 
            self.rect.move_ip(-c.LEFT_ADJUST, 0)

        if self.t_mutex:
            self.rect.move_ip(-c.T_LEFT_ADJUST, 0)
        """ 
        if self.fin: # just finished punching
            self.rect.move_ip(c.LEFT_ADJUST, 0)
            self.fin = False
        """

        if self.attack:
            if self.direc == c.RIGHT:
                self.punchPos = self.hitAnimate(self.punchr_sprites, self.punchPos, 
                                    self.punchFact)
            else:
                self.punchPos = self.hitAnimate(self.punchl_sprites, self.punchPos,
                                    self.punchFact)

        if self.throw:
            if self.direc == c.RIGHT:
                self.throwPos = self.throwAnimate(self.throwr_sprites, self.throwPos,
                                    self.throwFact)
            else:
                self.throwPos = self.throwAnimate(self.throwl_sprites, self.throwPos,
                                    self.throwFact)


    def update(self, obstacles, keys, screen):
        

        # idea 
        # change rect to suit image

    
        self.get_position(obstacles)
        self.manage_states()
        self.check_keys(keys)

        if self.fall:
            self.y_vel += c.GRAVITY
        else:
            self.y_vel = 0

        self.x += self.x_vel

        for each in self.weapons_list:
            each.update(screen)

        self.draw(screen)

        # move after drawing last punching image
        if self.fin:
            self.rect.move_ip((c.LEFT_ADJUST, 0))
            self.fin = False
            #WARNING
            self.image = self.idlel_sprites[0]

        if self.t_fin:
            self.rect.move_ip((c.T_LEFT_ADJUST, 0))
            self.t_fin = False
            self.image = self.idlel_sprites[0]
        

        if c.DEBUG_MODE:
            # draw rect
            pg.draw.rect(screen, c.GREEN, self.rect, 2)

        

    def draw(self, surface):
        surface.blit(self.image, self.rect)


