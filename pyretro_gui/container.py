
import pygame
from .app_core import app_state
from .constants import Colors

from .scrollbar import ScrollBar

class Container():
    def __init__ (self, x: int, y: int, w: int, h: int, content_surf: pygame.Surface, onclick = None, onpressed = None, anchors: list[int] = [0, 0], z_index = -100):

        self.x, self.y = x, y
        self.w, self.h = w, h
        self._surface = pygame.Surface((w, h))

        self.content_surf = content_surf
        self.content_size = list(content_surf.get_size())
        
        self.onclick = onclick
        self.onpressed = onpressed
        self.anchors = anchors
        self.z_index = z_index

        self.pressed = False
        self.__prev_pressed = self.pressed
        
        self.mpos_inside = None
        self._prev_pos_inside = None

        self.is_scroll_x = self.content_size[0] > w
        self.is_scroll_y = self.content_size[1] > h

        self.scrollbars = []

        if self.is_scroll_x:
            self.scrollbars.append(ScrollBar(0, 0, w - 16, self.content_size[0], horizontal = True, anchors = [0, 1]))
            self.content_size[0] += ScrollBar.SCRLBAR_WIDTH

        if self.is_scroll_y:
            self.scrollbars.append(ScrollBar(0, 0, h, self.content_size[1], anchors = [1, 0]))
            self.content_size[1] += ScrollBar.SCRLBAR_WIDTH

    def get_surface (self):
        return self._surface

    def get_rect (self, win_size):
        r = [self.x, self.y, self.w, self.h]
        if self.anchors[0]: r[0] = win_size[0] - r[0] - r[2]
        if self.anchors[1]: r[1] = win_size[1] - r[1] - r[3]

        return pygame.Rect(r)

    def get_content_dif (self):
        return [abs(self.content_size[0] - self.w), abs(self.content_size[1] - self.h)]

    def get_x_scrollbar (self):
        for s in self.scrollbars:
            if s.horizontal: return s
        return None

    def get_y_scrollbar (self):
        for s in self.scrollbars:
            if not s.horizontal: return s
        return None

    def update (self, mouse_pos, mouse_btns, win_size):

        for event in app_state.events:
            if event.type == pygame.MOUSEWHEEL:
                s = self.get_x_scrollbar() if pygame.key.get_pressed()[pygame.K_LSHIFT] else self.get_y_scrollbar()
                if s is not None:
                    if event.y < 0:
                        s.down(None)
                    elif event.y > 0:
                        s.up(None)

                sx = self.get_x_scrollbar()
                if sx is not None:
                    if event.x < 0:
                        sx.up(None)
                    elif event.x > 0:
                        sx.down(None)

        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0] and not app_state.resizing

        self._prev_pos_inside = self.mpos_inside if self.mpos_inside is not None else (mouse_pos[0] - r.x, mouse_pos[1] - r.y)
        self.mpos_inside = (mouse_pos[0] - r.x, mouse_pos[1] - r.y)

        # pressed
        if self.pressed and self.onpressed:
            if not self.__prev_pressed:
                self.origin_press = mouse_pos

            self.onpressed(self, self.mpos_inside)

        # clicked
        if not self.pressed and self.__prev_pressed and self.focused:
            if self.onclick:
                self.onclick(self, self.mpos_inside)

        for s in self.scrollbars:
            s.update(mouse_pos, mouse_btns, self.get_rect(win_size).topleft, self._surface.get_rect())


    def render (self, win, _):

        self._surface.fill((0, 0, 0))

        dif = self.get_content_dif()
        xp = 0 if not self.is_scroll_x else - dif[0] * self.get_x_scrollbar().progress
        yp = 0 if not self.is_scroll_x else - dif[1] * self.get_y_scrollbar().progress
        self._surface.blit(self.content_surf, (xp, yp))

        for s in self.scrollbars:
            s.render(self._surface, _, self._surface.get_rect())


        pygame.draw.rect(self._surface, Colors.TEXT, self._surface.get_rect(), 1)
        win.blit(self._surface, self.get_rect(win.get_size()).topleft)

