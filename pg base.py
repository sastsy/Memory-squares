import random
import sys
import time
import pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 700
WINDOWHEIGHT = 600
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 125
BUTTONGAPSIZE = 20
TIMEOUT = 4

#                R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED1 = (154, 0, 0)
YELLOW = (155, 155, 0)
BRIGHTYELLOW = (255, 255, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN1 = (0, 154, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE1 = (0, 0, 154)
RED2 = (155, 0, 0)
GREEN2 = (0, 155, 0)
BLUE2 = (0, 0, 155)
RED3 = (156, 0, 0)
GREEN3 = (0, 156, 0)
BLUE3 = (0, 0, 156)
DARKGRAY = (40, 40, 40)
bgColor = WHITE

XMARGIN = int((WINDOWWIDTH - (3 * BUTTONSIZE) - BUTTONGAPSIZE) / 2 - 10)
YMARGIN = int((WINDOWHEIGHT - (3 * BUTTONSIZE) - BUTTONGAPSIZE) / 2 - 10)

BLUERECT1 = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT2 = pygame.Rect(XMARGIN, YMARGIN + BUTTONGAPSIZE + BUTTONSIZE, BUTTONSIZE, BUTTONSIZE)
BLUERECT3 = pygame.Rect(XMARGIN, YMARGIN + 2 * BUTTONGAPSIZE + 2 * BUTTONSIZE, BUTTONSIZE, BUTTONSIZE)
REDRECT1 = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT2 = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE,
                       BUTTONSIZE, BUTTONSIZE)
REDRECT3 = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + 2 * BUTTONGAPSIZE + 2 * BUTTONSIZE,
                       BUTTONSIZE, BUTTONSIZE)
GREENRECT1 = pygame.Rect(XMARGIN + 2 * BUTTONSIZE + 2 * BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
GREENRECT2 = pygame.Rect(XMARGIN + 2 * BUTTONSIZE + 2 * BUTTONGAPSIZE, YMARGIN + BUTTONGAPSIZE + BUTTONSIZE,
                         BUTTONSIZE, BUTTONSIZE)
GREENRECT3 = pygame.Rect(XMARGIN + 2 * BUTTONSIZE + 2 * BUTTONGAPSIZE, YMARGIN + 2 * BUTTONGAPSIZE + 2 * BUTTONSIZE,
                         BUTTONSIZE, BUTTONSIZE)

YELLOWRECT = pygame.Rect(XMARGIN + 20, YMARGIN, 188, 188)
BLUERECT   = pygame.Rect(XMARGIN + 20 + 188 + BUTTONGAPSIZE, YMARGIN, 188, 188)
REDRECT    = pygame.Rect(XMARGIN + 20, YMARGIN + 188 + BUTTONGAPSIZE, 188, 188)
GREENRECT  = pygame.Rect(XMARGIN + 20 + 188 + BUTTONGAPSIZE, YMARGIN + 188 + BUTTONGAPSIZE,
                         188, 188)

lightmode_rect = pygame.Rect(20, YMARGIN, 75, 50)
hardmode_rect = pygame.Rect(20, YMARGIN + 70, 75, 50)

lightmode_on = True

pattern = []
currentStep = 0
lastClickTime = 0
score = 0
bestscorelight = int(open('bestscorelight.txt').read())
bestscorehard = int(open('bestscorehard.txt').read())
waitingForInput = False


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4, lightmode_on, pattern, currentStep
    global lastClickTime, score, bestscorelight, bestscorehard, waitingForInput

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Нажми на наужный квадрат с помощью мыши или клавишами Q, W, E и т.д.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Счет: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        if lightmode_on:
            bestscoreSurf = BASICFONT.render('Рекорд: ' + str(bestscorelight), 1, WHITE)
        else:
            bestscoreSurf = BASICFONT.render('Рекорд: ' + str(bestscorehard), 1, WHITE)
        bestscoreRect = bestscoreSurf.get_rect()
        bestscoreRect.topleft = (WINDOWWIDTH - 100, 40)
        DISPLAYSURF.blit(bestscoreSurf, bestscoreRect)

        lightmode_btn = pygame.font.SysFont("comicsansms", 20).render('EASY', 1, BLACK)
        lightmode_btn_rect = lightmode_btn.get_rect()
        lightmode_btn_rect.topleft = (30, YMARGIN + 10)
        DISPLAYSURF.blit(lightmode_btn, lightmode_btn_rect)

        lightmode_btn = pygame.font.SysFont("comicsansms", 20).render('HARD', 1, BLACK)
        lightmode_btn_rect = lightmode_btn.get_rect()
        lightmode_btn_rect.topleft = (30, YMARGIN + 80)
        DISPLAYSURF.blit(lightmode_btn, lightmode_btn_rect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            keys = pygame.key.get_pressed()
            if lightmode_on is False:
                if keys[pygame.K_q]:
                    clickedButton = BLUE1
                elif keys[pygame.K_w]:
                    clickedButton = RED1
                elif keys[pygame.K_e]:
                    clickedButton = GREEN1
                elif keys[pygame.K_a]:
                    clickedButton = BLUE2
                elif keys[pygame.K_s]:
                    clickedButton = RED2
                elif keys[pygame.K_d]:
                    clickedButton = GREEN2
                elif keys[pygame.K_z]:
                    clickedButton = BLUE3
                elif keys[pygame.K_x]:
                    clickedButton = RED3
                elif keys[pygame.K_c]:
                    clickedButton = GREEN3
            else:
                if keys[pygame.K_q]:
                    clickedButton = YELLOW
                elif keys[pygame.K_w]:
                    clickedButton = BLUE2
                elif keys[pygame.K_a]:
                    clickedButton = RED2
                elif keys[pygame.K_s]:
                    clickedButton = GREEN2

        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            if lightmode_on:
                pattern.append(random.choice((BLUE2, RED2, GREEN2, YELLOW)))
            else:
                pattern.append(random.choice((BLUE1, BLUE2, BLUE3, RED3, RED2, RED1, GREEN3, GREEN2, GREEN1)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1

                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    if score > bestscorelight and lightmode_on or score > bestscorehard and lightmode_on is False:
                        if lightmode_on:
                            bestscorelight = score
                            fin = open('bestscorelight.txt', 'w')
                            fin.write(str(bestscorelight))
                        else:
                            bestscorehard = score
                            fin = open('bestscorehard.txt', 'w')
                            fin.write(str(bestscorehard))
                        fin.close()
                    waitingForInput = False
                    currentStep = 0

            elif clickedButton and clickedButton != pattern[currentStep]:
                gameOverAnimation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def flashButtonAnimation(color, animationSpeed=50):
    if color == BLUE1 or color == BLUE2 or color == BLUE3:
        sound = BEEP1
        flashColor = BRIGHTBLUE
        if color == BLUE1:
            rectangle = BLUERECT1
        elif color == BLUE2:
            if lightmode_on:
                rectangle = BLUERECT
            else:
                rectangle = BLUERECT2
        elif color == BLUE3:
            rectangle = BLUERECT3
    elif color == RED1 or color == RED2 or color == RED3:
        sound = BEEP2
        flashColor = BRIGHTRED
        if color == RED1:
            rectangle = REDRECT1
        elif color == RED2:
            if lightmode_on:
                rectangle = REDRECT
            else:
                rectangle = REDRECT2
        elif color == RED3:
            rectangle = REDRECT3
    elif color == GREEN1 or color == GREEN2 or color == GREEN3:
        sound = BEEP3
        flashColor = BRIGHTGREEN
        if color == GREEN1:
            rectangle = GREENRECT1
        elif color == GREEN2:
            if lightmode_on:
                rectangle = GREENRECT
            else:
                rectangle = GREENRECT2
        elif color == GREEN3:
            rectangle = GREENRECT3
    elif color == YELLOW:
        flashColor = BRIGHTYELLOW
        sound = BEEP4
        rectangle = YELLOWRECT

    origSurf = DISPLAYSURF.copy()
    if lightmode_on:
        flashSurf = pygame.Surface((188, 188))
    else:
        flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))


def drawButtons():
    if lightmode_on:
        pygame.draw.rect(DISPLAYSURF, BRIGHTGREEN, lightmode_rect)
        pygame.draw.rect(DISPLAYSURF, WHITE, hardmode_rect)
        pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
        pygame.draw.rect(DISPLAYSURF, BLUE2, BLUERECT)
        pygame.draw.rect(DISPLAYSURF, RED2, REDRECT)
        pygame.draw.rect(DISPLAYSURF, GREEN2, GREENRECT)
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE, lightmode_rect)
        pygame.draw.rect(DISPLAYSURF, BRIGHTGREEN, hardmode_rect)
        pygame.draw.rect(DISPLAYSURF, BLUE1, BLUERECT1)
        pygame.draw.rect(DISPLAYSURF, RED1, REDRECT1)
        pygame.draw.rect(DISPLAYSURF, GREEN1, GREENRECT1)
        pygame.draw.rect(DISPLAYSURF, BLUE2, BLUERECT2)
        pygame.draw.rect(DISPLAYSURF, RED2, REDRECT2)
        pygame.draw.rect(DISPLAYSURF, GREEN2, GREENRECT2)
        pygame.draw.rect(DISPLAYSURF, BLUE3, BLUERECT3)
        pygame.draw.rect(DISPLAYSURF, RED3, REDRECT3)
        pygame.draw.rect(DISPLAYSURF, GREEN3, GREENRECT3)


def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getButtonClicked(x, y):
    global lightmode_on, pattern, currentStep, waitingForInput, score
    if lightmode_on:
        if YELLOWRECT.collidepoint((x, y)):
            lastClickTime
            return YELLOW
        elif BLUERECT.collidepoint((x, y)):
            return BLUE2
        elif REDRECT.collidepoint((x, y)):
            return RED2
        elif GREENRECT.collidepoint((x, y)):
            return GREEN2
    else:
        if BLUERECT1.collidepoint((x, y)):
            return BLUE1
        elif BLUERECT2.collidepoint((x, y)):
            return BLUE2
        elif BLUERECT3.collidepoint((x, y)):
            return BLUE3
        elif REDRECT1.collidepoint((x, y)):
            return RED1
        elif REDRECT2.collidepoint((x, y)):
            return RED2
        elif REDRECT3.collidepoint((x, y)):
            return RED3
        elif GREENRECT1.collidepoint((x, y)):
            return GREEN1
        elif GREENRECT2.collidepoint((x, y)):
            return GREEN2
        elif GREENRECT3.collidepoint((x, y)):
            return GREEN3
    if lightmode_rect.collidepoint((x, y)):
        if lightmode_on is not True:
            lightmode_on = True
            BEEP1.play()
            BEEP2.play()
            BEEP3.play()
            BEEP4.play()
            pattern = []
            currentStep = 0
            waitingForInput = False
            score = 0
            changeBackgroundAnimation()
            pygame.time.wait(1000)
    if hardmode_rect.collidepoint((x, y)):
        if lightmode_on:
            BEEP1.play()
            BEEP2.play()
            BEEP3.play()
            BEEP4.play()
            lightmode_on = False
            pattern = []
            currentStep = 0
            waitingForInput = False
            score = 0
            changeBackgroundAnimation()
            pygame.time.wait(1000)
    return None


if __name__ == '__main__':
    main()