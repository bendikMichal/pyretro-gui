
import pygame

from retro_dropdown import DropDown

from constants import Colors
from retro_text import font, small_font
from widget import Widget


class MenuItem (Widget):
    FONT_W = 6
    IT_PAD = 2

    def __init__(self, text: str, letter_index: int | None = None, dropdown: DropDown | None = None, color: tuple = Colors.TEXT, shortcut: str | None = None, shortcut_fn = lambda _: 0, onclick = None, z_index: int = 0):
        super().__init__()
        
        self.z_index = z_index
        self.text = text
        self.letter_index = letter_index
        self.shortcut_letter = None

        if self.letter_index is not None:
            self.shortcut_letter = self.text[self.letter_index].lower()

        self.shortcut = shortcut
        self.shortcut_fn = shortcut_fn
        self.onclick = onclick

        self.color = color

        self.dropdown = dropdown

        self.rect = pygame.Rect(0, 0, 1, 1)

        self.opened = False

    def update (self, mouse_pos, mouse_btns, in_dropdown = False, parent_self = None):
        super().update(mouse_pos, mouse_btns)
        self.opened = self.focused and mouse_btns[0] and self.dropdown
        
        if self.letter_index is not None and self.shortcut_letter is not None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LALT] and keys[ord(self.shortcut_letter)]:
                self.clicked = True
                self.focused = True
                if self.dropdown: self.dropdown.slow_toggle()

        # check if nested menu is opened
        if parent_self: parent_self.child_focus = self.dropdown and (self.dropdown.focused or self.dropdown.child_focus)

        # toggle dropdown
        if self.dropdown: 
            if self.clicked:
                self.dropdown.toggle()

            self.dropdown.update(mouse_pos, mouse_btns, trigger_focused = self.focused)

            if in_dropdown:
                if self.focused:
                    self.dropdown.opened = True
                    self.dropdown.focused = True

                elif not self.dropdown.focused and self.dropdown.opened and not self.dropdown.child_focus:
                    self.dropdown.opened = False


        # clicked
        if self.clicked:
            if self.onclick:
                self.onclick(self)

        self.shortcut_fn(self)
        
    def render (self, win, pos, custom_rect = None, in_dropdown = False):
        """
        custom_rect.h will be calculated based on the rendering if it == 0
        """

        txt = font.render(self.text, False, self.color)
        shortcut_txt = None
        if self.shortcut: shortcut_txt = small_font.render(self.shortcut, False, Colors.DARK_SHADOW)

        th = txt.get_height() - 2
        pos[1] = pos[1] - int(not not self.opened)
        if custom_rect is not None and custom_rect.h == 0: custom_rect.h = txt.get_height()

        # highlight
        if self.focused:
            if custom_rect is not None:
                pygame.draw.rect(win, Colors.LIGHT_BG, custom_rect)

            else:
                pygame.draw.rect(win, self.color, [
                    pos[0] - self.IT_PAD,
                    pos[1] - self.IT_PAD, 
                    txt.get_size()[0] + self.IT_PAD, 
                    txt.get_size()[1] + self.IT_PAD
                ], 1)

        # arrow
        if self.dropdown and in_dropdown and custom_rect:
            arrow_txt = font.render(">", False, Colors.TEXT)
            sp = (custom_rect.x + custom_rect.w - arrow_txt.get_width() - self.IT_PAD, pos[1] + 2)
            win.blit(arrow_txt, sp)

        # render item
        if self.letter_index is not None: pygame.draw.line(txt, self.color, (self.FONT_W * self.letter_index, th), (self.FONT_W * (self.letter_index + 1), th), 1)
        win.blit(txt, pos)
        if shortcut_txt and custom_rect: 
            sp = (custom_rect.x + custom_rect.w - shortcut_txt.get_width() - self.IT_PAD, pos[1] + 2)
            win.blit(shortcut_txt, sp)

        # update rect based on rendering
        if custom_rect is not None:
            self.rect = custom_rect
        else:
            self.rect = txt.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]

        # draw dropdown
        if self.dropdown:
            if self.dropdown.opened:
                r = self.rect.copy()
                if in_dropdown:
                    r.x = r.x + r.w + 4
                    # r.x = r.x + r.w
                    r.y = r.y - r.h - DropDown.DROPDOWN_PAD

                self.dropdown.render(win, r)

        # update offset
        return txt.get_size()


class MenuBar:
    MENU_PAD = 10
    MENU_START = 40
    MENU_Y = 32

    # def __init__ (self, items: dict, color: tuple = (0, 0, 0)):
    def __init__ (self, items: list[MenuItem], z_index: int = 0):
        # self.items = [MenuItem(key, items[key]["letter_index"], items[key]["dropdown_data"]) for key in items]
        self.z_index = z_index
        self.items = items


    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        for it in self.items:
            it.update(mouse_pos, mouse_btns)

    def render (self, win, win_size):
        offset_pos = 0

        for it in self.items:
            pos = [self.MENU_START + offset_pos, self.MENU_Y]
            offset_pos += it.render(win, pos)[0] + self.MENU_PAD

