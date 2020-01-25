import pygame, os, random
from pygame.locals import *
import random

wix=450
wiy=750

def msg (screen, text, color = (55, 55, 55), size = 36, pos = (-1, -1)):
    if pos[0] == -1:pos = (screen.get_rect().centerx,pos[1])
    if pos[1] == -1:pos = (pos[0], screen.get_rect().centery)
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery= pos[1]
    screen.blit(text, textpos)
def load_sound(name):
    if not pygame.mixer or not pygame.mixer.get_init():
        pass
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error:
        print ('Cannot load sound: %s' % name)
        raise SystemExit(str(geterror()))
    return sound


class button():
    x = 0
    y =- wiy // 5
    h = wix // 4 - 1
    l= wiy // 5
    enclick = True
    def pos(self,n):
        self.x = n * wix // 4
    def update(self,screen):
        if self.enclick :pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.h, self.l])
        else :pygame.draw.rect(screen, (180, 180, 180),[self.x, self.y, self.h, self.l])
    def click(self,ps):
        if ps[0] in range(self.x, self.x + self.h):
            if ps[1] in range (self.y, self.y + self.l):
                self.enclick = False
                return 0
        return 1
                

pygame.init()
pygame.mixer.get_init()
mutrue= load_sound("data/punch.wav") # punch.wav
mufall = load_sound("data/boom.wav") # boom.mp3
pygame.mixer.music.load("data/a.mp3") # a.mp3
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((wix,wiy))

a = random.randint(4)

map_one = [0,2,1,0,1,1,1,2,0,2,3,0,3,1,2,3,1,0,2,3,1,0,1,2,3,0,1,2,0]

lost=0
time=0
delt=60
sb=[]
speed=8
score=0

while lost == 0:
    #for i in range (10):
    for i in map_one:
        sb.append(button())
        sb[-1].pos(i)#(random.randrange(4))
        if lost!=0 : break
        for j in range(wiy //(5 * speed)):
            time += 1 / delt
            clock.tick(delt)
            screen.fill((224, 224, 255))
            if lost != 0 : break
            for k in range(len(sb)) :
                try:
                    sb[k].y += speed
                    sb[k].update(screen)
                     # if sb[k].y > wiy + 40 : sb.remove(sb[k])
                    if sb[k].y >wiy-sb[k].l and sb[k].enclick == True : lost=1
                except : pass
            for event in pygame.event.get():
                if event.type == QUIT or \
                   (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    lost=sb[score].click(pygame.mouse.get_pos())
                    if lost == 0:mutrue.play()
                    else :mufall.play()
                    score += 1
            msg(screen, "SCORE " + str(score), color=(0, 128, 255), pos = (-1, 30))
            if score >= 50:
                pass # добавляем 1-ую звезду
                if score >= 100:
                    pass # добавляем вторую звезду
                    if score >= 150:
                        pass # меняем цвет всех клавиш на золотой + добавляем 3-ю звезду
    
            pygame.display.update()
    speed += 1
pygame.mixer.music.stop()
msg(screen, "YOU LOSE ", color=(110, 128, 225), size = 100, pos=(-1, -1))
msg(screen, "by Dan095SS with LOVE", color=(110, 108, 225), pos=(-1, wiy // 2 + 40))
msg(screen, "Your Score: " + str(score), color=(110, 118, 225), pos=(-1, wiy // 2 + 60))
pygame.display.update()
pygame.time.wait(4000)
pygame.quit()
quit()
