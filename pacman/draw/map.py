import pygame
from pacman.core.map import Map


class MapDrawer:
    def __init__(self, map: Map, screen: pygame.Surface) -> None:
        self.map = map
        self.screen = screen

    def draw_wall(self):
        m = len(self.map._map)
        n = len(self.map._map[0])
        gap = self.map.gap

        # 生成墙体线
        lines = []
        for i in range(m):
            for j in range(n):
                # 横线
                if j > 0 and self.map.is_wall(i, j-1) and self.map.is_wall(i, j):
                    # 清除冗余边界线
                    if i > 0 and i < m-1 and \
                            self.map.is_wall(i-1, j-1) and \
                            self.map.is_wall(i-1, j) and \
                            self.map.is_wall(i+1, j-1) and \
                            self.map.is_wall(i+1, j):
                        pass
                    else:
                        line = [(i, j-1), (i, j)]
                        lines.append(line)
                # 竖线
                if i > 0 and self.map.is_wall(i-1, j) and self.map.is_wall(i, j):
                    # 清除冗余边界线
                    if j > 0 and j < n-1 and \
                            self.map.is_wall(i-1, j-1) and \
                            self.map.is_wall(i, j-1) and \
                            self.map.is_wall(i-1, j+1) and \
                            self.map.is_wall(i, j+1):
                        pass
                    else:
                        line = [(i-1, j), (i, j)]
                        lines.append(line)

        # 画墙
        for line in lines:
            line = [[i*gap + gap/2 for i in p] for p in line]
            p1, p2 = line
            p1.reverse()
            p2.reverse()
            pygame.draw.line(self.screen, (0, 0, 255), p1, p2, 5)

    def draw_bean(self):
        m = len(self.map._map)
        n = len(self.map._map[0])
        gap = self.map.gap

        ps = []
        for i in range(m):
            for j in range(n):
                if self.map.is_bean(i, j):
                    p = (i, j)
                    ps.append(p)

        for p in ps:
            p = [i*gap + gap/2 for i in p]
            p.reverse()
            pygame.draw.circle(self.screen, (255, 255, 255), p, 2, 2)

    def draw_power(self):
        m = len(self.map._map)
        n = len(self.map._map[0])
        gap = self.map.gap

        ps = []
        for i in range(m):
            for j in range(n):
                if self.map.is_power(i, j):
                    p = (i, j)
                    ps.append(p)

        for p in ps:
            p = [i*gap + gap/2 for i in p]
            p.reverse()
            pygame.draw.circle(self.screen, (255, 0, 0), p, 7, 7)
