
class Widget:
    def __init__ (self):
        self.rect = None

        self.focused = False
        self.pressed = False
        self.__prev_pressed = self.pressed
        self.clicked = False

    def update (self, mouse_pos, mouse_btns):
        if self.rect: self.focused = self.rect.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0]
        self.clicked = self.__prev_pressed and self.focused and not self.pressed
