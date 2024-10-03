
import os, sys
from re import S
import pygame

from border import Border


pygame.init()

from pygame.version import vernum
from menu_bar import MenuBar, MenuItem
from retro_button import RetroButton
from move_button import MoveButton
from retro_dropdown import DropDown
from retro_icon import RetroIcon
from scrollbar import ScrollBar
from container import Container

from constants import SCR_BORDER, SCREEN_PAD, SCREEN_X_POS, SCREEN_Y_POS, Colors, UI_FPS, WIN_BORDER_SIZE
from app_core import app_state

import todo

import window_handler as wh


def init ():
    print(
        """
    |> Docs:
    |>     https://github.com/bendikMichal/pyretro-gui/blob/master/docs/docs.md
    |>
    |>
        """
        )


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


__internal_clock = pygame.Clock()
ui_tick = lambda: __internal_clock.tick(UI_FPS)

def close_app (_):
    app_state.running = False


def create_window (w: int, h: int, caption: str, icon: str | None = None, flags: int = 0):
    wh._win_size = (w, h)
    app_state.flags = wh.WINDOW_FLAGS | flags
    win = pygame.display.set_mode((w, h), app_state.flags)
    pygame.display.set_caption(caption)

    ico = None
    if icon: 
        ico = pygame.image.load(icon).convert_alpha()
        pygame.display.set_icon(ico)

    screen = pygame.Surface((w - SCREEN_X_POS * 2 - SCR_BORDER, h - SCREEN_Y_POS - SCREEN_PAD - SCR_BORDER))
    
    # generating ui
    icon_size = RetroButton.ICON_SIZE
    pad = RetroButton.PAD
    icon_pad = RetroButton.PAD // 2

    neg = int(not flags & pygame.RESIZABLE)
    create_button("close", pad, pad, w = icon_size, h = icon_size, colors = [Colors.CLOSE, Colors.CLOSE_HOVER], anchors = [1, 0], onclick = close_app, z_index = 99)
    create_button("minimize", (icon_size + icon_pad) * (2 - neg) + pad, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = wh._minimize_app, z_index = 99)
    create_move_button((icon_size + pad) * (3 - neg), pad, h = 20, anchors = [1, 0], onpressed = wh._move_window)
    create_icon(pad, pad, icon = ico, z_index = 99)

    if flags & pygame.RESIZABLE:
        create_button("maximize", icon_size + icon_pad + pad, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = wh._maximize_app, z_index = 99)
        app_state.widgets.append(Border(border_width = 4, onpressed = wh._rezize_window ))


    app_state.Window = win
    app_state.screen = screen
    return screen


def window_update ():
    window = app_state.Window
    ui_tick()

    mouse_pos = None
    app_state.events = []
    for event in pygame.event.get():
        app_state.events.append(event)

        if event.type == pygame.QUIT:
            app_state.running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos


    app_state.update_dt()
    
    if not mouse_pos: mouse_pos = pygame.mouse.get_pos()
    mouse_btns = pygame.mouse.get_pressed()

    app_state.widgets.sort(key = lambda i: i.z_index)
    for w in app_state.widgets:
        w.update(mouse_pos, mouse_btns, window.get_size())


def window_render ():
    window = app_state.Window

    # clear window
    win_size = window.get_size()
    window.fill(Colors.BG) 

    # draw screen
    # if app_state.screen:
    #     s = app_state.screen.get_size()
    #     pygame.draw.rect(window, Colors.TEXT, (SCREEN_X_POS - SCR_BORDER, SCREEN_Y_POS - SCR_BORDER, s[0] + SCR_BORDER * 2, s[1] + SCR_BORDER * 2), SCR_BORDER)
    #     window.blit(app_state.screen, (SCREEN_X_POS, SCREEN_Y_POS))
    
    # draw widgets
    for w in app_state.widgets:
        w.render(window, window.get_size())

    # draw window border
    pygame.draw.rect(window, Colors.TEXT, (-1, -1, win_size[0] + 1, win_size[1] + 1), WIN_BORDER_SIZE)
    
    pygame.display.update()



# UI stuff ======================================

def create_button (name: str, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0], z_index = 0):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = RetroButton(name, x, y, w, h, colors, onclick, onpressed, anchors, z_index = z_index)
    app_state.widgets.append(_btn)
    return _btn

def create_move_button (x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], border_color: tuple = Colors.TEXT, shadow_color: tuple = Colors.SHADOW, onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0], z_index = 0):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = MoveButton(x, y, w, h, colors, border_color, shadow_color, onclick, onpressed, anchors, z_index = z_index)
    app_state.widgets.append(_btn)
    return _btn

def create_icon (x: int, y: int, w: int = 24, h: int = 32, color: tuple = Colors.BG, border_color: tuple = Colors.TEXT, icon: pygame.Surface | None = None, anchors: list[int] = [0, 0], z_index = 0):
    _btn = RetroIcon(x, y, w, h, color, border_color, icon, anchors, z_index = z_index)
    app_state.widgets.append(_btn)
    return _btn

