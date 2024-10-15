
from os import stat
import pygame
import sys

if sys.platform != "win32":
    from .retro_screen import x_can_minimize

from .constants import UI_FPS, Flags


import time
class app_state:
    running = True
    widgets = []
    events = []
    _dt = 1
    lt = time.time()
    origin_press = None
    resizing = False
    unclickable = False
    visible_buttons_count = 3

    windowized_size = (0, 0)
    windowized_pos = (0, 0)

    flags = 0
    titlebar_flags = 0
    
    timers = {
            "warn": 0.0
            }
    timer_lens = {
            "warn": 30 * (UI_FPS / 60)
            }

    Window: pygame.Surface = None

    moving = False

    @staticmethod
    def update_timers ():
        for k in app_state.timers:
            if (app_state.timers[k] > 0):
                app_state.timers[k] -= 1 * app_state.get_dt()

    @staticmethod
    def restart_timer (timer_name: str):
        app_state.timers[timer_name] = app_state.timer_lens[timer_name]

    @staticmethod
    def set_visible_count ():
        app_state.visible_buttons_count = 3
        if not(app_state.flags & pygame.RESIZABLE):
            app_state.visible_buttons_count -= 1
        if sys.platform != "win32":
            if not(x_can_minimize()):
                app_state.visible_buttons_count = 1

        if app_state.titlebar_flags & Flags.MINMAX_DISABLED:
            app_state.visible_buttons_count = 1


    @staticmethod
    def get_visible_count ():
        return app_state.visible_buttons_count

    @staticmethod
    def update_dt ():
        app_state._dt = time.time() - app_state.lt
        app_state._dt *= UI_FPS
        app_state.lt = time.time()

    @staticmethod
    def get_dt ():
        return app_state._dt
