import firstwindow
from functions import *
import SQL


class Registration:
    name = ''
    """Регистрация пользователя"""
    def __init__(self, screen):
        self.error = ''
        self.screen = screen
        # фон
        background = pygame.image.load('image/map.png')
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 50)
        # создание линии для ввода текста
        self.text_input_box = TextInputBox(300, 300, 400, font, self.func)
        group = pygame.sprite.Group(self.text_input_box)
        self.running = True
        # игровой цикл
        while self.running:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
            group.update(event_list)
            screen.blit(background, (0, 0))
            # заголовок
            self.textSurface = font.render('Введите имя: ', True, (0, 0, 0), None)
            self.textRect = self.textSurface.get_rect(center=(500, 200))
            self.screen.blit(self.textSurface, self.textRect)
            if self.error:
                # вывод ошибки
                self.textSurface1 = font.render(f'{self.error}', True, (255, 0, 0), None)
                self.textRect1 = self.textSurface1.get_rect(center=(500, 400))
                self.screen.blit(self.textSurface1, self.textRect1)
            group.draw(screen)
            pygame.display.flip()

    def func(self):
        self.name = self.text_input_box.text
        Registration.name = self.name
        self.running = False
        if self.name == '':
            self.error = 'Ошибка! Слишком короткое имя!'
        elif len(self.name) > 50:
            self.error = 'Ошибка! Слишком длинное имя!'
        else:
            SQL.Player(self.name)
            firstwindow.Menu(self.screen)
