from pacman.core.map import Map
from typing import List


class Node:
    def __init__(self, step: int, dist: int, pos: tuple, father: "Node") -> None:
        self.step = step
        self.dist = dist
        self.pos = pos
        self.father = father


class Astar:
    def __init__(self, map: Map) -> None:
        self.map = map
        self.path = []
        self.close_list: List[Node] = []

    def calc_dist(self, p1: tuple, p2: tuple):
        return sum(abs(i-j) for i, j in zip(p1, p2))

    def get_next_pos(self, p: tuple):
        ds = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        return iter([i+j for i, j in zip(p, d)] for d in ds)

    def pos_is_equal(self, p1: tuple, p2: tuple):
        return all(i == j for i, j in zip(p1, p2))

    def calc_path(self, begin: tuple, refer: tuple, chase: bool):
        dist = self.calc_dist(begin, refer)
        node = Node(0, dist, begin, None)
        open_list: List[Node] = [node]
        close_list: List[Node] = []
        pos_list: List[tuple] = [node.pos]

        while open_list:
            if chase:
                open_list.sort(key=lambda n: n.step + n.dist, reverse=True)
            else:
                open_list.sort(key=lambda n: n.step - n.dist, reverse=True)

            node = open_list.pop()
            close_list.append(node)

            if chase:
                if self.pos_is_equal(node.pos, refer):
                    break
            else:
                if node.step >= 10:
                    close_list.sort(key=lambda n: n.dist)
                    break

            for p in self.get_next_pos(node.pos):
                for pp in pos_list:
                    if self.pos_is_equal(pp, p):
                        break
                else:
                    r = self.map.is_wall(*p)
                    pos_list.append(p)
                    # 排除越界 和 墙
                    if r is False:
                        dist = self.calc_dist(p, refer)
                        next_node = Node(node.step+1, dist, p, node)
                        open_list.append(next_node)

        node = close_list[-1]
        path = [node.pos]
        while node.father:
            node = node.father
            path.append(node.pos)
            if self.pos_is_equal(node.pos, begin):
                break

        path.reverse()
        self.path = path
        self.close_list = close_list

    def calc_chase_path(self, begin: tuple, end: tuple):
        self.calc_path(begin, end, True)

    def calc_escape_path(self, begin: tuple, fear: tuple):
        self.calc_path(begin, fear, False)
