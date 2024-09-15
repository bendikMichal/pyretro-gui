
import pygame

from retro_button import RetroButton

class RetroIcon(RetroButton):

    def __init__(self, x: int, y: int, w: int = 24, h: int = 32, color: tuple = ..., border_color: tuple = ..., icon: pygame.Surface | None = None, anchors: list[int] = [0, 0], z_index: int = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.anchors = anchors
        self.z_index = z_index

        self.color = color
        self.border_color = border_color

        self.icon = icon

        self._disabled = False

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        pass

    def render(self, win, win_size):
        r = self.get_rect(win_size)
        r.w += 1
        r.h += 1

        pygame.draw.rect(win, self.color, r)
        pygame.draw.rect(win, self.border_color, r, 1)
        pygame.draw.line(win, self.border_color, (r.x, r.y + r.h), (r.x + r.w - 1, r.y + r.h), 1)

        if self.icon: win.blit(self.icon, [r.x, r.y])
