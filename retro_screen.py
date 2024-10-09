
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
    import pygame
    from Xlib.protocol import event

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

    def x_maximize():
        window_id = pygame.display.get_wm_info()['window']
        wm_state = ds.intern_atom('_NET_WM_STATE')
        max_horz = ds.intern_atom('_NET_WM_STATE_MAXIMIZED_HORZ')
        max_vert = ds.intern_atom('_NET_WM_STATE_MAXIMIZED_VERT')

        data = [1, max_horz, max_vert,0,0]
        e = event.ClientMessage(
                window=window_id,
                client_type=wm_state,
                format=32,
                data=(32, data)
            )
        root.send_event(e, event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask)
        ds.flush()

