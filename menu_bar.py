
import pygame
from retro_text import font

class MenuItem:
    def __init__(self, text: str, letter_index: int, dropdown_data: list):
        self.text = text
        self.letter_index = letter_index
        self.dropdown_data = dropdown_data

        self.rect = pygame.Rect(0, 0, 1, 1)
        self.focused = False

    def update (self, mouse_pos, mouse_btns, win_size):
        self.focused = self.rect.collidepoint(mouse_pos)

    # def render (self, win, win_size):




class MenuBar:
    MENU_PAD = 10
    MENU_START = 40
    MENU_Y = 32
    FONT_W = 6
    IT_PAD = 2

    # def __init__ (self, items: dict, color: tuple = (0, 0, 0)):
    def __init__ (self, items: list[MenuItem], color: tuple = (0, 0, 0), focus_bg_color: tuple = (0, 0, 0)):
        # self.items = [MenuItem(key, items[key]["letter_index"], items[key]["dropdown_data"]) for key in items]
        self.items = items

        self.color = color
        self.focus_bg_color = focus_bg_color

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        for it in self.items:
            it.update(mouse_pos, mouse_btns, win_size)

    def render (self, win, win_size):
        offset_pos = 0

        for it in self.items:
            txt = font.render(it.text, False, self.color)
            th = txt.get_height() - 2

            if it.focused:
                pygame.draw.rect(win, self.color, [
                    self.MENU_START + offset_pos - self.IT_PAD,
                    self.MENU_Y - self.IT_PAD, 
                    txt.get_size()[0] + self.IT_PAD, 
                    txt.get_size()[1] + self.IT_PAD
                ], 1)

            pygame.draw.line(txt, self.color, (self.FONT_W * it.letter_index, th), (self.FONT_W * (it.letter_index + 1), th), 1)
            win.blit(txt, (self.MENU_START + offset_pos, self.MENU_Y))

            # update rect based on rendering
            it.rect = txt.get_rect()
            it.rect.x = self.MENU_START + offset_pos
            it.rect.y = self.MENU_Y

            offset_pos += txt.get_width() + self.MENU_PAD
