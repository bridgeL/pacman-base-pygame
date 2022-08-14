import pygame
from pacman.core.pac import Pac
from pacman.core.enemy import Enemy
from pacman.draw.drawer import BaseDrawer


class EnemyDrawer(BaseDrawer):
    def __init__(self, pac: Pac, enemy: Enemy, gap: int, screen: pygame.Surface) -> None:
        self.pac = pac
        self.enemy = enemy
        self.screen = screen
        self.gap = gap
        self.dead_color = (255, 255, 255)
        self.fear_color = (0, 0, 255)
        self.color = (255, 0, 255)

    def draw_color(self, color):
        base = self.gap / 2
        pos = [x + base for x in self.enemy.pos]
        pos.reverse()
        pygame.draw.circle(self.screen, color, pos, 7, 7)

    def get_color(self):
        # 死亡，回家中
        if self.enemy.dead:
            # 快复活时，闪烁提示
            if self.enemy.revive >= 50 or int(self.enemy.revive / 10) % 2:
                return self.dead_color
            return self.fear_color

        # 逃跑
        if self.enemy.fear:
            # 快结束时，闪烁提示
            if self.pac.power >= 50 or int(self.pac.power / 10) % 2:
                return self.fear_color
            return self.color

        # 常规
        return self.color

    def draw(self):
        color = self.get_color()
        self.draw_color(color)

    def clear(self):
        self.draw_color((0, 0, 0))
