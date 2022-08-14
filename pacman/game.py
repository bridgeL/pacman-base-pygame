from typing import List
from pygame.constants import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.event import Event
from pygame.surface import Surface

from pacman.core.map import Map
from pacman.core.pac import Pac
from pacman.core.enemy import Enemy
from pacman.core.mover import Mover

from pacman.draw.map import MapDrawer
from pacman.draw.pac import PacDrawer
from pacman.draw.astar import AStarDrawer
from pacman.draw.enemy import EnemyDrawer
from pacman.draw.score import ScoreDrawer
from pacman.draw.drawer import BaseDrawer


class Game:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.map: Map
        self.pac: Pac
        self.drawers: List[BaseDrawer] = []
        self.movers: List[Mover] = []
        self.init()

    def init(self):
        # 初始化地图
        map = Map()
        map_drawer = MapDrawer(map, self.screen)

        # 初始化角色
        pac = Pac(map)
        pac.set_pos(2, 26)
        # pac.set_pos(23, 13)
        pac_drawer = PacDrawer(pac, map.gap, self.screen)

        # 初始化敌人
        enemy = Enemy(map, pac)
        enemy.set_pos(8, 21)
        # enemy.set_pos(15, 14)
        enemy_drawer = EnemyDrawer(pac, enemy, map.gap // 2, self.screen)

        # 初始化astar绘制器
        astar_drawer = AStarDrawer(enemy.astar, map.gap, self.screen)

        # 初始化分数绘制器
        score_drawer = ScoreDrawer(pac, map.gap, self.screen)

        self.map = map
        self.pac = pac
        self.movers = [pac, enemy]
        self.drawers = [map_drawer, pac_drawer, enemy_drawer, astar_drawer, score_drawer]

    def update(self):
        for drawer in self.drawers:
            drawer.clear()

        for mover in self.movers:
            mover.update()

        for drawer in self.drawers:
            drawer.draw()

    def restart(self):
        for drawer in self.drawers:
            drawer.clear()
        self.init()

    def handle_events(self, events: List[Event]):
        for event in events:
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN:
                self.handle_keydown(**event.dict)
            elif event.type == MOUSEBUTTONDOWN:
                self.handle_mousedown(**event.dict)

    def handle_mousedown(self, button: int, pos: tuple, **data):
        if button == 1:
            gap = self.map.gap
            coord = [(x - gap/2) / gap for x in reversed(pos)]
            print(coord)

    def handle_keydown(self, unicode: str, scancode: int, **data):
        unicode = unicode.lower()
        scancode = scancode

        if unicode == 'r':
            self.restart()

        dir_dict = {
            "w": -1,
            "s": 1,
            "a": -2,
            "d": 2,
            "i": -1,
            "k": 1,
            "j": -2,
            "l": 2,
            82: -1,
            81: 1,
            80: -2,
            79: 2
        }

        if unicode in dir_dict:
            self.pac.set_dir(dir_dict[unicode])

        if scancode in dir_dict:
            self.pac.set_dir(dir_dict[scancode])
