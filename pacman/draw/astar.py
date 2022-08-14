import pygame
from pacman.core.astar import Astar
from pacman.draw.drawer import BaseDrawer


class AStarDrawer(BaseDrawer):
    def __init__(self, astar: Astar, gap: int, screen: pygame.Surface) -> None:
        self.astar = astar
        self.screen = screen
        self.gap = gap

    def draw_color(self, color, path, base):
        # 生成轨迹线
        gap = self.gap
        n = len(path)

        lines = []
        for i in range(1, n):
            line = [path[i-1], path[i]]
            lines.append(line)

        for line in lines:
            line = [[i*gap + base for i in p] for p in line]
            p1, p2 = line
            p1.reverse()
            p2.reverse()
            pygame.draw.line(self.screen, color, p1, p2, 3)

    def draw(self):
        path = [n.pos for n in self.astar.close_list]
        self.draw_color((200, 0, 200), path, self.gap/2+3)
        self.draw_color((0, 200, 0), self.astar.path, self.gap/2-3)

    def clear(self):
        path = [n.pos for n in self.astar.close_list]
        self.draw_color((0, 0, 0), path, self.gap/2+3)
        self.draw_color((0, 0, 0), self.astar.path, self.gap/2-3)
