
import pygame

from constants import UI_FPS

import time
class app_state:
    running = True
    widgets = []
    _dt = 1
    lt = time.time()

    flags = 0

    Window: pygame.Surface = None
    screen: pygame.Surface = None

    moving = False

    @staticmethod
    def update_dt ():
        app_state._dt = time.time() - app_state.lt
        app_state._dt *= UI_FPS
        app_state.lt = time.time()

    @staticmethod
    def get_dt ():
        return app_state._dt
