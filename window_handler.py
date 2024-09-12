
import sys, os
import pygame
from retro_screen import get_mouse_pos

pygame.init()

BAR_SIZE        = 32
WINDOW_FLAGS    = pygame.NOFRAME
# WINDOW_FLAGS    = pygame.RESIZABLE

if sys.platform == "win32":
    SW_NORMAL   = 1
    SW_MAXIMIZE = 3
    SW_MINIMIZE = 6

__info = pygame.display.Info()
_win_size = (0, 0)

def move_check ():
    if not pygame.display.get_window_position or not pygame.display.set_window_position:
        print("Unable to get/set window position, update pygame-ce version! Minimum pygame-ce version is >= 2.5.x")
        os._exit(1)

def _maximize_app (btn):
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
    btn.onclick = _windowize_app

def _minimize_app (btn):
    pygame.display.iconify()

def _move_window (btn):
    move_check()

    mx, my = get_mouse_pos()
    x = mx - btn.origin_press[0]
    y = my - btn.origin_press[1]

    pygame.display.set_window_position((x, y))


def _windowize_app (btn):
    if sys.platform == "win32":
        hwnd = pygame.display.get_wm_info()["window"]

        import ctypes
        ctypes.windll.user32.ShowWindow(hwnd, SW_NORMAL)

    os.environ['SDL_VIDEO_CENTERED'] = "1"
    pygame.display.set_mode(_win_size, WINDOW_FLAGS)
    btn.name = "maximize"
    btn.load_img()
    btn.onclick = _maximize_app
