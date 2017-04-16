import pygame as pg

import os
import const as c


class Kunai(pg.sprite.Sprite):
    
    def __init__(self, pos, direc):
        
        pg.sprite.Sprite.__init__(self)

        self.pos = pos
        self.direc = direc

        kunair_image = pg.image.load(os.path.join(c.WEAPONS_FOLDER, "kunai_r.png"))
        kunail_image = pg.transform.flip(kunair_image, True, False)

        if self.direc == c.RIGHT:
            self.image = kunair_image
        else:
            self.image = kunail_image

        self.rect = self.image.get_rect(topleft=pos)

        self.speed = c.KUNAI_SPEED
        self.x_vel = self.speed if self.direc == c.RIGHT else -self.speed

    def update(self, screen):

        self.rect.move_ip((self.x_vel, 0))
        
        screen.blit(self.image, self.rect)


