import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox
import sys
from time import sleep

pygame.init()
life_up = pygame.mixer.Sound("./sounds/life_up.mp3")
life_down = pygame.mixer.Sound("./sounds/life_down.mp3")
width = 500
height = 500

cols = 25
rows = 20


class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake():
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    # 길이 줄이는 함수.
    def removeCube(self):
        self.body.pop()

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,0,0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    # 아이템 게임 보드에 그리기
    item.draw(win)
    obstacle.draw(win)
    draw_score()
    if gameover == 1:
        draw_gameover()
        pygame.display.update()
        sleep(1)
    else:
        pygame.display.update() #화면을 업데이트
    



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)

def draw_score():
    YELLOW = (255, 255, 0)
    small_font = pygame.font.SysFont(None, 36)
    score_image = small_font.render('Point {}'.format(score), True, YELLOW)
    win.blit(score_image, (15, 15)) # blit() 통해 게임판에 출력
    
def draw_gameover():
    RED = (255, 0, 0)
    large_font = pygame.font.SysFont(None, 72)
    gameover_image = large_font.render('Game Over', True, RED)
    win.blit(gameover_image, (width // 2 - gameover_image.get_width() // 2, height // 2 - gameover_image.get_height() // 2))

#Start Menu
def title():
    white = (255, 255, 255)
    pygame.init()
    clock = pygame.time.Clock()
    playing = True
    while playing:
        SCREEN = pygame.display.set_mode( (500, 500) )
        pygame.display.set_caption("pygame test")
        SCREEN.fill((0, 0, 0))
        myFont = pygame.font.SysFont("arial", 30, True, False)
        myFont2 = pygame.font.SysFont("arial", 15, True, False)
        title = myFont.render("Snake Game", True, white)
        text = title.get_rect()
        text.centerx = round(width / 2)
        text.y = 50
        start = myFont.render("Y : Start", True, white)
        text1 = title.get_rect()
        text1.centerx = round(width / 4 - 15)
        text1.y = 150
        exit = myFont.render("ESC : Exit", True, white)
        text2 = title.get_rect()
        text2.centerx = round(width / 4 - 15)
        text2.y = 200
        help = myFont.render("Rule", True, white)
        help2 = myFont2.render("Green : Score + 1, \n Lenth +1 Blue : Game over, White : Lenth - 1", True, white)
        text3 = title.get_rect()
        text4 = title.get_rect()
        text4.centerx = round(width / 4 - 15)
        text3.centerx = round(width / 4 - 15)
        text3.y = 350
        text4.y = 400
        SCREEN.blit(title, text)
        SCREEN.blit(start, text1)
        SCREEN.blit(exit, text2)
        SCREEN.blit(help, text3)
        SCREEN.blit(help2, text4)

        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
             if event.type == pygame.KEYDOWN:
                 if event.key == ord('y'):
                    playing = False
                    break
                 if event.key == pygame.K_ESCAPE:
                    playing = False
                    pygame.quit()
                    sys.exit(0)
             if event.type == pygame.QUIT:
                 playing = False
                 pygame.quit()
                 sys.exit(0)

def main():
    title()
    global s, snack, win, item, obstacle, gameover, score
    score = 0
    win = pygame.display.set_mode((width,height))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows,s), color=(0,255,0))
    # 아이템 객체 만들기
    # 색상 : 흰색 (변경가능)
    item = cube(randomSnack(rows, s), color=(255,255,255))
    
    # 장애물 객체 만들기
    # 색상 : 파란색
    obstacle = cube(randomSnack(rows, s), color=(0,0,255))
    gameover = 0
    flag = True
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", score)
            gameover = 1
            s.reset((10, 10))
            score = 0
            life_down.play()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(0,255,0))
            item = cube(randomSnack(rows, s), color=(255,255,255))
            score += 1
            life_up.play()

        # 아이템을 먹으면 길이 줄이기.
        # 만약 길이가 1이라면 길이를 줄이지 않고 위치만 바꿈.
        if s.body[0].pos == item.pos:
            if len(s.body) > 1:
                s.removeCube()
                item = cube(randomSnack(rows, s), color=(255,255,255))
            item = cube(randomSnack(rows, s), color=(255,255,255))
            life_up.play()
        

        # 장애물에 닿았을 때 게임오버
        if s.body[0].pos == obstacle.pos:
            print("Score:", score)
            gameover = 1
            s.reset((10,10))
            life_down.play()
            score = 0

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("Score:", score)
                gameover = 1
                s.reset((10,10))
                life_down.play()
                score = 0
                break

                    
        redrawWindow()
        gameover = 0

main()
