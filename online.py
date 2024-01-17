import sys
import stats
from const import *
import firstwindow
import game
from functions import *


class Online:
    def __init__(self, screen):
        self.screen = screen
        self.error = ''
        # фон экрана
        background = pygame.image.load('image/map.png')
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 50)
        # линия ввода кода игры
        self.text_input_box = TextInputBox(300, 450, 400, font, self.func)
        group = pygame.sprite.Group(self.text_input_box)

        self.id_country1 = 0
        running = True
        # игровой цикл
        while running:
            screen.blit(background, (0, 0))
            # заголовок
            self.textSurface = font.render('Введите пароль игры: ', True, (255, 255, 255), None)
            self.textRect = self.textSurface.get_rect(center=(500, 400))
            self.screen.blit(self.textSurface, self.textRect)
            # заголовок окна
            self.textSurfaceObj = font.render('Выберите страну', True, (255, 255, 255), None)
            self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 60))
            screen.blit(self.textSurfaceObj, self.textRectObj)

            # создание треугольных кнопок
            triangle1 = (375, 300), (375, 200), (325, 250)
            triangle2 = (625, 300), (625, 200), (675, 250)
            pygame.draw.polygon(self.screen, (0, 255, 0), triangle1)
            pygame.draw.polygon(self.screen, (0, 255, 0), triangle2)

            # кнопки движения назад и вперед по окнам и кнопки для открывания статистики
            self.image_back = pygame.image.load('image/home.png')
            self.image_next = pygame.image.load('image/next.png')
            self.image_stats = pygame.image.load('image/stats.png')
            # вывод на экран
            screen.blit(self.image_stats, (30, 30))
            screen.blit(self.image_back, (30, 510))
            screen.blit(self.image_next, (900, 510))
            # создание флага страны
            self.image1 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[self.id_country1]]}.png')
            screen.blit(self.image1, (390, 175))
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # обработка нажатия
                    if 325 < mouse_pos[0] < 375 and 200 < mouse_pos[1] < 300:
                        if self.id_country1 == 0:
                            self.id_country1 = 19
                        else:
                            self.id_country1 -= 1
                    elif 625 < mouse_pos[0] < 675 and 200 < mouse_pos[1] < 300:
                        if self.id_country1 == 19:
                            self.id_country1 = 0
                        else:
                            self.id_country1 += 1
                    elif 30 < mouse_pos[0] < 100 and 510 < mouse_pos[1] < 580:
                        firstwindow.Menu(screen)
                        running = False
                    elif 900 < mouse_pos[0] < 970 and 510 < mouse_pos[1] < 580:
                        game.Pitch(screen, 'online', self.id_country1)
                        running = False
                    elif 30 < mouse_pos[0] < 100 and 30 < mouse_pos[1] < 100:
                        stats.Stats(screen, 'online')
                        running = False
            if running:
                group.update(event_list)
                if self.error:
                    # вывод ошибки
                    self.textSurface1 = font.render(f'{self.error}', True, (255, 0, 0), None)
                    self.textRect1 = self.textSurface1.get_rect(center=(500, 520))
                    self.screen.blit(self.textSurface1, self.textRect1)
                group.draw(screen)
                pygame.display.flip()

    def func(self):
        self.name = self.text_input_box.text
        if sum([1 for i in self.name if i.isdigit()]) != len(self.name):
            self.error = 'Ошибка! Пароль должны состоять из чисел!'
        else:
            game.Pitch(self.screen, 'online', self.id_country1)
