import pygame
from const import *
import firstwindow
import sys
import game


class ChooseCountry:
    def __init__(self, screen):
        self.screen = screen
        # фон экрана
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))
        fontObj = pygame.font.Font(None, 50)

        # заголовок окна
        self.textSurfaceObj = fontObj.render('Выберите страну', True, (255, 255, 255), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 80))
        screen.blit(self.textSurfaceObj, self.textRectObj)

        # создание треугольных кнопок
        triangle1 = (375, 350), (375, 250), (325, 300)
        triangle2 = (625, 350), (625, 250), (675, 300)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle1)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle2)

        self.id_country1 = 0
        while True:
            # кнопки движения назад и вперед по окнам и кнопки для открывания статистики
            self.image_back = pygame.image.load('image/home.png')
            self.image_next = pygame.image.load('image/next.png')
            self.image_stats = pygame.image.load('image/stats.png')
            screen.blit(self.image_stats, (30, 30))
            screen.blit(self.image_back, (30, 510))
            screen.blit(self.image_next, (900, 510))
            # создание флага страны
            self.image1 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[self.id_country1]]}.png')
            screen.blit(self.image1, (390, 225))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # обработка нажатия
                    if 325 < mouse_pos[0] < 375 and 250 < mouse_pos[1] < 350:
                        if self.id_country1 == 0:
                            self.id_country1 = 19
                        else:
                            self.id_country1 -= 1
                    elif 625 < mouse_pos[0] < 675 and 250 < mouse_pos[1] < 350:
                        if self.id_country1 == 19:
                            self.id_country1 = 0
                        else:
                            self.id_country1 += 1
                    elif 30 < mouse_pos[0] < 100 and 510 < mouse_pos[1] < 580:
                        firstwindow.Menu(screen)
                    elif 900 < mouse_pos[0] < 970 and 510 < mouse_pos[1] < 580:
                        game.Pitch(screen, self.id_country1)
            pygame.display.flip()
