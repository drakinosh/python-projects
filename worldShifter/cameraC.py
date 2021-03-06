#!/usr/bin/env python

#Camera module that provides scrolling

class Camera:

    def __init__(self, screenW, screenH, levelW, levelH, player_coords):
        self.disp_val = 0
        self.mid_height = screenH/2
        self.mid_width  = screenW/2
        self.total_h = levelH
        self.total_w = levelW

        self.hor_pos = player_coords[0]
        self.init_x = player_coords[0]
        self.hor_offset = 0
        self.total_disp = 0
        self.max_disp = self.total_w - screenW

        self.focus_width = 0

    def use_cam(self, sprite):
        sprite.rect.move_ip((self.hor_offset, 0))


    def update(self, player_vel):
        self.hor_pos += player_vel
        self.total_disp = self.hor_pos - self.init_x
        # if the mid width has been exceeded,
        # make everything move opposite to the player
        # so that an illusion of 'scrolling' is created

        # calculate the focus width and decide to scroll


        self.focus_width  = self.mid_width

        if (self.hor_pos > self.focus_width and player_vel > 0) \
            or (self.hor_pos < self.focus_width and player_vel < 0):
            self.hor_offset = -player_vel
        else:
            self.hor_offset = 0
