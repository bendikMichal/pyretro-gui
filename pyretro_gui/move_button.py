
import pygame
import sys

from .app_core import app_state
from .constants import Colors
if sys.platform != "win32":
    from .retro_screen import x_can_minimize

from .retro_text import font
from .retro_button import RetroButton

pygame.font.init()

class MoveButton(RetroButton):
    APPICON_SIZE = 24

    def __init__ (self, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], border_color: tuple = Colors.TEXT, shadow_color: tuple = Colors.SHADOW, onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0], z_index: int = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.colors = colors
        self.border_color = border_color
        self.shadow_color = shadow_color
        self.z_index = z_index
        
        self.onclick = onclick
        self.onpressed = onpressed
        self.anchors = anchors
        
        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed

        self.origin_press = (0, 0)
    
    def get_rect (self, win_size):
        return super().get_rect(win_size)

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        self.w = win_size[0] - (self.APPICON_SIZE + (self.ICON_SIZE + self.PAD) * (4 - app_state.get_hidden_count())) + 18
        self.rect.w = self.w

        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos) or self.pressed
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0] and not app_state.resizing
        app_state.moving = self.pressed and self.onpressed

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
        pygame.draw.rect(win, self.shadow_color, (r.x, r.y + r.h - 4, r.w, 4))
        pygame.draw.rect(win, self.border_color, r, 1)
        pygame.draw.line(win, self.border_color, (r.x, r.y + r.h), (r.x + r.w - 1, r.y + r.h), 1)

        text_surf = font.render(pygame.display.get_caption()[0], False, self.border_color)
        win.blit(text_surf, [r.x + 4, r.y + 3])

