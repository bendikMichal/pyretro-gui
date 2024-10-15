
class Colors:
    BG          = (179, 156, 174)
    LIGHT_BG    = (217, 186, 202)
    TEXT        = (15, 11, 12)
    CLOSE       = (232, 127, 141)
    CLOSE_HOVER = (235, 153, 165)
    SHADOW      = (158, 133, 152)
    DARK_SHADOW = (132, 113, 132)

UI_FPS          = 60
WIN_BORDER_SIZE = 2

SCR_BORDER      = 1
# actual values are SCR_BORDER smaller, cuz of the border
SCREEN_PAD      = 5
SCREEN_X_POS    = SCREEN_PAD
SCREEN_Y_POS    = 53

class Flags:
    MINMAX_DISABLED = 1

class DialogStatus:
    CLOSE   = 0
    OK      = 1

    NO      = CLOSE
    YES     = OK

class DialogFlags:
    class DialogType:
        INFO    = 0
        WARNING = 1
        ERROR   = 2

    OK_CLOSE_COMBO  = 0
    YES_NO_COMBO    = 1



# not really a constant but a type
class ReferenceValue:
    def __init__ (self, value = None):
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)
