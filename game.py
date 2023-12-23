import random

import pygame.sprite
from const import *
from OneVSOne import *
import SQL
import registration


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Pitch:
    """Класс для создания поля"""

    def __init__(self, screen, called, id1, id2=None):
        id2 = random.randint(0, 19) if id2 is None else id2
        # загрузка фона

        fontObj = pygame.font.Font(None, 50)
        # счетчик таймера
        self.goals1 = 0
        self.goals2 = 0
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))

        running = True
        countdown = 90
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        image = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id1]]}.png')
        con_image = pygame.transform.scale(image, (90, 60))
        image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id2]]}.png')
        con_image2 = pygame.transform.scale(image2, (90, 60))
        player1 = Player(300, 340)
        player2 = Player(700, 340)
        ball = Ball(500, 440)
        gates1 = Gates((10, 285), screen)
        gates2 = Gates((900, 285), screen)
        left = right = False
        while running:
            timer = pygame.time.Clock()
            timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 5 < mouse_pos[0] < 95 and 250 < mouse_pos[1] < 494:
                        self.goals2 += 1
                    elif 905 < mouse_pos[0] < 995 and 250 < mouse_pos[1] < 494:
                        self.goals1 += 1
                elif event.type == TIMEREVENT:
                    countdown -= 1
                    if countdown == -1:
                        running = False
                        EndGame(screen, id1, id2, self.goals1, self.goals2, called)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                left = True
                right = False
            elif keys[pygame.K_RIGHT]:
                right = True
                left = False
            else:
                left = right = False
            screen.blit(background, (0, 0))
            # создание флагов, которые выбрали игроки
            screen.blit(con_image2, (550, 510))
            screen.blit(con_image, (350, 510))
            # создание счета
            self.score = fontObj.render(f'{self.goals1} : {self.goals2}', True, (0, 0, 0), None)
            self.scoreRect = self.score.get_rect(center=(495, 540))
            screen.blit(self.score, self.scoreRect)
            self.textSurfaceObj = fontObj.render(f'{countdown}', True, (0, 0, 0), None)
            self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 30))
            screen.blit(self.textSurfaceObj, self.textRectObj)
            player1.update(left, right)
            player1.draw(screen)
            player2.draw(screen)
            gates1.draw()
            gates2.draw()
            gates1.add(horizontal_borders)
            gates2.add(horizontal_borders)
            if player1.collide_ball(screen):
                ball.update(False, True)
            ball.draw(screen)
            pygame.display.flip()


class EndGame:
    def __init__(self, screen, id1, id2, score1, score2, called):
        name = registration.Registration.name
        if score1 > score2:
            res = (1, 0, 0)
        elif score1 == score2:
            res = (0, 1, 0)
        else:
            res = (0, 0, 1)
        if called == 'AgainstBot':
            SQL.AgainstBotDB(name).append(res, score1, score2, 'play-off', COUNTRIES_FLAG[COUNTRY[id1]],
                                          COUNTRIES_FLAG[COUNTRY[id2]])
        elif called == 'online':
            SQL.OnlineDB(name).append(res, score1, score2)
        self.screen = screen
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))
        fontObj = pygame.font.Font(None, 50)
        self.buttonSurface = pygame.Surface((400, 300))
        self.buttonRect = pygame.Rect(300, 150, 400, 300)
        self.buttonSurface.fill((255, 204, 0))
        self.screen.blit(self.buttonSurface, self.buttonRect)
        image = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id1]]}.png')
        con_image = pygame.transform.scale(image, (90, 60))
        image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id2]]}.png')
        con_image2 = pygame.transform.scale(image2, (90, 60))
        pygame.draw.rect(screen, (0, 0, 0), [559, 249, 92, 62])
        pygame.draw.rect(screen, (0, 0, 0), [349, 249, 92, 62])
        screen.blit(con_image2, (560, 250))
        screen.blit(con_image, (350, 250))
        self.image_next = pygame.image.load('image/next.png')
        screen.blit(self.image_next, (470, 350))
        running = True
        self.score = fontObj.render(f'{score1} : {score2}', True, (0, 0, 0), None)
        self.scoreRect = self.score.get_rect(center=(495, 280))
        screen.blit(self.score, self.scoreRect)
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 470 < mouse_pos[0] < 545 and 350 < mouse_pos[1] < 425:
                        pygame.time.delay(50)
                        firstwindow.Menu(self.screen)


class Gates(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, screen, turn=False):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.image_gate = pygame.image.load('image/gates1.png')
        self.imageSur = pygame.Surface((90, 205))
        self.rect = self.image_gate.get_rect()
        self.rect.x, self.rect.y = pos

    def draw(self):
        self.screen.blit(self.image_gate, self.pos)

    def check_goal(self):
        horizontal_borders = pygame.sprite.Group()
        return pygame.sprite.spritecollideany(Gates(self.pos, self.screen), horizontal_borders) \
            and not pygame.sprite.collide_rect(Gates(self.pos, self.screen), Player(self.pos, self.screen))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.y = y
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA, 32)
        self.image_ball = pygame.image.load('image/ball1.png')
        self.rect = pygame.Rect(x, y, 50, 50)  # прямоугольный объект
        self.add(horizontal_borders)

    def update(self, left, right):
        if left:
            self.xvel = -7  # Лево = x- n

        if right:
            self.xvel = 7  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        self.x += self.xvel # переносим свои положение на xvel
        self.remove(horizontal_borders)
        self.add(horizontal_borders)

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image_ball, (self.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = pygame.Surface((80, 150))
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x, y, 80, 150)  # прямоугольный объект

    def update(self, left, right, ):
        if left:
            self.xvel = -7  # Лево = x- n

        if right:
            self.xvel = 7  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if 10 <= self.rect.x + self.xvel <= 900:
            self.rect.x += self.xvel # переносим свои положение на xvel

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide_ball(self, screen):
        print(horizontal_borders)
        return pygame.sprite.spritecollideany(self, horizontal_borders) \
                and not pygame.sprite.collide_rect(self, Gates((10, 285), screen)) \
                and not pygame.sprite.collide_rect(self, Gates((900, 285), screen))
