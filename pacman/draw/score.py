import pygame
from pacman.core.pac import Pac
from pacman.draw.drawer import BaseDrawer


class ScoreDrawer(BaseDrawer):
    def __init__(self, pac: Pac, gap: int, screen: pygame.Surface) -> None:
        self.pac = pac
        self.screen = screen
        self.gap = gap
        self.font = pygame.font.SysFont('dengxian', 20)

    def get_text(self):
        gap = self.gap
        x, y = 13.5*gap, 14*gap

        text = f"{self.pac.score}"
        text = self.font.render(text, True, (255, 255, 255))
        pos = text.get_rect(x=x, y=y)

        return text, pos

    def draw(self):
        text, pos = self.get_text()
        self.screen.blit(text, pos)

    def clear(self):
        text, pos = self.get_text()
        pygame.draw.rect(self.screen, (0, 0, 0), pos)
