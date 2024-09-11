
import retro_gui as rg

Window = rg.get_window(640, 480, "Retro window")

while rg.app_state.running:
    rg.ui_tick()

    rg.window_update()

    rg.window_render(Window)

