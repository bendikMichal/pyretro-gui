
import pygame

from retro_dropdown import DropDown

from constants import Colors
from retro_text import font, small_font

class MenuItem:
    FONT_W = 6
    IT_PAD = 2

    def __init__(self, text: str, letter_index: int, dropdown: DropDown | None = None, color: tuple = Colors.TEXT, shortcut: str | None = None, shortcut_fn = lambda _: 0, onclick = None):
        self.text = text
        self.letter_index = letter_index
        self.shortcut = shortcut
        self.shortcut_fn = shortcut_fn
        self.onclick = onclick

        self.color = color

        self.dropdown = dropdown

        self.rect = pygame.Rect(0, 0, 1, 1)

        self.focused = False
        self.opened = False
        self.pressed = False
        self.__prev_pressed = self.pressed

    def update (self, mouse_pos, mouse_btns):
        self.focused = self.rect.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0]
        self.opened = self.focused and mouse_btns[0] and self.dropdown

        if self.dropdown: 
            if mouse_btns[0] and self.focused: self.dropdown.toggle()
            self.dropdown.update(mouse_pos, mouse_btns)

        # clicked
        if not self.pressed and self.__prev_pressed and self.focused:
            if self.onclick:
                self.onclick(self)

        self.shortcut_fn(self)
        
    def render (self, win, pos, custom_rect = None):
        """
        custom_rect.h will be calculated based on the rendering if it == 0
        """

        txt = font.render(self.text, False, self.color)
        shortcut_txt = None
        if self.shortcut: shortcut_txt = small_font.render(self.shortcut, False, Colors.DARK_SHADOW)

        th = txt.get_height() - 2
        pos[1] = pos[1] - int(not not self.opened)
        if custom_rect is not None and custom_rect.h == 0: custom_rect.h = txt.get_height()

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

        # render item
        pygame.draw.line(txt, self.color, (self.FONT_W * self.letter_index, th), (self.FONT_W * (self.letter_index + 1), th), 1)
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
            if self.opened or self.dropdown.opened:
                self.dropdown.render(win, self.rect)

        # update offset
        return txt.get_size()


class MenuBar:
    MENU_PAD = 10
    MENU_START = 40
    MENU_Y = 32

    # def __init__ (self, items: dict, color: tuple = (0, 0, 0)):
    def __init__ (self, items: list[MenuItem]):
        # self.items = [MenuItem(key, items[key]["letter_index"], items[key]["dropdown_data"]) for key in items]
        self.items = items


    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        for it in self.items:
            it.update(mouse_pos, mouse_btns)

    def render (self, win, win_size):
        offset_pos = 0

        for it in self.items:
            pos = [self.MENU_START + offset_pos, self.MENU_Y]
            offset_pos += it.render(win, pos)[0] + self.MENU_PAD

