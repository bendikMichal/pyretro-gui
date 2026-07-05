# PyRetro-Gui Docs

## Table of contents
1. [Importing](#Importing)
2. [Creating a window](#Creating-a-window)
3. [Setting UI refresh rate](#Setting-UI-refresh-rate)
4. [Main app loop](#Main-app-loop)
5. [Quitting app](#Quitting-app)
6. [Creating Menu Bar](#Creating-Menu-Bar)
7. [Menu Item](#Menu-Item)
8. [DropDown](#DropDown)
9. [Scrollbar](#Scrollbar)
10. [Container](#Container)
11. [Buttons](#RetroButton)
12. [About widgets](#Widgets)
13. [Adding widgets](#Adding-Widgets)
14. [Screen](#Screen)
15. [Dialog (MessageBox)](#Dialog)


### Importing
```python
import pyretro_gui as rg
```

### Creating a window
- recommended icon size is `24x32`px
```python
rg.create_window(640, 480, "Test App title", "test_icon.png")
```
- to make a resizable window use `pygame.RESIZABLE`
```python
rg.create_window(640, 480, "Test App title", "test_icon.png", flags = pygame.RESIZABLE)
```
> [!NOTE]
> Resizable window is highly experimental and might cause issues such as crashes, also rest of the flags are ignored except this one as of writing
- to make window always on top you can use `always_on_top=True` in the `rg.create_window`
> [!NOTE]
> Always on top setting might not work on all platforms


### Setting UI refresh rate 
> [!NOTE]
> OPTIONAL, default is 60
```python
rg.UI_FPS = 30
```

### Main app loop
```python
while rg.app_state.running:
    rg.window_update()
    rg.window_render()
```

### Quitting app
There are two functions that are used to quit. `close_app` and `quit_app`.
- `close_app` is a simpler and in a sense weaker, it just sets `running` to false.
- `quit_app` is a stronger option which unconditionally closes the app.
These two can be used in tandem with [Dialog (MessageBox)](#Dialog) to make a more complex closing mechanism such as:
```python
exit_dialog_code = ReferenceValue()

while app_state.running:
    window_update()
    window_render()
    
    if exit_dialog_code.value is not None:
        if exit_dialog_code.value == DialogStatus.YES:
            quit_app(None)
        exit_dialog_code.value = None

    if not app_state.running:
        app_state.running = True

        messagebox_show(300, 120, "Do you really want to exit?", "", button_flags=DialogFlags.YES_NO_COMBO, out=exit_dialog_code)
```

### Creating Menu Bar
- `MenuBar` takes a list of [Menu Items](#Menu-Item) as an argument
```python
rg.add_widget(rg.MenuBar([]))
```

### Menu Item
- `params` :
  ```python
  text: str
  letter_index: int | None = None
  dropdown: DropDown | None = None
  color: tuple = Colors.TEXT
  shortcut: str | None = None
  shortcut_fn = lambda _: 0
  onclick = None
  z_index: int = 0
  ```
> [!NOTE]
> The `z_index` does not affect the MenuItem if it is a child of a Widget (eg. [Menu Bar](#Creating-Menu-Bar) or [DropDown](#DropDown)

> [!NOTE]
> The `shortcut_fn` gets called on every update, it is upto you to check whether the shortcut have been pressed

- **Examples**
    - Most basic menu item, only has a name, does nothing
  ```python
    rg.MenuItem("File")
  ```
    - Menu item with letter_index, onclick function gets called by pressing `Alt + rg.MenuItem.text[letter_index]`
  ```python
    rg.MenuItem("File", 0)
  ```
    - Basic menu item with onclick function
  ```python
    rg.MenuItem("File", onclick = handle_click)
  ```
    - Menu item with shortcut label
  ```python
    rg.MenuItem("File", shortcut = "Alt+F4")
  ```
    - Advanced menu item that works as a dropdown button, [DropDown params](#DropDown) takes a list of MenuItems as a param
  ```python
    rg.MenuItem("File", dropdown = rg.DropDown([]))
  ```

### DropDown
- `params` :
  ```python
  items: list[MenuItem]
  width: int = 150
  ```
- DropDown takes a list of [MenuItems](#Menu-Item) as a param


### Scrollbar
> [!WARNING]
> Scrollbar is not meant to be used as a standalone widget, doing so will result in a crash of application
> The intended use for it is inside a [Container](#Container) widget

### Container
- `params` :
  ```python
    x: int
    y: int
    w: int
    h: int
    content_surf: pygame.Surface
    onclick: fn | None = None
    onpress: fn | None = None
    anchors: list[int] = [0, 0]
    z_index = -100
  ```
> [!NOTE]
> As of yet Container does not support auto-resizing

- `Container` is a replacement for as of now removed [Screen](#Screen)
- `onclick` and `onpress` both take a function as a value. The function gets called with 2 arguments: `self`, `position_of_click`
- `content_surf` is a `pygame.Surface` you create and manage yourself
- Scrollbars are activated automatically based on necessity
- `LSHIFT + SCROLL` is horizontal scroll

### RetroButton
- Also `Button`
- `params` :
  ```python
    x: int
    y: int
    w: int = 32
    h: int = 32
    colors: list[tuple] = [(0, 0, 0)] * 2
    onclick = None
    onpressed = None
    anchors: list[int] = [0, 0]
    z_index: int = 0
    name: str | None = None
    image_path: str | None = None
  ```
- `onclick` gets triggered on release whereas `onpressed` triggers on press
- `name` a string used to match a *.png from `ui_icons` folder
> [!NOTE]
> ~~will get updated to support custom icons~~ and text
> Should now support custom icons
- `anchors` specify whether the button is anchored to the from right or from left
    - examples:
        - `anchors = [0, 0]` and x = 0, y = 0, button will be in the top **left** corner
        - `anchors = [1, 0]` and x = 0, y = 0, button will be in the top **right** corner

### Widgets
- Widgets are the core of a PyRetro-Gui app
- `rg.app_state.widgets` is an internal list of all the existing ui elements
> [!NOTE]
> This list is internal and should NOT be used if possible, as using it directly is not the intended usage.
> ~~It is used in some parts of docs for now, since PyRetro-Gui is in very early stages of development.~~
> `add_widget()` function has been added. Check [Adding widgets](#Adding-Widgets)

### Adding Widgets
- You can add any pyretro-gui widget by doing
```python
rg.add_widget(widget_instance)
```
- `add_widget` returns added widget

### Screen
- ~~Returned by [rg.create_window](#Creating-a-window)~~
- ~~It is a pygame surface that gets drawn at a certain position each render, can be used to render custom ui or other things~~
> [!WARNING]
> ~~This part of the framework is untested and will most likely be replaced by a widget in future.~~
> `screen` was replaced by [Container](#Container) widget.


### Dialog
- Also called `MessageBox`
#### Usage
- can be called directly from terminal
```bash
# <width> <height> <title> <icon> <flags> [<Button title> <Return status>]*
python3 _dialog_window.py 200 100 "Predefined YES/NO messagebox" "" 1
python3 _dialog_window.py 300 100 "Custom messagebox" "" 4 Hello 1 World 2 "Miku Hatsune" 3
```
- or using code, the interface is:
```python
def open_dialog(w: int, h: int, title: str, icon: str, button_flags: int = 0, halting = False, out: ReferenceValue | None = None, buttons = []):
    ...
```
- `button_flags` is an `int` of flags from `DialogFlags`
- `buttons` is a list of tuples such as `(name: str, return_code: int)` eg. `("Accept", 1)`.
- `out` is a `ReferenceValue`, which in parameter `value` contains an int of type `DialogStatus` or if `DialogFlags.CUSTOM` is specified then the int is either `DialogStatus.ERROR` or a custom `return_code` specified in `buttons`
    - The intention of `out` is to provide a way to determine which button the user pressed.
- alternatively, you can also call `messagebox_show` which is an alias for `open_dialog`
