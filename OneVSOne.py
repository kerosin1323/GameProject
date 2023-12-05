import pygame
from functions import *


class ChooseCountries:
    """Создание окна с выбором стран пользователей"""
    def __init__(self, screen):
        fontObj = pygame.font.Font(None, 50)
        self.textSurfaceObj = fontObj.render('Выберите страны', True, (255, 255, 255), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(400, 80))
        screen.blit(self.textSurfaceObj, self.textRectObj)

    def back_country(self):
        pass

    def next_country(self):
        pass