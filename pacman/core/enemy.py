from time import time
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

    @property
    def dead(self):
        return self.revive > 0

    @property
    def fear(self):
        return self.pac.power > 0

    @property
    def step(self):
        return 1
        # return 1 if self.dead or self.fear else 2

    def eat(self):
        gap = self.map.gap
        if sum(abs(i-j) for i, j in zip(self.pos, self.pac.pos)) < gap/2:
            if self.fear:
                self.revive = 100
                self.pac.fight(True)
            else:
                self.pac.fight(False)

    def get_dir_from_path(self, path):
        gap = self.map.gap
        _p = [x/gap for x in self.pos]
        p = [x/gap for x in self.pac.pos]

        # 烂代码
        # 专门为穿越追踪做的烂代码
        if _p[0] == 14 and p[0] == 14:
            if (_p[1] <= 5 and p[1] >= 21):
                return -2

            if (p[1] <= 5 and _p[1] >= 21):
                return 2

        for i, p in enumerate(path):
            if all(i == j for i, j in zip(_p, p)):
                path = path[i:]

        if len(path) < 2:
            return self.dir

        d = [j-i for i, j in zip(*path[:2])]
        if d[0] != 0:
            return d[0]
        return d[1]*2

    def chase(self):
        """可以自行重载，编写不同的追逐逻辑"""
        gap = self.map.gap
        begin = [x//gap for x in self.pos]
        end = [x//gap for x in self.pac.pos]

        self.astar.calc_chase_path(begin, end, 100)
        dir = self.get_dir_from_path(self.astar.path)
        self.set_dir(dir)

    def escape(self):
        gap = self.map.gap
        begin = [x//gap for x in self.pos]
        fear = [x//gap for x in self.pac.pos]

        self.astar.calc_escape_path(begin, fear, 10)
        dir = self.get_dir_from_path(self.astar.path)
        self.set_dir(dir)

    def gohome(self):
        gap = self.map.gap
        begin = [x//gap for x in self.pos]
        end = [15, 14]

        self.astar.calc_chase_path(begin, end, 100)
        dir = self.get_dir_from_path(self.astar.path)
        self.set_dir(dir)

        self.at_home = len(self.astar.path) == 1

    def think(self):
        # 此处有bug，如果速度与剩余格子长度互质，则可能直到撞墙触发mover.close_to_wall之后才能改变策略
        # 但若不加此限制，则思考频率过快，大量冗余思考影响游戏运行速度，帧率下降到不可忍受
        # 一种解决方法是，令其运动速度始终与格子不互质
        print("fuck", time())

        # 三种移动策略
        if self.dead:
            self.gohome()
        elif self.fear:
            self.escape()
        else:
            self.chase()

    def update(self):
        if self.on_cross():
            self.think()

        # 复活计数器
        if self.dead and self.at_home:
            if self.revive:
                self.revive -= 1

        self.update_dir()
        self.update_pos()
        if not self.dead:
            self.eat()
