
import pygame

from app_core import app_state
from constants import Colors, UI_FPS
from retro_text import font

class DropDown:
    X_OFF               = 2
    DROPDOWN_PAD        = 4
    TEXT_X_OFF          = 16
    TOGGLE_DELAY        = UI_FPS / 10
    TOGGLE_DELAY_LONG   = UI_FPS / 5

    def __init__ (self, items: list = [], width: int = 150, z_index: int = 0):
        self.items = items

        self.z_index = z_index
        self.width = width
        self.rect = None
        self.focused = False
        self.opened = False
        self.child_focus = False

        self.toggle_timer = 0
    
    def toggle (self):
        if (self.toggle_timer > 0): return
        self.opened = not self.opened
        self.toggle_timer = self.TOGGLE_DELAY

    def slow_toggle (self):
        if (self.toggle_timer > 0): return
        self.opened = not self.opened
        self.toggle_timer = self.TOGGLE_DELAY_LONG

    def get_hitbox_rect (self):
        if not self.rect: return None
        pad = 2
        return pygame.Rect(self.rect.x - pad, self.rect.y, self.rect.w + pad, self.rect.h)

    def update (self, mouse_pos, mouse_btns, trigger_focused = False):
        if self.toggle_timer > 0:
            self.toggle_timer -= 1 * app_state.get_dt()

        self.focused = self.rect and self.get_hitbox_rect().collidepoint(mouse_pos)

        if not self.focused and mouse_btns[0] and self.toggle_timer <= 0 and not trigger_focused:
            self.opened = False

        for it in self.items:
            it.update(mouse_pos, mouse_btns, in_dropdown = True, parent_self = self)

    def render (self, win, rect):
        y_offset = rect.h + self.DROPDOWN_PAD
        self.rect = pygame.Rect(rect.x - self.X_OFF, rect.y + y_offset - self.DROPDOWN_PAD, self.width, 1)
        sample_h = font.render("A", False, Colors.TEXT).get_size()[1]
        self.rect.h = (sample_h + self.DROPDOWN_PAD) * len(self.items) + self.DROPDOWN_PAD

        # draw dropdown bg
        pygame.draw.rect(win, Colors.BG, self.rect)

        # draw dropdown items
        for it in self.items:
            r = pygame.Rect(rect.x, rect.y + y_offset, self.width - 4, 0)
            y_offset += it.render(win, [rect.x + self.TEXT_X_OFF, rect.y + y_offset], custom_rect = r, in_dropdown = True)[1] + self.DROPDOWN_PAD

        # dropdown border
        # self.rect.h = y_offset - self.DROPDOWN_PAD * 3
        pygame.draw.rect(win, Colors.TEXT, self.rect, 1)
        pygame.draw.rect(win, Colors.DARK_SHADOW, [self.rect.x, self.rect.y, self.rect.w - 1, self.rect.h - 1], 1)
