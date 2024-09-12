
import pygame
from retro_text import font

class MenuItem:
    def __init__(self, text: str, letter_index: int, dropdown_data: list):
        self.text = text
        self.letter_index = letter_index
        self.dropdown_data = dropdown_data

    # def render (self, win, win_size):


class MenuBar:
    MENU_PAD = 10
    MENU_START = 40
    MENU_Y = 32

    # def __init__ (self, items: dict, color: tuple = (0, 0, 0)):
    def __init__ (self, items: list[MenuItem], color: tuple = (0, 0, 0)):
        # self.items = [MenuItem(key, items[key]["letter_index"], items[key]["dropdown_data"]) for key in items]
        self.items = items

        self.color = color

    def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        pass

    def render (self, win, win_size):
        offset_pos = 0

        for i, it in enumerate(self.items):
            txt = font.render(it.text, False, self.color)
            win.blit(txt, (self.MENU_START + offset_pos, self.MENU_Y))

            offset_pos += txt.get_width() + self.MENU_PAD
