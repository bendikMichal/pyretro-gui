
from pyretro_gui import Button, add_widget, app_state, close_app, create_window, window_update, window_render, Flags, DialogStatus
import sys

def exit_dialog (status):
    close_app(None)
    sys.exit(status)


def __dialog (w, h, title, icon, button_flags):
    create_window(w, h, title, "", titlebar_flags = Flags.MINMAX_DISABLED)
    add_widget(Button(8, 8, h = 20, anchors = [1, 1], text = "Close", onclick = lambda _: exit_dialog(DialogStatus.CLOSE)))
    add_widget(Button(64, 8, h = 20, anchors = [1, 1], text = "Ok", onclick = lambda _: exit_dialog(DialogStatus.OK)))

    while app_state.running:
        window_update()
        window_render()


if __name__ == "__main__":
    print(sys.argv)
    w = int(sys.argv[1])
    h = int(sys.argv[2])
    title = sys.argv[3]
    icon = sys.argv[4]
    flags = int(sys.argv[5])
    __dialog(w, h, title, icon, flags)
