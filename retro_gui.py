

import os, sys
import pygame
from pygame.version import vernum
from menu_bar import MenuBar, MenuItem
from retro_button import RetroButton
from move_button import MoveButton
from retro_icon import RetroIcon
import window_handler as wh

pygame.init()

def init ():
    print("Requirements: ")
    print("Windows: pygame-ce >= 2.5.x")
    print("Linux: pygame-ce >= 2.5.x, python-xlib")

    if vernum.major < 2:
        print("Required major version of pygame-ce is >= 2")
        os._exit(1)
    if vernum.major == 2 and vernum.minor < 5:
        print("Required minor version of pygame-ce is >= 5")
        os._exit(1)

init()


class Colors:
    BG          = (179, 156, 174)
    LIGHT_BG    = (217, 186, 202)
    TEXT        = (15, 11, 12)
    CLOSE       = (232, 127, 141)
    CLOSE_HOVER = (235, 153, 165)
    SHADOW      = (158, 133, 152)

UI_FPS          = 60
WIN_BORDER_SIZE = 2


__internal_clock = pygame.Clock()
ui_tick = lambda: __internal_clock.tick(UI_FPS)


class app_state:
    running = True
    widgets = []

def __close_app (_):
    app_state.running = False


def get_window (w: int, h: int, caption: str, icon: str | None = None):
    wh._win_size = (w, h)
    win = pygame.display.set_mode((w, h), wh.WINDOW_FLAGS)
    pygame.display.set_caption(caption)

    ico = None
    if icon: 
        ico = pygame.image.load(icon).convert_alpha()
        pygame.display.set_icon(ico)

    icon_size = RetroButton.ICON_SIZE
    pad = RetroButton.PAD
    icon_pad = RetroButton.PAD // 2

    create_button("close", pad, pad, w = icon_size, h = icon_size, colors = [Colors.CLOSE, Colors.CLOSE_HOVER], anchors = [1, 0], onclick = __close_app)
    create_button("maximize", icon_size + icon_pad + pad, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = wh._maximize_app)
    create_button("minimize", (icon_size + icon_pad) * 2 + pad, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = wh._minimize_app)
    create_move_button(icon_size * 3 + pad * 3, pad, h = 20, anchors = [1, 0], onpressed = wh._move_window)
    create_icon(pad, pad, icon = ico)

    app_state.widgets.append(MenuBar([
        MenuItem("File", 0, []),
        MenuItem("Open", 0, [])
        ]))
    return win

def window_update (window: pygame.Surface):
    mouse_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_state.running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

    if not mouse_pos: mouse_pos = pygame.mouse.get_pos()
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

def create_button (name: str, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0]):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = RetroButton(name, x, y, w, h, colors, onclick, onpressed, anchors)
    app_state.widgets.append(_btn)
    return _btn

def create_move_button (x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], border_color: tuple = Colors.TEXT, shadow_color: tuple = Colors.SHADOW, onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0]):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = MoveButton(x, y, w, h, colors, border_color, shadow_color, onclick, onpressed, anchors)
    app_state.widgets.append(_btn)
    return _btn

def create_icon (x: int, y: int, w: int = 24, h: int = 32, color: tuple = Colors.BG, border_color: tuple = Colors.TEXT, icon: pygame.Surface | None = None, anchors: list[int] = [0, 0]):
    _btn = RetroIcon(x, y, w, h, color, border_color, icon, anchors)
    app_state.widgets.append(_btn)
    return _btn

