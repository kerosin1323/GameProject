import pygame
import sys
import firstwindow
from const import *

# запуск программы
if __name__ == '__main__':
    # инициализация pygame
    pygame.init()
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)
    # название окна
    pygame.display.set_caption('PyBall')
    while True:
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        firstwindow.Menu(screen)
        pygame.display.flip()
        fpsClock.tick(FPS)