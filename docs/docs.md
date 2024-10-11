# PyRetro-Gui Docs

## Table of contents
1. [Importing](#Importing)
2. [Creating a window](#Creating-a-window)
3. [Setting UI refresh rate](#Setting-UI-refresh-rate)
4. [Main app loop](#Main-app-loop)
5. [Creating Menu Bar](#Creating-Menu-Bar)
6. [Menu Item](#Menu-Item)
7. [DropDown](#DropDown)
8. [Scrollbar](#Scrollbar)
9. [Container](#Container)
10. [Buttons](#RetroButton)
11. [About widgets](#Widgets)
12. [Adding widgets](#Adding-Widgets)
13. [Screen](#Screen)


### Importing
```python
import pyretro_gui as rg
```

### Creating a window
```python
rg.create_window(640, 480, "Test App title", "test_icon.png")
```
- to make a resizable window use `pygame.RESIZABLE`
```python
rg.create_window(640, 480, "Test App title", "test_icon.png", flags = pygame.RESIZABLE)
```
> [!NOTE]
> Resizable window is highly experimental and might cause issues such as crashes

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
    anchors: list[int] = [0, 0]
    z_index = -100
  ```
> [!NOTE]
> As of yet Container does not support auto-resizing

- `Container` is a replacement for as of now removed [Screen](#Screen)
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


