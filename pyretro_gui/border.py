
import pygame

from .app_core import app_state
from .retro_screen import get_mouse_pos

class Border:
    def __init__ (self, border_width = 2, onpressed = lambda _: None, z_index = -99):
        # width as in border width
        self.border_width = border_width
        self.onpressed = onpressed
        self.z_index = z_index

        self.w, self.h = 0, 0

        self.resize_vector = [0, 0]
        self.origin_press = [0, 0]

        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed

    def resize (self, size):
        self.w = size[0]
        self.h = size[1]

    def set_cursor (self):
        if not self.focused: return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        rv = self.resize_vector
        if rv[0] != 0 and rv[1] != 0:
            if rv[0] == rv[1]: return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
            else: return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)

        if rv[0] != 0: return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
        if rv[1] != 0: return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)



    def update (self, mouse_pos, mouse_btns, window_size):
        self.resize(window_size)

        if not self.pressed: self.resize_vector = [0] * 2

        rect = pygame.Rect(0, 0, self.w, self.h)
        bw = self.border_width * 2
        inner_rect = pygame.Rect(self.border_width, self.border_width, self.w - bw, self.h - bw)

        # resize press must not come from inside app
        if app_state.origin_press is not None:
            origin_focus = rect.collidepoint(app_state.origin_press) and not inner_rect.collidepoint(app_state.origin_press)
        else:
            origin_focus = None

        if rect.collidepoint(mouse_pos) and not inner_rect.collidepoint(mouse_pos) or self.pressed:
            self.focused = True

            if not self.pressed:
                lr = pygame.Rect(0, self.border_width, self.border_width, self.h - bw) 
                rr = pygame.Rect(self.w - self.border_width, self.border_width, self.border_width, self.h - bw) 

                tr = pygame.Rect(self.border_width, 0, self.w - bw, self.border_width)
                br = pygame.Rect(self.border_width, self.h - self.border_width, self.w - bw, self.border_width)


                if lr.collidepoint(mouse_pos):
                    self.resize_vector[0] = -1

                elif rr.collidepoint(mouse_pos):
                    self.resize_vector[0] = 1

                elif tr.collidepoint(mouse_pos):
                    self.resize_vector[1] = -1

                elif br.collidepoint(mouse_pos):
                    self.resize_vector[1] = 1

                else:
                    if mouse_pos[0] < window_size[0] / 2: self.resize_vector[0] = -1
                    else: self.resize_vector[0] = 1

                    if mouse_pos[1] < window_size[1] / 2: self.resize_vector[1] = -1
                    else: self.resize_vector[1] = 1

        else:
            self.focused = False
            
        self.set_cursor()

        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0] and (origin_focus or self.pressed)
        app_state.resizing = self.pressed

        if self.pressed and self.onpressed:
            if not self.__prev_pressed:
                self.origin_press = mouse_pos

            self.onpressed(self)

    def render (self, window, _):
        pass
