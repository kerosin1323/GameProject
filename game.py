import random
import time

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
        # счетчик таймера
        self.goals1 = 0
        self.goals2 = 0
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))

        running = True
        countdown = 90
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        fontObj = pygame.font.Font(None, 50)
        image = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id1]]}.png')
        con_image = pygame.transform.scale(image, (90, 60))
        image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id2]]}.png')
        con_image2 = pygame.transform.scale(image2, (90, 60))
        player1 = Player(300, 340)
        player2 = Player(700, 340)
        ball = Ball(500, 440)
        gates1 = Gates((10, 285), screen)
        gates2 = Gates((900, 285), screen, True)
        shot1 = left1 = up1 = right1 = False
        shot2 = left2 = up2 = right2 = False
        while running:
            timer = pygame.time.Clock()
            timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == TIMEREVENT:
                    countdown -= 1
                    if countdown == -1:
                        running = False
                        EndGame(screen, id1, id2, self.goals1, self.goals2, called)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                shot1 = True
            else:
                shot1 = False
            if keys[pygame.K_SPACE]:
                shot2 = True
            else:
                shot2 = False
            if keys[pygame.K_w]:
                up1 = True
            else:
                up1 = False
            if keys[pygame.K_a]:
                left1 = True
                right1 = False
            elif keys[pygame.K_d]:
                right1 = True
                left1 = False
            else:
                left1 = right1 = False
            if keys[pygame.K_UP]:
                up2 = True
            else:
                up2 = False
            if keys[pygame.K_LEFT]:
                left2 = True
                right2 = False
            elif keys[pygame.K_RIGHT]:
                right2 = True
                left2 = False
            else:
                left2 = right2 = False
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
            player1.update(left1, right1, up1)
            player2.update(left2, right2, up2)
            player1.draw(screen)
            player2.draw(screen)
            if player1.rect.x + 72 <= ball.x <= player1.rect.x + 82 and shot1:
                ball.update(False, False, True, False)
            if player1.collide_ball_left(ball) and not left1:
                ball.update(False, True, False, False)
            if player2.rect.x - 5 <= ball.x + 50 <= player2.rect.x + 7 and shot2:
                ball.update(False, False, False, True)
            if player2.collide_ball_right(ball) and not right2:
                ball.update(True, False, False, False)
            if gates1.check_goal(ball) == 1:
                self.goals1 += 1
                player1 = Player(300, 340)
                player2 = Player(700, 340)
                ball = Ball(500, 440)
            elif gates2.check_goal(ball) == 2:
                self.goals2 += 1
                player1 = Player(300, 340)
                player2 = Player(700, 340)
                ball = Ball(500, 440)
            ball.draw(screen)
            gates1.draw()
            gates2.draw()
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
        if turn:
            self.image_gate = pygame.image.load('image/gates1_right.png')
        else:
            self.image_gate = pygame.image.load('image/gates1_left.png')
        self.imageSur = pygame.Surface((90, 205))
        self.rect = self.image_gate.get_rect()
        self.rect.x, self.rect.y = pos

    def draw(self):
        self.screen.blit(self.image_gate, self.pos)

    def check_goal(self, ball):
        if ball.x > 900 and ball.y - 50 > self.rect.y:
            return 1
        elif ball.x < 50 and ball.y - 50 > self.rect.y:
            return 2


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.y = y
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA, 32)
        self.image_ball = pygame.image.load('image/ball1.png')
        self.rect = pygame.Rect(x, y, 50, 50)  # прямоугольный объект

    def update(self, left, right, shot1, shot2):
        if shot1:
            self.xvel = 50
        elif shot2:
            self.xvel = -50
        elif left:
            self.xvel = -7  # Лево = x- n

        elif right:
            self.xvel = 7  # Право = x + n

        if not (left or right or shot1 or shot2):  # стоим, когда нет указаний идти
            self.xvel = 0
        if 10 <= self.x + self.xvel <= 940:
            self.x += self.xvel
        elif self.x + self.xvel <= 10:
            self.x = 10
        else:
            self.x = 900

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
        self.is_jump = False
        self.jump_count = 12
        self.rect = pygame.Rect(x, y, 80, 150)  # прямоугольный объект

    def update(self, left, right, up):
        if not self.is_jump:
            if up:
                self.is_jump = True
        else:
            if self.jump_count >= -12:
                self.rect.y -= self.jump_count
                self.jump_count -= 2
            else:
                self.is_jump = False
                self.jump_count = 12
        if left:
            self.xvel = -7  # Лево = x- n

        if right:
            self.xvel = 7  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if 10 <= self.rect.x + self.xvel <= 900:
            self.rect.x += self.xvel  # переносим свои положение на xvel

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide_ball_left(self, ball):
        return self.rect.x + 74 <= ball.x <= self.rect.x + 80 and self.rect.y + 150 == ball.y + 50

    def collide_ball_right(self, ball):
        return self.rect.x <= ball.x + 50 <= self.rect.x + 6 and self.rect.y + 150 == ball.y + 50