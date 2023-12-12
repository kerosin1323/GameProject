import pygame
import registration
from const import *

# запуск программы
if __name__ == '__main__':
    # инициализация pygame
    pygame.init()
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    # название окна
    pygame.display.set_caption('PyBall')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        registration.Registration(screen)
        pygame.display.flip()
        fpsClock.tick(FPS)
