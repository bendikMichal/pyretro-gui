
import subprocess
import threading

from .app_core import app_state
# import multiprocessing

from .path_handler import base_path

def open_dialog(w: int, h: int, title: str, icon: str, button_flags: int = 0, halting = False):
    # p = multiprocessing.Process(target = __dialog, args = (w, h, title, button_flags))
    # p.start()

    t = threading.Thread(target = _threaded_dialog, args = (w, h, title, icon, button_flags))
    t.start()
    if halting:
        t.join()

lock_app_state = threading.Lock()
def _threaded_dialog (w, h, title, icon, button_flags):
    with lock_app_state:
        app_state.unclickable = True

    print("Opening dialog with:", w, h, title, button_flags)
    res = subprocess.call(f"python {base_path}/../_dialog_window.py {w} {h} \"{title}\" \"{icon}\" {button_flags}".split())

    with lock_app_state:
        app_state.unclickable = False
    return res

    






