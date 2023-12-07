import sys
from const import *
import pygame
from functions import *
import OneVSOne


class Menu:
    """Создание стартовой менюшки"""
    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        self.screen.fill((0, 0, 0))
        # нарисовка кнопок
        Button(200, 150, 400, 80, '1 VS 1', self.objects, self.open_one_vs_one, self.screen)
        Button(200, 300, 400, 80, 'Против бота', self.objects, self.open_against_bot, self.screen)
        Button(200, 450, 400, 80, 'Настройки', self.objects, self.open_settings, self.screen)
        font = pygame.font.Font(None, 50)
        # заголовок окна
        self.textSurface = font.render('PyGame', True, (255, 255, 255), None)
        self.textRect = self.textSurface.get_rect(center=(400, 80))
        self.screen.blit(self.textSurface, self.textRect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # оработка нажатия на кнопку
                for object in self.objects:
                    object.process()
            pygame.display.flip()

    def open_one_vs_one(self):
        OneVSOne.ChooseCountries(self.screen)

    def open_against_bot(self):
        pass

    def open_settings(self):
        pass

