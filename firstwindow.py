import pygame
from functions import *
import OneVSOne


class Menu:
    """Создание стартовой менюшки"""
    def __init__(self, screen):
        fontObj = pygame.font.Font(None, 50)
        self.textSurfaceObj = fontObj.render('PyGame', True, (255, 255, 255), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(400, 80))
        self.screen = screen
        self.screen.blit(self.textSurfaceObj, self.textRectObj)

        self.objects = []

        Button(200, 150, 400, 80, '1 VS 1', self.objects, self.open_one_vs_one, self.screen)
        Button(200, 300, 400, 80, 'Против бота', self.objects, self.open_against_bot, self.screen)
        Button(200, 450, 400, 80, 'Настройки', self.objects, self.open_settings, self.screen)
        for object in self.objects:
            object.process()

    def open_one_vs_one(self):
        self.screen.fill((0, 0, 0))
        OneVSOne.ChooseCountries(self.screen)
        return

    def open_against_bot(self):
        pass

    def open_settings(self):
        pass

