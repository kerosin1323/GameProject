import sys
import pygame


class Button:
    """Класс для создания кнопки"""
    def __init__(self, x, y, width, height, buttonText, objects, onclickFunction, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        font = pygame.font.Font(None, 35)
        self.screen = screen

        # создание поверхности кнопки и создание кнопки
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.buttonSurface.fill('#ffffff')
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)

        objects.append(self)

    def process(self):
        # обработка нажатия
        mousePos = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]:
                self.onclickFunction()

