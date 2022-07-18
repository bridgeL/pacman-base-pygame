import pygame
from pacman.core.pac import Pac
from pacman.core.enemy import Enemy
from pacman.draw.astar import AStarDrawer


class EnemyDrawer:
    def __init__(self, pac: Pac, enemy: Enemy, gap: int, screen: pygame.Surface) -> None:
        self.pac = pac
        self.enemy = enemy
        self.screen = screen
        self.gap = gap
        self.astardrawer = AStarDrawer(enemy.astar, gap, screen)

    def draw(self, color):
        gap = self.gap
        pos = [x + gap/2 for x in self.enemy.pos]
        pos.reverse()
        pygame.draw.circle(self.screen, color, pos, 7, 7)

    def draw_enemy(self):
        self.astardrawer.draw_path()

        if self.enemy.dead:
            if self.enemy.revive >= 50:
                color = (255, 255, 255)
            # 快结束时，闪烁提示
            elif int(self.enemy.revive / 10) % 2:
                color = (255, 255, 255)
            else:
                color = (0, 0, 255)
        elif self.enemy.fear:
            # 快结束时，闪烁提示
            if self.pac.power >= 50:
                color = (0, 0, 255)
            elif int(self.pac.power / 10) % 2:
                color = (255, 0, 255)
            else:
                color = (0, 0, 255)
        else:
            color = (255, 0, 255)

        self.draw(color)

    def clear_enemy(self):
        self.astardrawer.clear_path()
        self.draw((0, 0, 0))
