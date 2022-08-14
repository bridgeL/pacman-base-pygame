import pygame
from pacman.core.pac import Pac
from pacman.draw.drawer import BaseDrawer


class PacDrawer(BaseDrawer):
    def __init__(self, pac: Pac, gap: int, screen: pygame.Surface) -> None:
        self.pac = pac
        self.screen = screen
        self.gap = gap
        self.color = (255, 255, 0)
        self.dead_color = (255, 255, 255)
        self.power_color = (255, 0, 0)

    def draw_color(self, color):
        gap = self.gap
        pos = [x + gap/2 for x in self.pac.pos]
        pos.reverse()
        pygame.draw.circle(self.screen, color, pos, 7, 7)

    def get_color(self):
        # 死了
        if self.pac.dead:
            return self.dead_color

        # 牛了
        if self.pac.is_power:
            # 快结束时，闪烁提示
            if self.pac.power >= 50 or (self.pac.power // 10) % 2:
                return self.power_color

        # 正常了
        return self.color

    def draw(self):
        color = self.get_color()
        self.draw_color(color)

    def clear(self):
        self.draw_color((0, 0, 0))
