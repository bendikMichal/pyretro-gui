
import retro_gui as rg

Window = rg.get_window(640, 480, "File Open")

while rg.app_state.running:
    rg.ui_tick()

    rg.window_update(Window)

    rg.window_render(Window)

