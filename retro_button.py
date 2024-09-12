
import os
import pygame

pygame.font.init()

class RetroButton:
    ICON_SIZE = 24
    PAD = 6
    ICON_PATH = os.path.abspath(".") + "/ui_icons"

    def __init__ (self, name: str, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [(0, 0, 0)] * 2, onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0]):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.colors = colors
        
        self.onclick = onclick
        self.onpressed = onpressed
        self.anchors = anchors

        self.load_img()
        
        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed

        self.origin_press = (0, 0)

    def load_img (self):
        self.path = self.ICON_PATH + "/" + self.name + ".png"
        self.img = pygame.image.load(self.path).convert_alpha()
    
    def get_rect (self, win_size):
        r = [self.x, self.y, self.w, self.h]
        if self.anchors[0]: r[0] = win_size[0] - r[0] - r[2]
        if self.anchors[1]: r[1] = win_size[1] - r[1] - r[3]

        return pygame.Rect(r)

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0]

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
        win.blit(self.img, [r.x, r.y])


class MoveButton(RetroButton):
    APPICON_SIZE = 24
    # font = pygame.font.SysFont("Courier New", 14)
    # font = pygame.font.SysFont("microsoftsansserif", 14)
    font = pygame.font.Font(os.path.abspath(".") + "/fonts/retrofont.ttf", 16)
    # font.set_bold(True)

    def __init__ (self, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [(0, 0, 0)] * 2, border_color: tuple = (0, 0, 0), shadow_color: tuple = (0, 0, 0), onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0]):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.colors = colors
        self.border_color = border_color
        self.shadow_color = shadow_color
        
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
        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos) or self.pressed
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0]

        # pressed
        if self.pressed and self.onpressed:
            if not self.__prev_pressed:
                self.origin_press = mouse_pos

            self.onpressed(self)

        # clicked
        if not self.pressed and self.__prev_pressed and self.focused:
            if self.onclick:
                self.onclick(self)

        self.w = win_size[0] - (self.APPICON_SIZE + (self.ICON_SIZE + self.PAD) * 4)
        self.rect.w = self.w

    def render (self, win, win_size):
        r = self.get_rect(win_size)

        if self.pressed: r.y -= 1

        pygame.draw.rect(win, self.colors[int(self.focused)], r)
        pygame.draw.rect(win, self.shadow_color, (r.x, r.y + r.h - 4, r.w, 4))
        pygame.draw.rect(win, self.border_color, r, 1)
        pygame.draw.line(win, self.border_color, (r.x, r.y + r.h), (r.x + r.w - 1, r.y + r.h), 1)

        text_surf = self.font.render(pygame.display.get_caption()[0], False, self.border_color)
        win.blit(text_surf, [r.x + 4, r.y + 3])


