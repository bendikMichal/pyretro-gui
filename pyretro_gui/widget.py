
from .app_core import app_state


class Widget:
    def __init__ (self, z_index: int = 0):
        self.rect = None

        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed
        self.clicked = False

        self.z_index = z_index

    def update (self, mouse_pos, mouse_btns):
        if self.rect: self.focused = self.rect.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0] and not app_state.resizing
        self.clicked = self.__prev_pressed and self.focused and not self.pressed
