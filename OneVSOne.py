import pygame
from functions import *
from const import *


class ChooseCountries:
    """Создание окна с выбором стран пользователей"""
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill((0, 0, 0))
        fontObj = pygame.font.Font(None, 50)
        self.textSurfaceObj = fontObj.render('Выберите страны', True, (255, 255, 255), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(400, 80))
        screen.blit(self.textSurfaceObj, self.textRectObj)
        triangle1 = (80, 350), (80, 250), (30, 300)
        triangle2 = (250, 350), (250, 250), (300, 300)
        triangle3 = (550, 350), (550, 250), (500, 300)
        triangle4 = (720, 350), (720, 250), (770, 300)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle1)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle2)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle3)
        pygame.draw.polygon(self.screen, (0, 255, 0), triangle4)
        font_vs = pygame.font.Font(None, 180)
        self.text_vs_surface = font_vs.render('VS', True, (255, 255, 255), None)
        self.text_vs = self.textSurfaceObj.get_rect(center=(470, 265))
        self.screen.blit(self.text_vs_surface, self.text_vs)
        self.id_country1 = 0
        self.id_country2 = 0
        while True:
            self.image1 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[self.id_country1]]}.png')
            self.image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[self.id_country2]]}.png')
            screen.blit(self.image1, (90, 250))
            screen.blit(self.image2, (560, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 30 < mouse_pos[0] < 80 and 250 < mouse_pos[1] < 350:
                        if self.id_country1 == 0:
                            self.id_country1 = 19
                        else:
                            self.id_country1 -= 1
            pygame.display.flip()



    def back_country(self):
        pass

    def next_country(self):
        pass
