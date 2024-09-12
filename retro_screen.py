
import sys


if sys.platform == "win32":
    import ctypes
    from ctypes.wintypes import POINT

    def get_mouse_pos ():
        p = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(p))
        return (int(p.x), int(p.y))
else:
    from Xlib import display

    ds = display.Display()
    root = ds.screen().root

    def get_mouse_pos ():
        p = root.query_pointer()
        return (p.root_x, p.root_y)
