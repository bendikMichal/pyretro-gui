
import pygame
import sys

if sys.platform != "win32":
    from retro_screen import x_can_minimize

from constants import UI_FPS

import time
class app_state:
    running = True
    widgets = []
    events = []
    _dt = 1
    lt = time.time()
    origin_press = None
    resizing = False
    hidden_buttons_count = 0

    windowized_size = (0, 0)
    windowized_pos = (0, 0)

    flags = 0

    Window: pygame.Surface = None

    moving = False

    @staticmethod
    def set_hidden_count ():
        app_state.hidden_buttons_count = int(not app_state.flags & pygame.RESIZABLE)
        if sys.platform != "win32":
            # + 1 if can not minimize
            app_state.hidden_buttons_count += int(not x_can_minimize())

    @staticmethod
    def get_hidden_count ():
        return app_state.hidden_buttons_count

    @staticmethod
    def update_dt ():
        app_state._dt = time.time() - app_state.lt
        app_state._dt *= UI_FPS
        app_state.lt = time.time()

    @staticmethod
    def get_dt ():
        return app_state._dt
