import pygame
from pacman.core.astar import AStar


class AStarDrawer:
    def __init__(self, astar: AStar, gap: int, screen: pygame.Surface) -> None:
        self.astar = astar
        self.screen = screen
        self.gap = gap

    def draw(self, color):
        # 生成轨迹线
        gap = self.gap
        path = self.astar.path
        n = len(path)

        lines = []
        for i in range(1, n):
            line = [path[i-1], path[i]]
            lines.append(line)

        for line in lines:
            line = [[i*gap + gap/2 for i in p] for p in line]
            p1, p2 = line
            p1.reverse()
            p2.reverse()
            pygame.draw.line(self.screen, color, p1, p2, 5)

    def draw_path(self):
        self.draw((0, 255, 0))

    def clear_path(self):
        self.draw((0, 0, 0))
