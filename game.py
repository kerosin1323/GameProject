import random
import time
import pygame.sprite

import AgainstBot
import OneVSOne
import online
from OneVSOne import *
import SQL
import registration


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
        timer = pygame.time.Clock()
        while running:
            timer.tick(30)
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
                    player1 = Player(300, 376, True)
                    player2 = Player(620, 376)
                    ball = Ball(500, 440)
                    self.is_scored = False
                if 0 <= ball.rect.x - player1.rect.x - 60 <= 50 and keys[pygame.K_f]:
                    shot1 = True
                    shot2 = False
                elif 0 <= player2.rect.x - ball.rect.x - 50 <= 50 and keys[pygame.K_SPACE]:
                    shot2 = True
                    shot1 = False
                else:
                    shot1, shot2 = False, False
                if player1.collide_ball_left(ball) and not left1:
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
    sound_idx = 1

    def __init__(self, screen, called):
        self.screen = screen
        self.called = called
        self.back = pygame.image.load('image/exit.png')
        self.rules = pygame.image.load('image/rules.png')
        self.play = pygame.image.load('image/next.png')
        self.running = True

    def draw(self):
        pygame.draw.rect(self.screen, (255, 204, 0), (340, 260, 320, 80))
        self.sound = pygame.image.load(f'image/sound{SettingsGame.sound_idx}.png')
        self.volume = pygame.mixer.music.get_volume()
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
                        if SettingsGame.sound_idx == 4:
                            SettingsGame.sound_idx = 1
                            self.volume = 1.0
                            pygame.mixer.music.set_volume(self.volume)
                        else:
                            SettingsGame.sound_idx += 1
                            self.volume -= 0.33
                            pygame.mixer.music.set_volume(self.volume)
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
        if ball.rect.x > 900 and ball.rect.y > self.rect.y:
            return 1
        elif ball.rect.x < 50 and ball.rect.y > self.rect.y:
            return 2


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.ball_idx = 0
        self.image_ball = pygame.image.load(f'image/ball{self.ball_idx + 1}.png')
        self.mask = pygame.mask.from_surface(self.image_ball)
        self.rect = self.image_ball.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_shot = False
        self.shot_count = 0.5
        self.speed = 7
        self.xvel = 0
        self.yvel = 0
        self.ymax = 0
        self.stop_y = False
        self.shot_y = 0.5

    def update(self, left, right, shot1, shot2, p1, p2):
        if self.check_crossbar_left():
            print(self.check_crossbar_left(), 1)
        if self.speed != 7 and (p1.right and right or p2.left and left):
            self.speed = 7
        if left or self.rect.x >= 940:
            self.xvel = -self.speed
        elif right or self.rect.x <= 10:
            self.xvel = self.speed
        if self.rect.x >= 940:
            self.xvel = -self.speed
            self.is_shot = False
        elif self.rect.x <= 10:
            self.xvel = self.speed
            self.is_shot = False

        if not self.is_shot:
            if shot1:
                self.is_shot = 1
                self.stop_y = False
                self.shot_y = 0.5
                self.yvel = self.ymax = min(max(30 - (self.rect.x - p1.rect.x - 60), 10), 22)
            elif shot2:
                self.is_shot = -1
                self.stop_y = False
                self.shot_y = 0.5
                self.yvel = self.ymax = min(max(30 - (p2.rect.x - self.rect.x - 50), 10), 22)
        else:
            if abs(self.xvel) <= 50:
                self.shot_count += 2 * self.is_shot
                self.xvel = self.shot_count
            else:
                self.is_shot = False
                self.shot_count = 0.5

        if self.yvel >= -self.ymax and not self.stop_y:
            self.rect.y -= self.yvel
            self.yvel -= self.shot_y
        else:
            self.yvel = self.ymax
            self.stop_y = True
        if self.stop_y and self.rect.y != 440:
            self.rect.y += self.yvel
            self.yvel -= self.shot_y + 1
        if self.rect.y == 440:
            self.ymax *= 0.8
            self.yvel = self.ymax
            self.shot_y = 1
            self.stop_y = False
        if self.rect.x == 940 or self.rect.x == 10:
            self.ymax *= 0.5
            self.yvel = self.ymax
            self.stop_y = False
        if self.collide_both(p1, p2):
            self.xvel = 0
            self.yvel = 0
        if self.rect.x + self.xvel <= p1.rect.x + 60 <= self.rect.x and p1.rect.y <= self.rect.y + 50 <= p1.rect.y + 114 and \
                (not p1.left and self.is_shot or p1.left and not self.is_shot or p1.left and self.is_shot or not (p1.left and self.is_shot)):
            self.rect.x = p1.rect.x + 60
            if self.is_shot:
                self.speed = 3
            else:
                self.speed //= 2
            self.xvel = self.speed
            self.is_shot = False
            self.shot_count = 0.5
            self.ymax *= 1.2
            self.yvel = self.ymax
            self.shot_y = 1.5
        elif self.rect.x + self.xvel + 50 >= p2.rect.x + 20 >= self.rect.x + 50 and p2.rect.y <= self.rect.y + 50 <= p2.rect.y + 114 and \
                (not p2.right and self.is_shot or p2.right and not self.is_shot or p2.right and self.is_shot or not (p2.right and self.is_shot)):
            self.rect.x = p2.rect.x - 40
            if self.is_shot:
                self.speed = 3
            else:
                self.speed //= 2
            self.is_shot = False
            self.xvel = -self.speed
            self.shot_count = 0.5
            self.ymax *= 1.2
            self.yvel = self.ymax
            self.shot_y = 1.5
        else:
            if 10 <= self.rect.x + self.xvel <= 940:
                self.rect.x += self.xvel
            elif self.rect.x + self.xvel <= 10:
                self.rect.x = 10
            elif self.rect.x + self.xvel >= 940:
                self.rect.x = 940
        if self.rect.y > 440:
            self.rect.y = 440
        if self.xvel:
            if self.ball_idx == 3:
                self.ball_idx = 0
            else:
                self.ball_idx += 1

    def draw(self, screen):  # Выводим себя на экран
        self.image_ball = pygame.image.load(f'image/ball{self.ball_idx + 1}.png')
        screen.blit(self.image_ball, (self.rect.x, self.rect.y))

    def collide_both(self, player1, player2):
        return player1.rect.x + 60 <= self.rect.x <= self.rect.x + 50 <= player2.rect.x + 60 and player1.rect.y + 114 == self.rect.y + 50 \
            and player2.rect.x - player1.rect.x <= 100

    def check_crossbar_left(self):
        if self.rect.x <= 90 and self.rect.y + 50 == 285:
            return 1
        elif self.rect.x == 100 and 235 <= self.rect.y <= 295:
            return 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, turn=False):
        super().__init__()
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        if turn:
            self.player_image = load_image('image/player1.png')
        else:
            self.player_image = load_image('image/player2.png')
        self.is_jump = False
        self.jump_count = 24
        self.rect = self.player_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.player_image)

    def update(self, left, right, up):
        self.left = left
        self.right = right
        if not self.is_jump:
            if up:
                self.is_jump = True
        else:
            if self.jump_count >= -24:
                self.rect.y -= self.jump_count
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

        if 10 <= self.rect.x + self.xvel <= 910:
            self.rect.x += self.xvel  # переносим свои положение на xvel

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.player_image, (self.rect.x, self.rect.y))

    def collide_ball_left(self, ball):
        return pygame.sprite.collide_mask(self, ball)

    def collide_ball_right(self, ball):
        return pygame.sprite.collide_mask(ball, self)