#!/usr/bin/env python

import pygame
import const as c
import cus_game
from levelEditor import editor

FPS = 60
STARTBUT_NAME = 'startbut'
EDITBUT_NAME = 'editbut'

class Button(pygame.sprite.Sprite):
    
    def __init__(self, name, pos, image):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.pos = pos
        self.name = name
        self.rect = self.image.get_rect(topleft=pos)

    def lies_in(self, pos):
        "Checks if a coordinate pos lies within self's rectangle"

        if self.rect.collidepoint(pos):
            return True
        return False

    def update(self, mainS):
        mainS.blit(self.image, self.rect)


class Control(object):
    
    def __init__(self):
        
        self.screen = pygame.display.set_mode((c.SCREEN_W, c.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.buttonG = pygame.sprite.Group()
        self.do_loop = True
        self.add_items()
        pygame.mouse.set_visible(True)

    def add_items(self):
        start_but = Button(STARTBUT_NAME, (c.HALF_W-100, c.HALF_H-100), 
          c.STARTBUT_PATH)
        edit_but = Button(EDITBUT_NAME,  (c.HALF_W-100, c.HALF_H), 
          c.EDITBUT_PATH)
        self.buttonG.add(start_but)
        self.buttonG.add(edit_but)

    def loop(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.do_loop = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                but_list = [but for but in self.buttonG if but.lies_in(pos)]
                for but in but_list:
                    if but.name == STARTBUT_NAME:
                        cus_game.main()
                    elif but.name == EDITBUT_NAME:
                        editor.main()

        self.screen.fill(c.BLUE)
        self.buttonG.update(self.screen)
        self.clock.tick(FPS)
        pygame.display.flip()

    def main(self):
        
        pygame.init()
        while self.do_loop:
            self.loop()

        pygame.quit()

def main():
    cont = Control()
    cont.main()


if __name__ == '__main__':
    main()
    print("GAME MENU.PY MAIN CONTROL CHECK")
