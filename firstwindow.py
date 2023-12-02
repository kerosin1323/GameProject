import pygame
from functions import *


class ChooseMode:
    def __init__(self, screen):
        fontObj = pygame.font.Font(None, 50)
        self.textSurfaceObj = fontObj.render('PyGame', True, (255, 255, 255), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(400, 80))
        screen.blit(self.textSurfaceObj, self.textRectObj)

        self.objects = []

        Button(200, 150, 400, 80, '1 VS 1', self.objects, self.open_one_vs_one)
        Button(200, 300, 400, 80, 'Против бота', self.objects, self.open_against_bot)
        Button(200, 450, 400, 80, 'Настройки', self.objects, self.open_settings)
        for object in self.objects:
            object.process(screen)

    def open_one_vs_one(self):
        pass

    def open_against_bot(self):
        pass

    def open_settings(self):
        pass

