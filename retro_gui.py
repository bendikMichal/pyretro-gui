

import os, sys
import pygame
from pygame.version import vernum
from retro_button import MoveButton, RetroButton
from retro_screen import get_mouse_pos

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

def move_check ():
    if not pygame.display.get_window_position or not pygame.display.set_window_position:
        print("Unable to get/set window position, update pygame-ce version! Minimum pygame-ce version is >= 2.5.x")
        os._exit(1)

class Colors:
    BG          = (179, 156, 174)
    LIGHT_BG    = (217, 186, 202)
    TEXT        = (15, 11, 12)
    CLOSE       = (232, 127, 141)
    CLOSE_HOVER = (235, 153, 165)
    SHADOW      = (158, 133, 152)

UI_FPS          = 60
WIN_BORDER_SIZE = 2
BAR_SIZE        = 48
WINDOW_FLAGS    = pygame.NOFRAME
# WINDOW_FLAGS = pygame.RESIZABLE

if sys.platform == "win32":
    SW_NORMAL   = 1
    SW_MAXIMIZE = 3
    SW_MINIMIZE = 6

__internal_clock = pygame.Clock()
ui_tick = lambda: __internal_clock.tick(UI_FPS)

__info = pygame.display.Info()
__win_size = (0, 0)

class app_state:
    running = True
    widgets = []

def __close_app (_):
    app_state.running = False

def __maximize_app (btn):
    if sys.platform == "win32":
        move_check()
        pygame.display.set_mode((1, 1), pygame.RESIZABLE)
        hwnd = pygame.display.get_wm_info()["window"]

        import ctypes
        ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
        size = list(pygame.display.get_window_size()).copy()

        titlebar_h = ctypes.windll.user32.GetSystemMetrics(4)
        size[1] += titlebar_h

        pygame.display.set_mode((1, 1), WINDOW_FLAGS)
        pygame.display.set_mode(size, WINDOW_FLAGS)

        x, y = pygame.display.get_window_position()
        pygame.display.set_window_position((x, y - titlebar_h))

    else:
        pygame.display.set_mode((__info.current_w, __info.current_h - BAR_SIZE), WINDOW_FLAGS)
        pygame.display.set_window_position((0, 0))

    btn.name = "windowize"
    btn.load_img()
    btn.onclick = __windowize_app

def __minimize_app (btn):
    pygame.display.iconify()

def __move_window (btn):
    move_check()

    x, y = pygame.display.get_window_position()
    # mpos = pygame.mouse.get_pos()
    # dist_x = mpos[0] - btn.origin_press[0]
    # dist_y = mpos[1] - btn.origin_press[1]

    # x += dist_x
    # y += dist_y
    mx, my = get_mouse_pos()
    x = mx - btn.origin_press[0]
    y = my - btn.origin_press[1]

    pygame.display.set_window_position((x, y))


def __windowize_app (btn):
    if sys.platform == "win32":
        hwnd = pygame.display.get_wm_info()["window"]

        import ctypes
        ctypes.windll.user32.ShowWindow(hwnd, SW_NORMAL)

    os.environ['SDL_VIDEO_CENTERED'] = "1"
    pygame.display.set_mode(__win_size, WINDOW_FLAGS)
    btn.name = "maximize"
    btn.load_img()
    btn.onclick = __maximize_app


def get_window (w: int, h: int, caption: str, icon: str | None = None):
    global __win_size
    __win_size = (w, h)
    win = pygame.display.set_mode((w, h), WINDOW_FLAGS)
    pygame.display.set_caption(caption)
    if icon: pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

    icon_size = RetroButton.ICON_SIZE
    pad = RetroButton.PAD
    create_button("close", pad, pad, w = icon_size, h = icon_size, colors = [Colors.CLOSE, Colors.CLOSE_HOVER], anchors = [1, 0], onclick = __close_app)
    create_button("maximize", icon_size + pad * 2, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = __maximize_app)
    create_button("minimize", icon_size * 2 + pad * 3, pad, w = icon_size, h = icon_size, anchors = [1, 0], onclick = __minimize_app)
    create_move_button(icon_size * 3 + pad * 4, pad, w = w - (MoveButton.APPICON_SIZE + (icon_size + pad) * 4), h = 20, anchors = [1, 0], onpressed = __move_window)
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
