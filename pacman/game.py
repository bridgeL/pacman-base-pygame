import pygame
from pacman.core.map import Map
from pacman.core.pac import Pac
from pacman.core.enemy import Enemy

from pacman.draw.map import MapDrawer
from pacman.draw.pac import PacDrawer
from pacman.draw.enemy import EnemyDrawer
from pacman.draw.score import ScoreDrawer


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.init()

    def init(self):
        # 初始化地图
        self.map = Map()
        self.mapdrawer = MapDrawer(self.map, self.screen)

        # 初始化角色
        self.pac = Pac(self.map)
        self.pac.set_pos(23, 13)
        self.pacdrawer = PacDrawer(self.pac, self.map.gap, self.screen)

        # 初始化敌人
        self.enemy = Enemy(self.map, self.pac)
        self.enemy.set_pos(15, 14)
        self.enemydrawer = EnemyDrawer(
            self.pac, self.enemy, self.map.gap, self.screen)

        # 初始化分数绘制器
        self.scoredrawer = ScoreDrawer(self.pac, self.map.gap, self.screen)

        # 首次绘制墙体
        self.mapdrawer.draw_wall()

    def update(self):
        self.pacdrawer.clear_pac()
        self.enemydrawer.clear_enemy()
        self.scoredrawer.clear_score()

        self.pac.update()
        self.enemy.update()

        self.mapdrawer.draw_bean()
        self.mapdrawer.draw_power()
        self.scoredrawer.draw_score()
        self.enemydrawer.draw_enemy()
        self.pacdrawer.draw_pac()

        pygame.display.flip()

    def restart(self):
        self.pacdrawer.clear_pac()
        self.enemydrawer.clear_enemy()
        self.scoredrawer.clear_score()
        self.init()

    def deal_event(self, event: pygame.event.Event):
        unicode = event.unicode.lower()
        scancode = event.scancode

        if unicode:
            dir_dict = {
                "wi": -1,
                "sk": 1,
                "aj": -2,
                "dl": 2
            }
            for key, val in dir_dict.items():
                if unicode in key:
                    self.pac.set_dir(val)
                    return

            if unicode == 'r':
                self.restart()
            elif unicode == 'p':
                exit()

        else:
            dir_dict = {
                82: -1,
                81: 1,
                80: -2,
                79: 2
            }
            if scancode in dir_dict:
                self.pac.set_dir(dir_dict[scancode])
