
import pygame

pygame.init()

class Colors:
    # BG = (200, 177, 189)
    BG = (179, 156, 174)
    TEXT = (15, 11, 12)

UI_FPS = 60
WIN_BORDER_SIZE = 2

__internal_clock = pygame.Clock()
ui_tick = lambda: __internal_clock.tick(UI_FPS)

__win_size = (0, 0)

class app_state:
    running = True

def get_window (w: int, h: int, caption: str):
    global __win_size
    __win_size = (w, h)
    win = pygame.display.set_mode((w, h), pygame.NOFRAME)
    pygame.display.set_caption(caption)
    return win

def window_update ():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_state.running = False


def window_render (window: pygame.Surface):
    window.fill(Colors.BG) 
    pygame.draw.rect(window, Colors.TEXT, (-1, -1, __win_size[0] + 1, __win_size[1] + 1), WIN_BORDER_SIZE)
    pygame.display.update()

