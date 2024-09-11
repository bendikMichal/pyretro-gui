
import os
import pygame
from retro_button import RetroButton

pygame.init()

class Colors:
    BG = (179, 156, 174)
    LIGHT_BG = (217, 186, 202)
    TEXT = (15, 11, 12)
    CLOSE = (232, 127, 141)
    CLOSE_HOVER = (235, 153, 165)

UI_FPS = 60
WIN_BORDER_SIZE = 2
WINDOW_FLAGS = pygame.NOFRAME | pygame.RESIZABLE

__internal_clock = pygame.Clock()
ui_tick = lambda: __internal_clock.tick(UI_FPS)

__info = pygame.display.Info()
print(__info.current_w, __info.current_h)
__win_size = (0, 0)

class app_state:
    running = True
    widgets = []

def __close_app (_):
    app_state.running = False

def __maximize_app (btn):
    os.environ['SDL_VIDEO_CENTERED'] = "1"
    pygame.display.set_mode((__info.current_w, __info.current_h), WINDOW_FLAGS)

def get_window (w: int, h: int, caption: str):
    global __win_size
    __win_size = (w, h)
    win = pygame.display.set_mode((w, h), WINDOW_FLAGS)
    pygame.display.set_caption(caption)

    icon_size = 24
    pad = 6
    create_button("close", icon_size + pad, pad, w = icon_size, h = icon_size, colors = [Colors.CLOSE, Colors.CLOSE_HOVER], anchors = [1, 0], onclick = __close_app)
    create_button("maximize", (icon_size + pad) * 2, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = __maximize_app)
    return win

def window_update (window: pygame.Surface):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_state.running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_btns = pygame.mouse.get_pressed()

    for w in app_state.widgets:
        w.update(mouse_pos, mouse_btns, window.get_size())

def window_render (window: pygame.Surface):
    win_size = window.get_size()
    window.fill(Colors.BG) 
    
    for w in app_state.widgets:
        w.render(window, window.get_size())

    pygame.draw.rect(window, Colors.TEXT, (-1, -1, win_size[0] + 1, win_size[1] + 1), WIN_BORDER_SIZE)
    pygame.display.update()



# UI stuff ======================================

def create_button (name: str, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], onclick = None, anchors: list[int] = [0, 0, 0, 0]):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = RetroButton(name, x, y, w, h, colors, onclick, anchors)
    app_state.widgets.append(_btn)
    return _btn
