
import subprocess
# import multiprocessing

def open_dialog(w: int, h: int, title: str, button_flags: int = 0):
    # p = multiprocessing.Process(target = __dialog, args = (w, h, title, button_flags))
    # p.start()

    print("Opening dialog with:", w, h, title, button_flags)
    res = subprocess.call("python _dialog_window.py".split())

    






