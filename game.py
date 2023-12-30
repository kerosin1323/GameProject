import random
import time

import pygame.sprite

import AgainstBot
import OneVSOne
import online
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
        player1 = Player(300, 376, True)
        player2 = Player(620, 376)
        ball = Ball(475, 440)
        gates1 = Gates((10, 285), screen)
        gates2 = Gates((900, 285), screen, True)
        left1 = up1 = right1 = False
        left2 = up2 = right2 = False
        shot1 = shot2 = left = right = False
        self.is_scored = False
        self.game = True
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 20 < mouse_pos[0] < 90 and 20 < mouse_pos[1] < 90:
                        settings = SettingsGame(screen, called)
                        settings.draw()
                        self.game = False
            keys = pygame.key.get_pressed()
            if self.game or not settings.is_running():
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
                screen.blit(con_image2, (560, 510))
                screen.blit(con_image, (350, 510))
                # создание счета
                self.score = fontObj.render(f'{self.goals1} : {self.goals2}', True, (0, 0, 0), None)
                self.scoreRect = self.score.get_rect(center=(500, 540))
                screen.blit(self.score, self.scoreRect)
                self.textSurfaceObj = fontObj.render(f'{countdown}', True, (0, 0, 0), None)
                self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 30))
                screen.blit(self.textSurfaceObj, self.textRectObj)
                if self.is_scored:
                    time.sleep(1)
                    player1 = Player(300, 340)
                    player2 = Player(700, 340)
                    ball = Ball(500, 440)
                    self.is_scored = False
                if pygame.sprite.collide_mask(player1, ball) and keys[pygame.K_f]:
                    shot1 = True
                    shot2 = False
                elif pygame.sprite.collide_mask(ball, player2) and keys[pygame.K_SPACE]:
                    shot2 = True
                    shot1 = False
                else:
                    shot1, shot2 = False, False
                if player1.collide_ball_left(ball) and not left1:
                    print(1)
                    right = True
                    left = False
                elif player2.collide_ball_right(ball) and not right2:
                    left = True
                    right = False
                else:
                    left, right = False, False
                if ball.collide_both(player1, player2) and not (left1 or right2 or up1 or up2):
                    shot1 = shot2 = left = right = left1 = left2 = right1 = right2 = False
                player1.update(left1, right1, up1)
                player2.update(left2, right2, up2)
                ball.update(left, right, shot1, shot2, player1, player2)
                if gates1.check_goal(ball) == 1:
                    self.goals1 += 1
                    self.is_scored = True
                elif gates2.check_goal(ball) == 2:
                    self.goals2 += 1
                    self.is_scored = True
                player1.draw(screen)
                player2.draw(screen)
                ball.draw(screen)
                gates1.draw()
                gates2.draw()
                self.settings = pygame.image.load('image/settings.png')
                screen.blit(self.settings, (20, 20))
            pygame.display.flip()


class SettingsGame:
    def __init__(self, screen, called):
        self.sound_idx = 1
        self.screen = screen
        self.called = called
        self.back = pygame.image.load('image/exit.png')
        self.rules = pygame.image.load('image/rules.png')
        self.play = pygame.image.load('image/next.png')
        self.running = True

    def draw(self):
        pygame.draw.rect(self.screen, (255, 204, 0), (340, 260, 320, 80))
        self.sound = pygame.image.load(f'image/sound{self.sound_idx}.png')
        self.screen.blit(self.back, (348, 265))
        self.screen.blit(self.rules, (426, 265))
        self.screen.blit(self.sound, (504, 265))
        self.screen.blit(self.play, (582, 265))
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 348 < mouse_pos[0] < 418 and 265 < mouse_pos[1] < 335:
                        if self.called == 'OneVSOne':
                            OneVSOne.ChooseCountries(self.screen)
                        elif self.called == 'AgainstBot':
                            AgainstBot.ChooseCountry(self.screen)
                        elif self.called == 'online':
                            online.Online(self.screen)
                        self.running = False
                    elif 426 < mouse_pos[0] < 496 and 265 < mouse_pos[1] < 335:
                        pass
                    elif 504 < mouse_pos[0] < 574 and 265 < mouse_pos[1] < 335:
                        if self.sound_idx == 4:
                            self.sound_idx = 1
                        else:
                            self.sound_idx += 1
                        self.draw()
                    elif 582 < mouse_pos[0] < 652 and 265 < mouse_pos[1] < 335:
                        self.running = False

    def is_running(self):
        return self.running


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
        self.ball_idx = 0
        self.image_ball = pygame.image.load(f'image/ball{self.ball_idx + 1}.png')
        self.rect = self.image_ball.get_rect()
        print(self.rect.x)
        self.is_shot = False
        self.shot_count = 2
        self.shooting = False
        self.to_left = False
        self.to_right = False
        self.speed = 7
        self.mask = pygame.mask.from_surface(self.image_ball)

    def update(self, left, right, shot1, shot2, p1, p2):
        if not self.is_shot:
            if shot1:
                self.is_shot = True
        else:
            if self.shot_count <= 50:
                self.xvel += self.shot_count
                self.shooting = True
                self.shot_count += 2
            else:
                self.is_shot = False
                self.shot_count = 12
        if not self.shooting:
            if shot2:
                self.xvel = -50
            else:
                if left or self.to_left:
                    self.xvel = -abs(self.speed)
                    self.to_left = True
                elif right or self.to_right:
                    self.xvel = abs(self.speed)
                    self.to_right = True
                if (p1.collide_ball_left(self) and self.to_left or p2.collide_ball_right(self) and self.to_right)\
                        and (right or left):
                    self.speed = self.speed // -2
                    self.to_left = False
                    self.to_right = False

        if self.shooting and left:
            self.is_shot = False
            self.shooting = False
            self.xvel = 0
        if self.x + self.xvel <= p1.rect.x + 80 <= self.x:
            self.x = p1.rect.x + 80
            self.is_shot = False
            self.shooting = False
            self.xvel = 0
        elif self.x + self.xvel >= p2.rect.x >= self.x:
            self.x = p2.rect.x - 50
            self.is_shot = False
            self.shooting = False
            self.xvel = 0
        else:
            if 10 <= self.x + self.xvel <= 940:
                self.x += self.xvel
            elif self.x + self.xvel <= 10:
                self.x = 10
            else:
                self.x = 940
        if self.xvel:
            if self.ball_idx == 3:
                self.ball_idx = 0
            else:
                self.ball_idx += 1

    def draw(self, screen):  # Выводим себя на экран
        self.image_ball = pygame.image.load(f'image/ball{self.ball_idx + 1}.png')
        screen.blit(self.image_ball, (self.x, self.y))

    def collide_both(self, player1, player2):
        return player1.rect.x + 74 <= self.x <= self.x + 50 <= player2.rect.x + 6 and player1.rect.y + 150 == self.y + 50 \
            and player2.rect.x - player1.rect.x <= 130


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, turn=False):
        super().__init__()
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.y = y
        if turn:
            self.player_image = pygame.image.load('image/player2.png')
        else:
            self.player_image = pygame.image.load('image/player1.png')
        self.is_jump = False
        self.jump_count = 24
        self.rect = self.player_image.get_rect()
        self.mask = pygame.mask.from_surface(self.player_image)

    def update(self, left, right, up):
        if not self.is_jump:
            if up:
                self.is_jump = True
        else:
            if self.jump_count >= -24:
                self.y -= self.jump_count
                self.jump_count -= 4
            else:
                self.is_jump = False
                self.jump_count = 24
        if left:
            self.xvel = -7  # Лево = x- n

        if right:
            self.xvel = 7  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if 10 <= self.x + self.xvel <= 910:
            self.x += self.xvel  # переносим свои положение на xvel

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.player_image, (self.x, self.y))

    def collide_ball_left(self, ball):
        return pygame.sprite.collide_mask(self, ball)

    def collide_ball_right(self, ball):
        return pygame.sprite.collide_mask(ball, self)
