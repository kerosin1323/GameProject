import pygame
from functions import *
from const import *
import firstwindow


class ChooseCountries:
    """Создание окна с выбором стран пользователей"""
    def __init__(self, screen):
        self.screen = screen
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))
        fontObj = pygame.font.Font(None, 50)

        # заголовок окна
        self.textSurfaceObj = fontObj.render('Выберите страны', True, (255, 255, 255), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 80))
        screen.blit(self.textSurfaceObj, self.textRectObj)
        font_vs = pygame.font.Font(None, 180)

        # создание треугольных кнопок
        triangle1 = (100, 350), (100, 250), (50, 300)
        triangle2 = (350, 350), (350, 250), (400, 300)
        triangle3 = (650, 350), (650, 250), (600, 300)
        triangle4 = (900, 350), (900, 250), (950, 300)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle1)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle2)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle3)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle4)

        # создание заголовков для указания кто за какую страну будеи играть
        self.text_p1_surface = fontObj.render('Игрок 1', True, (0, 0, 0), None)
        self.text_p1 = self.text_p1_surface.get_rect(center=(235, 190))
        self.screen.blit(self.text_p1_surface, self.text_p1)

        self.text_p2_surface = fontObj.render('Игрок 2', True, (0, 0, 0), None)
        self.text_p2 = self.text_p2_surface.get_rect(center=(765, 190))
        self.screen.blit(self.text_p2_surface, self.text_p2)

        self.text_vs_surface = font_vs.render('VS', True, (0, 0, 0), None)
        self.text_vs = self.textSurfaceObj.get_rect(center=(570, 265))
        self.screen.blit(self.text_vs_surface, self.text_vs)

        self.id_country1 = 0
        self.id_country2 = 0
        while True:
            # кнопки движения назад и вперед по окнам
            self.image_back = pygame.image.load('image/home.png')
            self.image_next = pygame.image.load('image/next.png')
            screen.blit(self.image_back, (30, 510))
            screen.blit(self.image_next, (900, 510))
            # создание флага страны
            self.image1 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[self.id_country1]]}.png')
            self.image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[self.id_country2]]}.png')
            screen.blit(self.image1, (115, 225))
            screen.blit(self.image2, (665, 225))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # изменение флага благодаря нажатию на кнопку
                    if 50 < mouse_pos[0] < 100 and 250 < mouse_pos[1] < 350:
                        if self.id_country1 == 0:
                            self.id_country1 = 19
                        else:
                            self.id_country1 -= 1
                    elif 400 > mouse_pos[0] > 350 > mouse_pos[1] > 250:
                        if self.id_country1 == 19:
                            self.id_country1 = 0
                        else:
                            self.id_country1 += 1
                    elif 600 < mouse_pos[0] < 650 and 250 < mouse_pos[1] < 350:
                        if self.id_country2 == 0:
                            self.id_country2 = 19
                        else:
                            self.id_country2 -= 1
                    elif 900 < mouse_pos[0] < 950 and 250 < mouse_pos[1] < 350:
                        if self.id_country2 == 19:
                            self.id_country2 = 0
                        else:
                            self.id_country2 += 1
                    elif 30 < mouse_pos[0] < 100 and 510 < mouse_pos[1] < 580:
                        firstwindow.Menu(screen)
                    elif 900 < mouse_pos[0] < 970 and 510 < mouse_pos[1] < 580:
                        pass
            pygame.display.flip()