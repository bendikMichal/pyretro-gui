
import subprocess
import threading

from .constants import ReferenceValue
from .app_core import app_state
from .path_handler import base_path

def open_dialog(w: int, h: int, title: str, icon: str, button_flags: int = 0, halting = False, out: ReferenceValue | None = None):
    # p = multiprocessing.Process(target = __dialog, args = (w, h, title, button_flags))
    # p.start()
    ref = out if out is not None else ReferenceValue()

    t = threading.Thread(target = _threaded_dialog, args = (w, h, title, icon, button_flags, ref))
    t.start()
    if halting:
        t.join()
    

lock_app_state = threading.Lock()
def _threaded_dialog (w, h, title, icon, button_flags, ref):
    with lock_app_state:
        app_state.unclickable = True

    print("Opening dialog with:", w, h, title, button_flags)
    res = subprocess.call(f"python {base_path}/../_dialog_window.py {w} {h} \"{title}\" \"{icon}\" {button_flags}".split())

    with lock_app_state:
        app_state.unclickable = False

    ref.value = res
    return res

    






