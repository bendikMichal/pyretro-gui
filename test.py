
import retro_gui as rg

screen = rg.create_window(640, 480, "copy - untitled_image.png", "testicon2.png")

while rg.app_state.running:

    rg.window_update()

    rg.window_render()

