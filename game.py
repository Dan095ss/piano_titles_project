from main_menu import speed
import pygame
import os
import random
from pygame.locals import *
import random

wix = 450
wiy = 750

a = random.randint(1, 2)

def msg(screen, text, color=(55, 55, 55), size=36, pos=(-1, -1)):
    if pos[0] == -1:
        pos = (screen.get_rect().centerx,pos[1])
    if pos[1] == -1:
        pos = (pos[0], screen.get_rect().centery)
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    screen.blit(text, textpos)


def load_sound(name):
    if not pygame.mixer or not pygame.mixer.get_init():
        pass
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error:
        print('Cannot load sound: %s' % name)
        raise SystemExit(str(geterror()))
    return sound


class button():
    x = 0
    y = -wiy // 5
    h = wix // 4 - 1
    l = wiy // 5
    enclick = True

    def pos(self, n):
        self.x = n * wix // 4

    def update(self, screen):
        if self.enclick:
                pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.h, self.l])
        else:
            pygame.draw.rect(screen, (128, 128, 128), [self.x, self.y, self.h, self.l])

    def click(self, ps):
        if ps[0] in range(self.x, self.x + self.h):
            if ps[1] in range(self.y, self.y + self.l):
                self.enclick = False
                return 0
        return 1
                

pygame.init()
pygame.mixer.get_init()
mutrue= load_sound("data/punch.wav")  # punch.wav
mufall = load_sound("data/boom.wav")  # boom.mp3
pygame.mixer.music.load("data/music_one.mp3")  # a.mp3
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((wix, wiy))

# a = random.randint(4)

star = pygame.image.load('data/star.png')
ed_star = pygame.transform.scale(star, (30, 30))

hearth = pygame.image.load('data/hearth.png')
ed_hearth = pygame.transform.scale(hearth, (45, 45))

map_one = [0,2,1,0,1,1,1,2,0,2,3,0,3,1,2,3,1,0,2,3,1,0,1,2,3,0,1,2,0]

b = random.randint(50, 255)
c = random.randint(100, 150)
ac = random.randint(10, 200)
aac = random.randint(0, 3)
lost = 0
time = 0
delt = 60
sb = []
score = 0

while lost == 0:
    #for i in range (10):
    for i in map_one:
        sb.append(button())
        sb[-1].pos(i)  #(random.randrange(4))
        if lost != 0:
            break

        for j in range(wiy // (5 * speed)):
            time += 1 / delt
            clock.tick(delt)

            if aac == 3:
                screen.fill((b, c, ac))
            if aac == 2:
                screen.fill((c, ac, b))
            else:
                screen.fill((ac, c, b))

            if lost != 0:
                break

            for k in range(len(sb)):
                try:
                    sb[k].y += speed
                    sb[k].update(screen)
                    # if sb[k].y > wiy + 40:
                    #   sb.remove(sb[k])
                    if sb[k].y > wiy - sb[k].l and sb[k].enclick == True:
                        lost = 1
                except:
                    pass
            for event in pygame.event.get():
                if event.type == QUIT or \
                   (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    lost = sb[score].click(pygame.mouse.get_pos())
                    if lost == 0:
                        mutrue.play()
                    else:
                        mufall.play()
                    score += 1
            msg(screen, "SCORE " + str(score), color=(0, 128, 255), pos=(-1, 30))
            if score >= 1:
                screen.blit(ed_star, (20, 10))
                # добавляем 1-ую звезду
                if score >= 2:
                    screen.blit(ed_star, (50, 10))
                    if score >= 3:
                        screen.blit(ed_star, (80, 10))
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("data/win.mp3")  # a.mp3
                        pygame.mixer.music.play(-1)
                        if aac == 3:
                            screen.fill((b, c, ac))
                        if aac == 2:
                            screen.fill((c, ac, b))
                        else:
                            screen.fill((ac, c, b))
                        msg(screen, "Ты победил!!!", color=(255, 55, 225), size=75, pos=(-1, -1))
                        pygame.display.update()
                        pygame.time.wait(4000)
                        quit()
            pygame.display.update()
    speed += 1

pygame.mixer.music.stop()
pygame.mixer.music.load("data/fail.mp3")  # a.mp3
pygame.mixer.music.play(-1)
if aac == 3:
    screen.fill((b, c, ac))
if aac == 2:
    screen.fill((c, ac, b))
else:
    screen.fill((ac, c, b))
msg(screen, "YOU LOSE ", color=(110, 128, 225), size=100, pos=(-1, -1))
msg(screen, "by Dan095SS with", color=(110, 108, 225), pos=(-1, wiy // 2 + 40))
screen.blit(ed_hearth, (350, 400))
msg(screen, "Your Score: " + str(score), color=(110, 118, 225), pos=(-1, wiy // 2 + 60))
pygame.display.update()
pygame.time.wait(4000)
# pygame.quit()
# quit()

