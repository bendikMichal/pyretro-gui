
import pygame
from app_core import app_state

from constants import Colors
from retro_button import RetroButton


class ScrollBar:
    SCRLBAR_WIDTH = 16
    ICON_PATH = RetroButton.ICON_PATH

    def __init__ (self, x: int, y: int, size: int, content_size: int, horizontal: bool = False, row_size: int = 16, anchors: list[int] = [0, 0], z_index: int = 0):
        self.z_index = z_index
        self.x = x
        self.y = y
        self.anchors = anchors

        self.content_size = content_size
        self.horizontal = horizontal
        self.row_size = row_size

        self.progress = 0

        self.resize(size)
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

        self.button_a = RetroButton(self.name_a, self.x, self.y, self.SCRLBAR_WIDTH, self.SCRLBAR_WIDTH, colors = c, onpressed = self.up, anchors = self.anchors)
        s = self.scrl_size + self.SCRLBAR_WIDTH
        self.button_b = RetroButton(self.name_b, self.x + (0 if not self.horizontal else s), self.y + (0 if self.horizontal else s), self.SCRLBAR_WIDTH, self.SCRLBAR_WIDTH, colors = c, onpressed = self.down, anchors = self.anchors)

    def resize (self, size):
        self.size = size
        self.start = self.x if self.horizontal else self.y
        # btn - the scrolling one
        self.scrl_size = self.size - self.SCRLBAR_WIDTH * 2
        self.btn_size = self.scrl_size * (self.scrl_size / self.content_size)
        if self.btn_size < 8: self.btn_size = 8

        self.set_progress(self.progress)

    def up (self, _):
        self.btn_pos -= self.row_size * (self.scrl_size / self.content_size) * app_state.get_dt()
        self.update_progress()

    def down (self, _):
        self.btn_pos += self.row_size * (self.scrl_size / self.content_size) * app_state.get_dt()
        self.update_progress()

    def get_progress (self):
        s = self.SCRLBAR_WIDTH
        return (self.btn_pos - s) / (self.scrl_size - self.btn_size)

    def set_progress (self, progress: float):
        self.btn_pos = (self.scrl_size - self.btn_size) * progress + self.SCRLBAR_WIDTH
        self.progress = progress

    def get_rect (self, container_rect):
        w = self.size if self.horizontal else self.SCRLBAR_WIDTH
        h = self.size if not self.horizontal else self.SCRLBAR_WIDTH
        x = self.x
        y = self.y

        if self.anchors[0]: x = container_rect.x + container_rect.w - self.x - w
        if self.anchors[1]: y = container_rect.y + container_rect.h - self.y - h

        return pygame.Rect(x, y, w, h)

    def update (self, mouse_pos, mouse_btns, container_pos, container_rect: pygame.Rect):
        # re-calculate mouse pos, because container has different origin
        mouse_pos = list(mouse_pos)
        mouse_pos[0] -= container_pos[0]
        mouse_pos[1] -= container_pos[1]

        self.__prev_btn_pressed = self.btn_pressed

        self.resize(container_rect.size[int(not self.horizontal)])

        # scrollbar button handling
        r = self.get_rect(container_rect)
        if not self.horizontal:
            self.btn_rect = pygame.Rect(r.x, r.y + self.btn_pos, self.SCRLBAR_WIDTH, self.btn_size)
            mp = mouse_pos[1]
            self.start = self.y
        else:
            self.btn_rect = pygame.Rect(r.x + self.btn_pos, r.y, self.btn_size, self.SCRLBAR_WIDTH)
            mp = mouse_pos[0]
            self.start = self.x

        # moving cuz of btns
        self.start += self.SCRLBAR_WIDTH

        self.btn_focused = self.btn_rect.collidepoint(mouse_pos) or self.btn_pressed
        self.btn_pressed = self.btn_focused and mouse_btns[0] and not app_state.resizing

        if not self.__prev_btn_pressed and self.btn_pressed: self.mouse_diff = mp - self.btn_pos
        if self.btn_focused and self.btn_pressed: self.btn_pos = mp - self.mouse_diff

        self.button_a.update(mouse_pos, mouse_btns, container_rect.size)
        self.button_b.update(mouse_pos, mouse_btns, container_rect.size)

        self.update_progress()

    def update_progress (self):
        # keeping in bounds
        if self.btn_pos < self.start: self.btn_pos = self.start
        if self.btn_pos > self.start + self.scrl_size - self.btn_size: self.btn_pos = self.start + self.scrl_size - self.btn_size

        self.progress = self.get_progress()

    def render (self, win, _, container_rect: pygame.Rect):

        # bar
        w = self.scrl_size if self.horizontal else self.SCRLBAR_WIDTH
        h = self.scrl_size if not self.horizontal else self.SCRLBAR_WIDTH

        r = self.get_rect(container_rect)
        _x = r.x
        _y = r.y
        x = _x + (0 if not self.horizontal else self.SCRLBAR_WIDTH)
        y = _y + (0 if self.horizontal else self.SCRLBAR_WIDTH)
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


