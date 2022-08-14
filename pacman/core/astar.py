from pacman.core.map import Map
from typing import Callable, List


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

    def calc_dist(self, p1: tuple, p2: tuple):
        return sum(abs(i-j) for i, j in zip(p1, p2))

    def get_next_pos(self, p: tuple):
        ds = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        return iter([i+j for i, j in zip(p, d)] for d in ds)

    def pos_is_equal(self, p1: tuple, p2: tuple):
        return all(i == j for i, j in zip(p1, p2))

    def calc_path(self, begin: tuple, dist_refer: tuple, calc_cost: Callable[[Node], int], stop_check: Callable[..., bool]):
        dist = self.calc_dist(begin, dist_refer)
        node = Node(0, dist, begin, None)
        open_list: List[Node] = [node]
        close_list: List[Node] = []
        pos_list: List[tuple] = [node.pos]

        while open_list:
            open_list.sort(key=calc_cost, reverse=True)
            node = open_list.pop()
            close_list.append(node)

            if stop_check(node=node, open_list=open_list):
                break

            for p in self.get_next_pos(node.pos):
                for pp in pos_list:
                    if self.pos_is_equal(pp, p):
                        break
                else:
                    r = self.map.is_wall(*p)
                    # 排除越界
                    if r is not None:
                        pos_list.append(p)

                        # 排除墙
                        if not r:
                            dist = self.calc_dist(p, dist_refer)
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

    def calc_chase_path(self, begin: tuple, end: tuple, max_step: int):
        def calc_cost(node: Node):
            return node.step + node.dist

        def stop_check(node: Node, **data):
            return self.pos_is_equal(node.pos, end) or node.step >= max_step

        self.calc_path(begin, end, calc_cost, stop_check)

    def calc_escape_path(self, begin: tuple, fear: tuple, max_step: int):
        def calc_cost(node: Node):
            return node.step - node.dist

        def stop_check(node: Node, **data):
            return node.step >= max_step

        # def stop_check(open_list: List[Node], **data):
        #     steps = [node.step for node in open_list]
        #     print(steps)
        #     return steps and min(steps) >= max_step

        self.calc_path(begin, fear, calc_cost, stop_check)
