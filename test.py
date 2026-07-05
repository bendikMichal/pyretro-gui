
# do NOT learn from this file
# import pyretro_gui as rg
__package__ = "pyretro_gui"
from pyretro_gui.dialog import open_dialog, messagebox_show
from .pyretro_gui import app_state, close_app, quit_app, MenuBar, MenuItem, DropDown, Container, create_window, window_update, window_render, ReferenceValue, DialogFlags, DialogStatus

from .constants import SCREEN_X_POS, SCREEN_Y_POS

import pygame
create_window(640, 480, "copy - untitled_image.png", "testicon2.png", flags = pygame.RESIZABLE)
# rg.create_window(640, 480, "copy - untitled_image.png", "testicon2.png", flags = 0)

surf = pygame.Surface((50, 50))
surf.fill([255] * 3)
img = pygame.image.load("example2.png").convert()
app_state.widgets.append(
        Container(SCREEN_X_POS, SCREEN_Y_POS, 600, 400, img)
        # Container(SCREEN_X_POS, SCREEN_Y_POS, img.get_width(), img.get_height(), img)
        )

app_state.widgets.append(MenuBar([
    MenuItem("File", 0, DropDown([
        MenuItem("Open", 0, DropDown([
            MenuItem("image 1"), 
            MenuItem("image 2"), 
            MenuItem("Nested", dropdown = DropDown([
                MenuItem("Option 1"), 
                MenuItem("Option 2"),
                MenuItem("Nested deep", dropdown = DropDown([
                    MenuItem("Option 3"), 
                    MenuItem("Option 4")
                ], width = 100))
            ]))
        ])), 
        MenuItem("Close", 0, shortcut = "Alt+F4", onclick = close_app)
    ]) ),
    MenuItem("Edit", 0, None),
    MenuItem("View", 1, None)
    ]))


exit_dialog_code = ReferenceValue()

while app_state.running:
    window_update()
    window_render()
    
    if exit_dialog_code.value is not None:
        if exit_dialog_code.value == DialogStatus.YES:
            quit_app(None)
        exit_dialog_code.value = None

    if not app_state.running:
        app_state.running = True

        # messagebox_show(300, 120, "Do you really want to exit?", "", button_flags=DialogFlags.YES_NO_COMBO, out = exit_dialog_code)
        messagebox_show(300, 120, "Do you really want to exit?", "", button_flags=DialogFlags.CUSTOM, out=exit_dialog_code,
                        buttons=[("Yes", DialogStatus.YES), ("No", DialogStatus.NO), ("Hatsune Miku", 67)])




