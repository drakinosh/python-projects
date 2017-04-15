import pygame as pg
import const as c
import playerHandler as ph

class Player(pg.sprite.Sprite):
    
    def __init__(self, pid, pos, direc):
        """
        pos -> position
        pid -> player's id -- identifies character
        """

        pg.sprite.Sprite.__init__(self)

        self.x, self.y = pos
        self.health = c.MAX_HEALTH
        self.chakra = c.MAX_CHAKRA
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

        self.image = self.idler_sprites[0]
        self.rect = self.image.get_rect(topleft=pos)

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

        # other attribs
        self.cooldown = ph.getCoolDown(self.pid)
        self.canThrow = True # Kunai
        self.canJustu = True # I hereby declare that justu is a ver

        self.walkPos = c.WALK_POS
        self.walkFact = c.WALK_FACT
        self.animSpeed = c.ANIM_SPEED

        self.idlePos = c.IDLE_POS
        self.idleFact = c.IDLE_FACT

        # other poses
        self.jumpPos = 0
        self.fallPos = 0
        self.airFact = 16


    def animate(self, imageList, animPos, animFact):
        
        if animPos % animFact == 0:
            try:
                self.image = imageList[animPos/animFact]
            except IndexError:
                animPos = -self.animSpeed
        animPos += self.animSpeed
        return animPos

    def jump(self):
        
        if not self.fall:
            self.y_vel = -self.jump_power
            self.fall = True

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
        

        if not self.walk and not self.attack and not self.fall:
            self.idle = True
        else:
            self.idle = False

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

        elif self.idle:
            if self.direc == c.RIGHT:
                self.idlePos = self.animate(self.idler_sprites, self.idlePos,
                                    self.idleFact)
            else:
                self.idlePos = self.animate(self.idlel_sprites, self.idlePos,
                                    self.idleFact)



    def update(self, obstacles, keys):
        
        self.get_position(obstacles)
        self.manage_states()
        self.check_keys(keys)

        if self.fall:
            self.y_vel += c.GRAVITY
        else:
            self.y_vel = 0

        self.x += self.x_vel


    def draw(self, surface):
        surface.blit(self.image, self.rect)


