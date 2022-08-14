from pacman.core.map import Map


class Mover:
    def __init__(self, map: Map) -> None:
        self.dir = 0
        self.next_dir = 0
        self.map = map
        self.pos = self.map.coord2pos((1, 1))
        self.step = 2

    def set_dir(self, dir: int):
        self.next_dir = dir

    def set_coord(self, i: float, j: float):
        self.pos = self.map.coord2pos((i, j))

    def get_next_pos(self, dir, step):
        next_pos = [x for x in self.pos]
        # step = self.step
        if dir == 1:
            next_pos[0] += step
        elif dir == -1:
            next_pos[0] -= step
        elif dir == 2:
            next_pos[1] += step
        elif dir == -2:
            next_pos[1] -= step

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

    def get_next_coord(self, dir):
        coord = self.map.pos2coord(self.pos)
        if self.on_cross():
            if dir == 1:
                coord[0] += 1
            elif dir == -1:
                coord[0] -= 1
            elif dir == 2:
                coord[1] += 1
            elif dir == -2:
                coord[1] -= 1
        else:
            if dir == 1:
                coord[0] += 1
            elif dir == 2:
                coord[1] += 1

        row = self.map.row
        col = self.map.col

        def limit(x, x_max):
            if x < 0:
                x += x_max
            elif x >= x_max:
                x -= x_max
            return x

        coord[0] = limit(coord[0], row)
        coord[1] = limit(coord[1], col)

        return coord

    def on_cross(self):
        gap = self.map.gap
        return all(x % gap == 0 for x in self.pos)

    def move(self):
        # 赋初值 或 掉头
        if self.dir == 0 or self.dir == -self.next_dir:
            self.dir = self.next_dir

        if not self.dir:
            return

        left = self.step

        # 先移动到路口
        if not self.on_cross():
            # 下一个路口
            coord = self.get_next_coord(self.dir)
            gap = self.map.gap
            pos = [i*gap for i in coord]
            dist = sum(abs(x-y) for x,y in zip(pos, self.pos))
            step = min(dist, self.step)
            left -= step
            self.pos = self.get_next_pos(self.dir, step)
            if not left:
                return

        # 尝试转弯
        if self.dir != self.next_dir:
            coord = self.get_next_coord(self.next_dir)
            if not self.map.is_wall(*coord):
                self.dir = self.next_dir

        coord = self.get_next_coord(self.dir)
        if not self.map.is_wall(*coord):
            self.pos = self.get_next_pos(self.dir, left)

    def update(self): ...
