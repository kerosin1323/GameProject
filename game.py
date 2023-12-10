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
        countdown = 90
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        self.goals1 = 0
        self.goals2 = 0
        while True:
            pygame.time.delay(100)
            # создание флагов, которые выбрали игроки
            image = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id1]]}.png')
            con_image = pygame.transform.scale(image, (90, 60))
            image2 = pygame.image.load(f'image/flags/{COUNTRIES_FLAG[COUNTRY[id2]]}.png')
            con_image2 = pygame.transform.scale(image2, (90, 60))
            screen.blit(con_image2, (550, 510))
            screen.blit(con_image, (350, 510))
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
                        EndGame()
            pygame.display.flip()


class EndGame:
    pass
