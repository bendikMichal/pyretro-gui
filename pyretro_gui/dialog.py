
import subprocess
import threading

from .constants import ReferenceValue
from .app_core import app_state
from .path_handler import base_path

def open_dialog(w: int, h: int, title: str, icon: str, button_flags: int = 0, halting = False, out: ReferenceValue | None = None, buttons = []):
    # p = multiprocessing.Process(target = __dialog, args = (w, h, title, button_flags))
    # p.start()
    ref = out if out is not None else ReferenceValue()

    t = threading.Thread(target = _threaded_dialog, args = (w, h, title, icon, button_flags, ref, buttons))
    t.start()
    if halting:
        t.join()
    
messagebox_show = open_dialog

lock_app_state = threading.Lock()
def _threaded_dialog (w, h, title, icon, button_flags, ref, buttons):
    with lock_app_state:
        app_state.unclickable = True

    print("Opening dialog with:", w, h, title, button_flags, buttons)
    command = f"python$|{base_path}/../_dialog_window.py$|{w}$|{h}$|\"{title}\"$|\"{icon}\"$|{button_flags}"
    for btn in buttons:
        command += f"$|{btn[0]}$|{btn[1]}"
    res = subprocess.call(command.split("$|"))

    with lock_app_state:
        app_state.unclickable = False

    ref.value = res
    return res

    






