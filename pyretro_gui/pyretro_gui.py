
print(f"{__package__ = }, {__name__ = }")
# __package__ = "pyretro_gui"

import os, sys
from typing_extensions import deprecated
import pygame

pygame.init()
pygame.mixer.init(channels = 1)
from pygame.version import vernum

from .border import Border
from .menu_bar import MenuBar, MenuItem
from .retro_button import RetroButton
Button = RetroButton

from .move_button import MoveButton
from .retro_dropdown import DropDown
from .retro_icon import RetroIcon
Icon = RetroIcon
from .scrollbar import ScrollBar
from .container import Container

from .constants import SCR_BORDER, SCREEN_PAD, SCREEN_X_POS, SCREEN_Y_POS, Colors, UI_FPS, WIN_BORDER_SIZE, Flags, DialogStatus, ReferenceValue
from .app_core import app_state

from .todo import *

from .window_handler import _move_window, _maximize_app, _minimize_app, _rezize_window, WINDOW_FLAGS
from .path_handler import base_path

from .dialog import open_dialog

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
    print("Windows: pygame-ce >= 2.5.x, typing_extensions")
    print("Linux: pygame-ce >= 2.5.x, python-xlib, typing_extensions")

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


def create_window (w: int, h: int, caption: str, icon: str | None = None, flags: int = 0, titlebar_flags: int = 0):
    _win_size = (w, h)
    app_state.flags = WINDOW_FLAGS | flags
    app_state.titlebar_flags = titlebar_flags
    win = pygame.display.set_mode((w, h), app_state.flags)
    pygame.display.set_caption(caption)

    ico = None
    if icon: 
        ico = pygame.image.load(icon).convert_alpha()
        pygame.display.set_icon(ico)

    # screen = pygame.Surface((w - SCREEN_X_POS * 2 - SCR_BORDER, h - SCREEN_Y_POS - SCREEN_PAD - SCR_BORDER))
    
    # generating ui
    icon_size = RetroButton.ICON_SIZE
    pad = RetroButton.PAD
    icon_pad = RetroButton.PAD // 2

    
    app_state.set_visible_count()

    add_widget(Button(pad, pad, w = icon_size, h = icon_size, colors = [Colors.CLOSE, Colors.CLOSE_HOVER], anchors = [1, 0], onclick = close_app, z_index = 99, name = "close"))
    _minimize_btn = Button((app_state.get_visible_count() - 1) * (icon_size + icon_pad) + pad, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = _minimize_app, z_index = 99, name = "minimize")

    _maximize_button = Button(icon_size + icon_pad + pad, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = _maximize_app, z_index = 99, name = "maximize")
    if sys.platform != "win32":
        if app_state.get_visible_count() == 3:
            add_widget(_minimize_btn)
            add_widget(_maximize_button)
            add_widget(Border(border_width = 4, onpressed = _rezize_window ))
        elif app_state.get_visible_count() == 2:
            add_widget(_minimize_btn)
    else:
        if not app_state.titlebar_flags & Flags.MINMAX_DISABLED:
            add_widget(_minimize_btn)
            if flags & pygame.RESIZABLE:
                add_widget(_maximize_button)
                add_widget(Border(border_width = 4, onpressed = _rezize_window ))


    add_widget(MoveButton(app_state.get_visible_count()*(icon_size+icon_pad)+pad, pad, h = 20, anchors = [1, 0], onpressed = _move_window))
    add_widget(Icon(pad, pad, icon = ico, z_index = 99))


    app_state.Window = win


_prev_pressed = False
def window_update ():
    global _prev_pressed
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
    app_state.update_timers()
    
    if not mouse_pos: mouse_pos = pygame.mouse.get_pos()
    mouse_btns = pygame.mouse.get_pressed()
    if app_state.unclickable:
        if mouse_btns[0]:
            if app_state.timers["warn"] <= 0:
                pygame.mixer.Sound(base_path + "/sounds/warn.wav").play()
                app_state.restart_timer("warn")

        mouse_btns = (0, 0, 0)
        mouse_pos = (0, 0)

    if (mouse_btns[0] and not _prev_pressed): app_state.origin_press = mouse_pos
    _prev_pressed = mouse_btns[0]

    app_state.widgets.sort(key = lambda i: i.z_index)
    for w in app_state.widgets:
        w.update(mouse_pos, mouse_btns, window.get_size())


def window_render ():
    window = app_state.Window

    # clear window
    win_size = window.get_size()
    window.fill(Colors.BG) 

    # draw widgets
    for w in app_state.widgets:
        w.render(window, window.get_size())

    if app_state.unclickable:
        s = pygame.Surface(window.get_size())
        s.fill([125] * 3)
        window.blit(s, (0, 0), special_flags = pygame.BLEND_ADD)

    # draw window border
    pygame.draw.rect(window, Colors.TEXT, (-1, -1, win_size[0] + 1, win_size[1] + 1), WIN_BORDER_SIZE)
    
    pygame.display.update()



# UI stuff ======================================
def add_widget (Widget):
    """
    Widget: Widget
    Accepts any pyretro-gui Widget instance as a parameter and adds it to the widget list.
    """
    if Widget is None:
        Exception("Widget cannot be None!")

    app_state.widgets.append(Widget)
    return Widget

@deprecated("Use add_widget() instead")
def create_button (name: str, x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0], z_index = 0):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = RetroButton(x, y, w, h, colors, onclick, onpressed, anchors, z_index = z_index, name = name)
    app_state.widgets.append(_btn)
    return _btn

@deprecated("Use add_widget() instead")
def create_move_button (x: int, y: int, w: int = 32, h: int = 32, colors: list[tuple] = [Colors.BG, Colors.LIGHT_BG], border_color: tuple = Colors.TEXT, shadow_color: tuple = Colors.SHADOW, onclick = None, onpressed = None, anchors: list[int] = [0, 0, 0, 0], z_index = 0):
    """
    colors: list[tuple] : [normal_color, hover_color] # eg. [(0, 0, 0), (255, 255, 255)] 
    anchors: list[int]  : [right, bottom] # eg. [1, 1]; when used with x = 4, y = 4 the button will be 4 pixels from right edge and 4 pixels from bottom 
    """
    _btn = MoveButton(x, y, w, h, colors, border_color, shadow_color, onclick, onpressed, anchors, z_index = z_index)
    app_state.widgets.append(_btn)
    return _btn

@deprecated("Use add_widget() instead")
def create_icon (x: int, y: int, w: int = 24, h: int = 32, color: tuple = Colors.BG, border_color: tuple = Colors.TEXT, icon: pygame.Surface | None = None, anchors: list[int] = [0, 0], z_index = 0):
    _btn = RetroIcon(x, y, w, h, color, border_color, icon, anchors, z_index = z_index)
    app_state.widgets.append(_btn)
    return _btn

