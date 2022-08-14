from pacman.core.map import Map
from pacman.core.mover import Mover
from pacman.core.pac import Pac
from pacman.core.astar import Astar


class Enemy(Mover):
    def __init__(self, map: Map, pac: Pac) -> None:
        super().__init__(map)
        self.pac = pac

        # 初始化轨迹
        self.astar = Astar(map)

        # 在家中
        self.at_home = False

        # 复活计数器
        self.revive = 0

        # 思考计数器
        self.think = 0

    @property
    def dead(self):
        return self.revive > 0

    @property
    def fear(self):
        return self.pac.power > 0

    def eat(self):
        gap = self.map.gap
        if sum(abs(i-j) for i, j in zip(self.pos, self.pac.pos)) < gap/2:
            if self.fear:
                self.revive = 100
                self.pac.fight(True)
            else:
                self.pac.fight(False)


    def get_dir(self, coord:tuple):
        # 烂代码
        # 专门为穿越追踪做的烂代码
        _p = self.map.pos2coord(self.pos)
        p = self.map.pos2coord(self.pac.pos)

        if _p[0] == 14 and p[0] == 14:
            if (_p[1] <= 5 and p[1] >= 21):
                return -2

            if (p[1] <= 5 and _p[1] >= 21):
                return 2

        # 根据上次思考的路径行动
        path = self.astar.path
        for i, p in enumerate(path):
            if p[0] == coord[0] and p[1] == coord[1]:
                path = path[i:]
                break
        path = path[:2]
        if len(path) < 2:
            path = [path[0], path[0]]
        d = [j-i for i, j in zip(*path)]
        if d[0] != 0:
            return d[0]
        return d[1]*2


    def chase(self):
        """可以自行重载，编写不同的追逐逻辑"""
        begin = self.map.pos2coord(self.pos)
        end = self.map.pos2coord(self.pac.pos)
        self.astar.calc_chase_path(begin, end)


    def escape(self):
        begin = self.map.pos2coord(self.pos)
        fear = self.map.pos2coord(self.pac.pos)
        self.astar.calc_escape_path(begin, fear)

    def gohome(self):
        begin = self.map.pos2coord(self.pos)
        end = [15, 14]
        self.astar.calc_chase_path(begin, end)
        self.at_home = len(self.astar.path) == 1

    def update(self):
        if self.think:
            self.think -= 1
        else:
            self.think = 20
            # 三种移动策略
            if self.dead:
                self.gohome()
            elif self.fear:
                self.escape()
            else:
                self.chase()

        coord = self.map.pos2coord(self.pos)
        dir = self.get_dir(coord)
        self.set_dir(dir)

        # 复活计数器
        if self.dead and self.at_home:
            if self.revive:
                self.revive -= 1

        self.move()

        if not self.dead:
            self.eat()
