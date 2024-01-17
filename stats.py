import sys
import pygame
import AgainstBot
import SQL
import online
import registration


class Stats:
    """Статистика матчей пользователя"""
    def __init__(self, screen, called):
        self.screen = screen
        # фон экрана
        background = pygame.image.load('image/map.png')
        screen.blit(background, (0, 0))
        fontObj = pygame.font.Font(None, 50)

        # заголовок окна
        self.textSurfaceObj = fontObj.render('Статистика', True, (0, 0, 0), None)
        self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 80))
        screen.blit(self.textSurfaceObj, self.textRectObj)

        category = ['Матчи', 'Победы', 'Ничьи', 'Поражения', 'Забито', 'Пропущено', 'Сухие матчи']
        for i in category:
            self.textSurface = fontObj.render(f'{i}', True, (0, 0, 0), None)
            self.textRect = self.textSurface.get_rect(topleft=(100, 150 + category.index(i) * 50))
            screen.blit(self.textSurface, self.textRect)
        # БД
        name = registration.Registration.name
        if called == 'AgainstBot':
            data = SQL.AgainstBotDB(name).get_all()[0]
        else:
            data = SQL.OnlineDB(name).get_all()[0]
        for i, j in enumerate(data):
            self.dataSurface = fontObj.render(f'{j}', True, (0, 255, 0), None)
            self.dataRect = self.dataSurface.get_rect(center=(600, 165 + i * 50))
            screen.blit(self.dataSurface, self.dataRect)
        self.image_back = pygame.image.load('image/home.png')
        screen.blit(self.image_back, (30, 510))
        running = True
        # игровой цикл
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # обработка нажатия
                elif event.type == pygame.MOUSEBUTTONDOWN and running:
                    mouse_pos = pygame.mouse.get_pos()
                    if 30 < mouse_pos[0] < 100 and 510 < mouse_pos[1] < 580:
                        running = False
                        if called == 'AgainstBot':
                            AgainstBot.ChooseCountry(screen)
                        else:
                            online.Online(screen)
            pygame.display.flip()
