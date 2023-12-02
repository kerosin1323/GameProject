import pygame
import sys
import firstwindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    pygame.init()
    size = width, height = 800, 600
    fps = 60
    fpsClock = pygame.time.Clock()
    objects = []
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('PyBall')
    pygame.display.flip()
    while True:
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        firstwindow.ChooseMode(screen)

        pygame.display.flip()
        fpsClock.tick(fps)