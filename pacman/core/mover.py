from math import ceil, floor
from pacman.core.map import Map


class Mover:
    def __init__(self, map: Map) -> None:
        self.dir = 1
        self.next_dir = 0
        self.map = map

        gap = self.map.gap
        self.pos = [gap, gap]

    @property
    def step(self):
        return 2

    def set_dir(self, dir: int):
        # self.next_dir = dir
        self.next_dir = dir

    def set_pos(self, i: int, j: int):
        gap = self.map.gap
        self.pos = [i*gap, j*gap]

    def get_next_pos(self, dir):
        next_pos = [x for x in self.pos]
        if dir == 1:
            next_pos[0] += self.step
        elif dir == -1:
            next_pos[0] -= self.step
        elif dir == 2:
            next_pos[1] += self.step
        elif dir == -2:
            next_pos[1] -= self.step

        gap = self.map.gap
        h = (self.map.row-1)*gap
        w = (self.map.col-1)*gap

        def limit(x, x_max):
            if x < 0:
                x += x_max
            elif x >= x_max:
                x -= x_max
            return x

        next_pos[0] = limit(next_pos[0], h)
        next_pos[1] = limit(next_pos[1], w)
        return next_pos

    def check_pos(self, pos):
        """查看pos是否合法（跑到墙里、超出边界、脱轨"""
        gap = self.map.gap

        i, j = [x / gap for x in pos]

        # 脱轨
        if all(x % gap != 0 for x in pos):
            return False

        if self.map.is_wall(floor(i), floor(j)) or self.map.is_wall(ceil(i), ceil(j)):
            return False
        return True

    def on_cross(self):
        gap = self.map.gap
        return all(x % gap == 0 for x in self.pos)

    def update_dir(self):
        if self.dir == 0 or self.dir == -self.next_dir:
            self.dir = self.next_dir
            return

        # 由于这里的设计，吃豆人地图必须设计为单宽度的路径
        if self.on_cross():
            pos = self.get_next_pos(self.next_dir)
            if self.check_pos(pos):
                self.dir = self.next_dir
                return

    def close_to_wall(self, pos):
        """如果维持原速前进会越界，则尽可能在接近墙的位置停下"""
        gap = self.map.gap

        i, j = [x / gap for x in pos]
        if self.map.is_wall(floor(i), floor(j)):
            if self.dir < 0:
                pos = [ceil(i)*gap, ceil(j)*gap]

        if self.map.is_wall(ceil(i), ceil(j)):
            if self.dir > 0:
                pos = [floor(i)*gap, floor(j)*gap]

        return pos

    def update_pos(self):
        pos = self.get_next_pos(self.dir)
        self.pos = pos if self.check_pos(pos) else self.close_to_wall(pos)

    def get_coord(self):
        # 将自身的位置转换为坐标
        return self.map.pos2coord(self.pos)

    def update(self): ...
