import asyncio
import os
import time
import pygame
from pacman.game import Game


# 事件循环
async def game_loop(framerate_limit):
    # 初始化
    loop = asyncio.get_event_loop()

    gap = 1.0 / framerate_limit
    target = 0.0

    while True:
        this_time = time.time()
        delay = target - this_time
        if delay > 0:
            await asyncio.sleep(gap)
        target = this_time + gap

        events = list(pygame.event.get())
        if game.handle_events(events) == -1:
            break

        game.update()
        pygame.display.flip()

    loop.stop()


if __name__ == "__main__":
    # 规定每次启动pygame界面的左上角坐标
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((560, 620))
    game = Game(screen)
    game.update()

    asyncio.run(game_loop(150))

    pygame.quit()
