
import sys


if sys.platform == "win32":
    import ctypes
    from ctypes.wintypes import POINT

    def get_mouse_pos ():
        p = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(p))
        return (int(p.x), int(p.y))
else:
    from Xlib import X, display

    ds = display.Display()
    root = ds.screen().root

    def get_mouse_pos ():
        p = root.query_pointer()
        return (p.root_x, p.root_y)
    
    def x_can_minimize():
        allowed = root.get_full_property(ds.intern_atom('_NET_SUPPORTED'), X.AnyPropertyType)
        if allowed is None:
            return False
        if ds.intern_atom('_NET_WM_ACTION_MINIMIZE') in allowed.value:
            return True
        else:
          return False

    def x_lib_get_workarea ():
        workarea = root.get_full_property(ds.intern_atom('_NET_WORKAREA'), X.AnyPropertyType)
        if workarea is None: return None
        print(workarea.value)
        return workarea.value

    x_lib_get_workarea()
