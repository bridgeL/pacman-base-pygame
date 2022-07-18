import os
import pygame
from pacman.clock import Clock
from pacman.game import Game

# 规定每次启动pygame界面的左上角坐标
os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

# 初始化
pygame.init()

# 初始化时钟激励
clock = Clock(100)

# 初始化屏幕
screen = pygame.display.set_mode((560, 620))

game = Game(screen)
game.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            game.deal_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gap = game.map.gap
                p = [(x-gap/2) / gap for x in event.pos]
                p.reverse()
                print(p)

    if clock.check():
        game.update()

