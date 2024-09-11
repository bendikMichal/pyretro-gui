
import os
import pygame

class RetroButton:
    ICON_PATH = os.path.abspath(".") + "/ui_icons"
    def __init__ (self, name: str, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [(0, 0, 0)] * 2, onclick = None, anchors: list[int] = [0, 0, 0, 0]):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.colors = colors
        
        self.onclick = onclick
        self.anchors = anchors

        self.path = self.ICON_PATH + "/" + name + ".png"
        self.img = pygame.image.load(self.path).convert_alpha()
        
        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed
    
    def get_rect (self, win_size):
        r = [self.x, self.y, self.w, self.h]
        if self.anchors[0]: r[0] = win_size[0] - r[0]
        if self.anchors[1]: r[1] = win_size[1] - r[1]

        return pygame.Rect(r)

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0]

        # clicked
        if not self.pressed and self.__prev_pressed and self.focused:
            if self.onclick:
                self.onclick(self)


    def render (self, win, win_size):
        r = self.get_rect(win_size)

        if self.pressed: r.y -= 1

        pygame.draw.rect(win, self.colors[int(self.focused)], r)
        win.blit(self.img, [r.x, r.y])


