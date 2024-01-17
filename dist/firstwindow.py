import AgainstBot
import OneVSOne
from functions import *
import registration
import online


class Menu:
    """Создание стартового меню"""
    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        # фон
        background = pygame.image.load('image/map.png')
        screen.blit(background, (0, 0))
        # нарисовка кнопок
        Button(250, 120, 500, 80, '1 VS 1', self.objects, self.open_one_vs_one, self.screen)
        Button(250, 270, 500, 80, 'Против бота', self.objects, self.open_against_bot, self.screen)
        Button(250, 420, 500, 80, 'Онлайн', self.objects, self.open_online, self.screen)
        font = pygame.font.Font(None, 50)
        # заголовок окна
        self.textSurface = font.render('PyBall', True, (255, 255, 255), None)
        self.textRect = self.textSurface.get_rect(center=(500, 70))
        self.screen.blit(self.textSurface, self.textRect)
        # кнопка выхода
        self.image_exit = pygame.image.load('image/exit.png')
        self.screen.blit(self.image_exit, (30, 30))
        self.running = True
        # игровой цикл
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # обработка нажатия
                elif event.type == pygame.MOUSEBUTTONDOWN and self.running:
                    mouse_pos = pygame.mouse.get_pos()
                    if 30 < mouse_pos[0] < 100 and 30 < mouse_pos[1] < 100:
                        self.running = False
                        registration.Registration(screen)
                # оработка нажатия на кнопку
                if self.running:
                    for i in self.objects:
                        i.process()
            pygame.display.flip()

    def open_one_vs_one(self):
        self.running = False
        OneVSOne.ChooseCountries(self.screen)

    def open_against_bot(self):
        self.running = False
        AgainstBot.ChooseCountry(self.screen)

    def open_online(self):
        self.running = False
        online.Online(self.screen)
