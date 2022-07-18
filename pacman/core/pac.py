from math import ceil, floor
from pacman.core.map import Map
from pacman.core.mover import Mover


class Pac(Mover):
    def __init__(self, map: Map) -> None:
        super().__init__(map)
        self.score = 0
        self.power = 0
        self.dead = False

    @property
    def is_power(self):
        return self.power > 0

    @property
    def step(self):
        return 4 if self.is_power else 2

    def eat(self, check):
        gap = self.map.gap
        i, j = [x / gap for x in self.pos]

        flag = False
        if check(floor(i), floor(j)):
            if any(x % gap < 2 for x in self.pos):
                self.map.clear(floor(i), floor(j))
                flag = True

        if check(ceil(i), ceil(j)):
            if any(x % gap >= gap - 2 for x in self.pos):
                self.map.clear(ceil(i), ceil(j))
                flag = True

        return flag

    def update(self):
        if self.dead:
            return

        self.update_move()

        if self.eat(self.map.is_bean):
            self.score += 1

        if self.eat(self.map.is_power):
            self.score += 15
            self.power = 500

        if self.power:
            self.power -= 1

    def fight(self, win: bool):
        """由外部对象调用"""
        if win:
            self.score += 100
        else:
            self.dead = True
