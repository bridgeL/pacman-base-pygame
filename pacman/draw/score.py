import pygame
from pacman.core.pac import Pac


class ScoreDrawer:
    def __init__(self, pac: Pac, gap: int, screen: pygame.Surface) -> None:
        self.pac = pac
        self.screen = screen
        self.gap = gap
        self.font = pygame.font.SysFont('dengxian', 20)

    def draw_score(self):
        gap = self.gap
        x, y = 13.5*gap, 14*gap

        text = f"{self.pac.score}"
        text = self.font.render(text, True, (255, 255, 255))
        textpos = text.get_rect(x=x, y=y)

        self.screen.blit(text, textpos)

    def clear_score(self):
        gap = self.gap
        x, y = 13.5*gap, 14*gap

        text = f"{self.pac.score}"
        text = self.font.render(text, True, (255, 255, 255))
        textpos = text.get_rect(x=x, y=y)

        pygame.draw.rect(self.screen, (0, 0, 0), textpos)
