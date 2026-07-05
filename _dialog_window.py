
from pyretro_gui import Button, add_widget, app_state, close_app, create_window, window_update, window_render, Flags, DialogStatus, DialogFlags
import sys

def exit_dialog (status):
    close_app(None)
    sys.exit(status)


def __dialog (w, h, title, icon, button_flags):
    create_window(w, h, title, "", titlebar_flags = Flags.MINMAX_DISABLED, always_on_top = True)

    close_text = "No" if button_flags & DialogFlags.YES_NO_COMBO else "Close"
    ok_text = "Yes" if button_flags & DialogFlags.YES_NO_COMBO else "Ok"
    b1 = add_widget(Button(8, 8, h = 20, anchors = [1, 1], text = close_text, onclick = lambda _: exit_dialog(DialogStatus.CLOSE)))
    b2 = add_widget(Button(16 + b1.w, 8, h = 20, anchors = [1, 1], text = ok_text, onclick = lambda _: exit_dialog(DialogStatus.OK)))

    while app_state.running:
        window_update()
        b2.x = 16 + b1.w

        window_render()

def __customizable_dialog (w, h, title, icon, buttons):
    create_window(w, h, title, "", titlebar_flags = Flags.MINMAX_DISABLED, always_on_top = True)

    x_start_origin = 8

    x_start = x_start_origin
    for button_info in reversed(buttons):
        button_name, button_status = button_info
        b = Button(x_start, 8, h = 20, anchors = [1, 1], text = button_name, onclick = lambda _: exit_dialog(button_status))
        add_widget(b)
        b.recalc_dimensions()
        x_start += 16 + b.w

    while app_state.running:
        window_update()
        window_render()


if __name__ == "__main__":
    print(sys.argv)
    w = int(sys.argv[1])
    h = int(sys.argv[2])
    title = sys.argv[3].replace("\"", "")
    icon = sys.argv[4].replace("\"", "")
    flags = int(sys.argv[5])

    if not (flags & DialogFlags.CUSTOM):
        __dialog(w, h, title, icon, flags)

    if len(sys.argv) > 6 and len(sys.argv)%2 == 0:
        buttons = []
        for i in range(6, len(sys.argv), 2):
            buttons.append((sys.argv[i], int(sys.argv[i+1])))
        __customizable_dialog(w, h, title, icon, buttons)

    else:
        print("Incorrect amount of arguments!")
        sys.exit(DialogStatus.ERROR)
