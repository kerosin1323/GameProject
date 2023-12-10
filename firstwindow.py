import sys
import AgainstBot
import OneVSOne
from functions import *


class Menu:
    """Создание стартового меню"""
    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))
        # нарисовка кнопок
        Button(250, 150, 500, 80, '1 VS 1', self.objects, self.open_one_vs_one, self.screen)
        Button(250, 300, 500, 80, 'Против бота', self.objects, self.open_against_bot, self.screen)
        Button(250, 450, 500, 80, 'Настройки', self.objects, self.open_settings, self.screen)
        font = pygame.font.Font(None, 50)
        # заголовок окна
        self.textSurface = font.render('PyGame', True, (255, 255, 255), None)
        self.textRect = self.textSurface.get_rect(center=(500, 80))
        self.screen.blit(self.textSurface, self.textRect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # оработка нажатия на кнопку
                for i in self.objects:
                    i.process()
            pygame.display.flip()

    def open_one_vs_one(self):
        OneVSOne.ChooseCountries(self.screen)

    def open_against_bot(self):
        AgainstBot.ChooseCountry(self.screen)

    def open_settings(self):
        pass
