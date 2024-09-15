
import pygame

from constants import Colors
from retro_button import RetroButton


class ScrollBar:
    SCRLBAR_WIDTH = 16
    ICON_PATH = RetroButton.ICON_PATH

    def __init__ (self, x: int, y: int, size: int, content_size: int, horizontal: bool = False, row_size: int = 16, z_index: int = 0):
        self.z_index = z_index
        self.x = x
        self.y = y

        self.size = size
        self.content_size = content_size
        self.horizontal = horizontal
        self.row_size = row_size

        self.progress = 0

        # btn - the scrolling one
        self.scrl_size = self.size - self.SCRLBAR_WIDTH * 2
        self.btn_size = self.scrl_size * (self.scrl_size / content_size)
        if self.btn_size < 8: self.btn_size = 8

        self.btn_pos = (self.scrl_size - self.btn_size) * self.progress
        self.btn_rect = None

        self.btn_focused = False
        self.btn_pressed = False
        self.__prev_btn_pressed = False

        self.mouse_diff = 0

        self.load_img()

    def load_img (self):
        self.name_a = "arrow_" + ("up" if not self.horizontal else "left")
        self.name_b = "arrow_" + ("down" if not self.horizontal else "right")
        c = [Colors.BG, Colors.LIGHT_BG]

        self.button_a = RetroButton(self.name_a, self.x, self.y, self.SCRLBAR_WIDTH, self.SCRLBAR_WIDTH, colors = c, onpressed = self.up)
        s = self.scrl_size + self.SCRLBAR_WIDTH
        self.button_b = RetroButton(self.name_b, self.x + (0 if not self.horizontal else s), self.y + (0 if self.horizontal else s), self.SCRLBAR_WIDTH, self.SCRLBAR_WIDTH, colors = c, onpressed = self.down)


    def up (self, _):
        self.btn_pos -= self.row_size * (self.scrl_size / self.content_size)

    def down (self, _):
        self.btn_pos += self.row_size * (self.scrl_size / self.content_size)

    def get_progress (self):
        return self.btn_pos / (self.scrl_size - self.btn_size)


    def update (self, mouse_pos, mouse_btns, _):
        self.__prev_btn_pressed = self.btn_pressed

        # scrollbar button handling
        if not self.horizontal:
            self.btn_rect = pygame.Rect(self.x, self.btn_pos, self.SCRLBAR_WIDTH, self.btn_size)
            mp = mouse_pos[1]
            start = self.y
        else:
            self.btn_rect = pygame.Rect(self.btn_pos, self.y, self.btn_size, self.SCRLBAR_WIDTH)
            mp = mouse_pos[0]
            start = self.x

        # moving cuz of btns
        start += self.SCRLBAR_WIDTH

        self.btn_focused = self.btn_rect.collidepoint(mouse_pos) or self.btn_pressed
        self.btn_pressed = self.btn_focused and mouse_btns[0]

        if not self.__prev_btn_pressed and self.btn_pressed: self.mouse_diff = mp - self.btn_pos
        if self.btn_focused and self.btn_pressed: self.btn_pos = mp - self.mouse_diff

        self.button_a.update(mouse_pos, mouse_btns, None)
        self.button_b.update(mouse_pos, mouse_btns, None)

        # keeping in bounds
        if self.btn_pos < start: self.btn_pos = start
        if self.btn_pos > start + self.scrl_size - self.btn_size: self.btn_pos = start + self.scrl_size - self.btn_size

        self.progress = self.get_progress()

    def render (self, win, _):

        # bar
        w = self.scrl_size if self.horizontal else self.SCRLBAR_WIDTH
        h = self.scrl_size if not self.horizontal else self.SCRLBAR_WIDTH
        x = self.x + (0 if not self.horizontal else self.SCRLBAR_WIDTH)
        y = self.y + (0 if self.horizontal else self.SCRLBAR_WIDTH)
        r = (x, y, w, h)
        pygame.draw.rect(win, Colors.DARK_SHADOW, r)
        pygame.draw.rect(win, Colors.TEXT, r, 1)

        # scrollbar button
        if self.btn_rect:
            pygame.draw.rect(win, Colors.BG if not self.btn_focused else Colors.LIGHT_BG, self.btn_rect)
            r = (self.btn_rect.x + 1, self.btn_rect.y + 1, self.btn_rect.w - 2, self.btn_rect.h - 2)
            pygame.draw.rect(win, Colors.LIGHT_BG, r, 1)
            pygame.draw.rect(win, Colors.TEXT, self.btn_rect, 1)

        # buttons
        self.button_a.render(win, win.get_size())
        self.button_b.render(win, win.get_size())


