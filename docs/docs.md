# PyRetro-Gui Docs

## Table of contents
1. [Importing](#Importing)
2. [Creating a window](#Creating-a-window)
3. [Setting UI refresh rate](#Setting-UI-refresh-rate)
4. [Main app loop](#Main-app-loop)
5. [Creating Menu Bar](#Creating-Menu-Bar)
6. [Menu Item](#Menu-Item)
7. [About widgets](#Widgets)
8. [Screen](#Screen)


### Importing
```python
import retro_gui as rg
```

### Creating a window
```python
screen = rg.create_window(640, 480, "Test App title", "test_icon.png")
```

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
rg.app_state.widgets.append(rg.MenuBar([]))
```

### Menu Item



### Widgets
- Widgets are the core of a PyRetro-Gui app
- `rg.app_state.widgets` is a list of all the existing ui elements
> [!NOTE]
> This list is internal and should not be used if possible, as using it directly is not the intended usage.
> It is used in some parts of docs for now, since PyRetro-Gui is in very early stages of development.

### Screen
- It is a pygame surface that gets drawn at a certain position each render, can be used to render custom ui or other things
> [!WARNING]
> This part of the framework is untested and might be replaced by a widget in future.


