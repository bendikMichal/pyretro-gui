
import os
import pygame

from app_core import app_state
from constants import Colors

class RetroButton:
    ICON_SIZE = 24
    PAD = 6
    ICON_PATH = os.path.abspath(".") + "/ui_icons"

    def __init__ (self, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], onclick = None, onpressed = None, anchors: list[int] = [0, 0], z_index: int = 0, name: str | None = None, image_path: str | None = None):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.colors = colors
        
        self.z_index = z_index
        self.onclick = onclick
        self.onpressed = onpressed
        self.anchors = anchors

        self.image_path = image_path
        self.img = None
        self.load_img()
        
        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed
        self._disabled = False

        self.origin_press = (0, 0)

    def load_img (self):
        self.path = None
        if self.name is not None:
            self.path = self.ICON_PATH + "/" + self.name + ".png"

        if self.image_path is not None:
            self.path = self.image_path
        
        if self.path is None: return

        self.img = pygame.image.load(self.path).convert_alpha()
    
    def get_rect (self, win_size):
        r = [self.x, self.y, self.w, self.h]
        if self.anchors[0]: r[0] = win_size[0] - r[0] - r[2]
        if self.anchors[1]: r[1] = win_size[1] - r[1] - r[3]

        return pygame.Rect(r)

    def disabled(self):
        self._disabled = True

    def enabled(self):
        self._disabled = False

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos) and not self._disabled
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0] and not app_state.resizing

        # pressed
        if self.pressed and self.onpressed:
            if not self.__prev_pressed:
                self.origin_press = mouse_pos

            self.onpressed(self)

        # clicked
        if not self.pressed and self.__prev_pressed and self.focused:
            if self.onclick:
                self.onclick(self)


    def render (self, win, win_size):
        r = self.get_rect(win_size)

        if self.pressed: r.y -= 1

        pygame.draw.rect(win, self.colors[int(self.focused)], r)
        if self.img:
            win.blit(self.img, [r.x, r.y])



