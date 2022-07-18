import pygame
from pacman.core.pac import Pac


class PacDrawer:
    def __init__(self, pac: Pac, gap: int, screen: pygame.Surface) -> None:
        self.pac = pac
        self.screen = screen
        self.gap = gap

    def draw(self, color):
        gap = self.gap
        pos = [x + gap/2 for x in self.pac.pos]
        pos.reverse()
        pygame.draw.circle(self.screen, color, pos, 7, 7)

    def draw_pac(self):
        if self.pac.dead:
            color = (255, 255, 255)
        elif self.pac.is_power:
            if self.pac.power >= 50:
                color = (255, 0, 0)
            # 快结束时，闪烁提示
            elif int(self.pac.power / 10) % 2:
                color = (255, 0, 0)
            else:
                color = (255, 255, 0)
        else:
            color = (255, 255, 0)
        self.draw(color)

    def clear_pac(self):
        self.draw((0, 0, 0))
