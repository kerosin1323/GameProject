import random
from OneVSOne import *


class Pitch:
    """Класс для создания поля"""
    def __init__(self, screen, id1, id2=None):
        id2 = random.randint(0, 19) if id2 is None else id2
        # загрузка фона
        background = pygame.image.load('image/map2.png')
        screen.blit(background, (0, 0))
        fontObj = pygame.font.Font(None, 50)
        # счетчик таймера
        countdown = 3
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        self.goals1 = 0
        self.goals2 = 0
        image_gate = pygame.image.load('image/gates1.png')
        screen.blit(image_gate, (5, 285))
        screen.blit(image_gate, (905, 285))
        # создание флагов, которые выбрали игроки
        image = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id1]]}.png')
        con_image = pygame.transform.scale(image, (90, 60))
        image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id2]]}.png')
        con_image2 = pygame.transform.scale(image2, (90, 60))
        screen.blit(con_image2, (550, 510))
        screen.blit(con_image, (350, 510))
        running = True
        while running:
            pygame.time.delay(100)
            # создание счета
            pygame.draw.rect(screen, (0, 0, 0), (460, 515, 70, 50))
            self.score = fontObj.render(f'{self.goals1} : {self.goals2}', True, (255, 255, 255), None)
            self.scoreRect = self.score.get_rect(center=(495, 540))
            screen.blit(self.score, self.scoreRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == TIMEREVENT:
                    # изменение счетчика таймера
                    pygame.draw.rect(screen, (0, 0, 0), (480, 10, 40, 40))
                    self.textSurfaceObj = fontObj.render(f'{countdown}', True, (255, 255, 255), None)
                    self.textRectObj = self.textSurfaceObj.get_rect(center=(500, 30))
                    screen.blit(self.textSurfaceObj, self.textRectObj)
                    countdown -= 1
                    if countdown == -1:
                        running = False
                        EndGame(screen, id1, id2, self.goals1, self.goals2)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 5 < mouse_pos[0] < 95 and 250 < mouse_pos[1] < 494:
                        self.goals2 += 1
                    elif 905 < mouse_pos[0] < 995 and 250 < mouse_pos[1] < 494:
                        self.goals1 += 1
            pygame.display.flip()


class EndGame:
    def __init__(self, screen, id1, id2, score1, score2):
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
