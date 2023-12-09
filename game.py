import sys
from const import *
import pygame
import time
from OneVSOne import *


class Pitch:
    def __init__(self, screen, id1, id2=None):
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))
        fontObj = pygame.font.Font(None, 50)
        countdown = 90
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        while True:
            pygame.time.delay(100)
            image = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id1]]}.png')
            con_image = pygame.transform.scale(image, (90, 60))
            if id2 is not None:
                image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id2]]}.png')
                con_image2 = pygame.transform.scale(image2, (90, 60))
                screen.blit(con_image2, (600, 510))
            screen.blit(con_image, (400, 510))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == TIMEREVENT:
                    pygame.draw.rect(screen, (0, 0, 0), (480, 10, 40, 40))
                    self.textSurfaceObj = fontObj.render(f'{countdown}', True, (255, 255, 255), None)
                    self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 30))
                    screen.blit(self.textSurfaceObj, self.textRectObj)
                    countdown -= 1


            pygame.display.flip()
