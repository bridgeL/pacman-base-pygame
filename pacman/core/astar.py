from pacman.core.map import Map
from typing import List


class Node:
    def __init__(self, p, g, h, father: "Node" = None) -> None:
        '''
        p pos
        g step
        h distance
        '''
        self.p = p
        self.g = g
        self.h = h
        self.father = father

    @property
    def f(self):
        return self.g + self.h

    @property
    def ef(self):
        return self.g  - self.h * 2

    def __str__(self) -> str:
        return f"{self.p} {self.ef}, "


class AStar:
    def __init__(self, map: Map):
        self.map = map
        self.path = []

    def get_dist(self, p1, p2):
        return sum(abs(i-j) for i, j in zip(p1, p2))

    def get_near_ps(self, node: Node):
        ds = []
        for i in range(3):
            for j in range(3):
                if (i == 1) ^ (j == 1):
                    d = (i-1, j-1)
                    ds.append(d)

        return [[i+j for i, j in zip(node.p, d)] for d in ds]

    def find(self, begin, end):
        node = Node(begin, 0, self.get_dist(begin, end))

        open_list: List[Node] = [node]
        close_list: List[Node] = []

        while len(open_list):
            open_list.sort(key=lambda x: x.f)
            node = open_list.pop(0)

            close_list.append(node)
            if all(i == j for i, j in zip(node.p, end)):
                break

            ps = self.get_near_ps(node)

            def check_list(p):
                for n in open_list:
                    if all(i == j for i, j in zip(n.p, p)):
                        return False
                for n in close_list:
                    if all(i == j for i, j in zip(n.p, p)):
                        return False
                return True

            ps = [p for p in ps if check_list(p)]

            def check_map(p):
                m = len(self.map._map)
                n = len(self.map._map[0])

                if all(i in range(j) for i, j in zip(p, [m, n])):
                    return not self.map.is_wall(*p)
                else:
                    return False

            ps = [p for p in ps if check_map(p)]
            ns = [Node(p, node.g+1, self.get_dist(p, end), node) for p in ps]
            open_list.extend(ns)

        node = close_list[-1]
        path = [node.p]
        while node.father:
            node = node.father
            path.append(node.p)
            if all(i == j for i, j in zip(node.p, begin)):
                break

        path.reverse()
        self.path = path


class EscapeAStar(AStar):
    def find(self, begin, fear, step):
        node = Node(begin, 0, self.get_dist(begin, fear))

        open_list: List[Node] = [node]
        close_list: List[Node] = []
        while len(open_list):
            open_list.sort(key=lambda x: x.ef)
            node = open_list.pop(0)

            close_list.append(node)

            if node.g > step:
                break

            ps = self.get_near_ps(node)

            def check_list(p):
                for n in open_list:
                    if all(i == j for i, j in zip(n.p, p)):
                        return False
                for n in close_list:
                    if all(i == j for i, j in zip(n.p, p)):
                        return False
                return True

            ps = [p for p in ps if check_list(p)]

            def check_map(p):
                m = len(self.map._map)
                n = len(self.map._map[0])

                if all(i in range(j) for i, j in zip(p, [m, n])):
                    return not self.map.is_wall(*p)
                else:
                    return False

            ps = [p for p in ps if check_map(p)]
            ns = [Node(p, node.g+1, self.get_dist(p, fear), node) for p in ps]
            open_list.extend(ns)

        close_list.sort(key=lambda x:x.ef)
        node = close_list[0]
        path = [node.p]
        while node.father:
            node = node.father
            path.append(node.p)
            if all(i == j for i, j in zip(node.p, begin)):
                break
        path.reverse()
        self.path = path

