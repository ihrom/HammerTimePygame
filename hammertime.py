# Hammer Time
# by Ivan H.
# May 21, 2014

import pygame, sys, random
from pygame.locals import *

TEXTCOLOR = (255,255,255)
BACKGROUNDCOLOR = (0,0,0)

def presstostart():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return

pygame.init()

gameClock = pygame.time.Clock()
randomClock = pygame.time.Clock()

hammerImage = pygame.image.load('hammer1.png')
hammerRect = hammerImage.get_rect()
squirrelImage = pygame.image.load('squirrel.png')
squirrelRect = squirrelImage.get_rect()
forestImage = pygame.image.load('forest1.png')
forestRect = forestImage.get_rect()

gameSurface = pygame.display.set_mode((400,400))
pygame.display.set_caption('Hammer Time')
pygame.mouse.set_visible(False)

gamefont = pygame.font.SysFont(None, 48)

gametitleobj = gamefont.render('Hammer Time', 1, TEXTCOLOR)
gametitlerect = gametitleobj.get_rect()
gametitlerect.topleft = ((400/3)-50, (400/3))
gameSurface.blit(gametitleobj, gametitlerect)

gamestartobj = gamefont.render('Press any key to start.',1, TEXTCOLOR)
gamestartrect = gamestartobj.get_rect()
gamestartrect.topleft = ((400/3)-100, (400/3)+50)
gameSurface.blit(gamestartobj, gamestartrect)

pygame.display.update()
presstostart()

while True:
    missedsquirrels = 0
    hitsquirrels = 0
    hammerRect.topleft = (400/2, 400/2)
    squirrelRect.topleft = (random.randint(0, 400-40), random.randint(0,400-40))
    moveLeft = moveRight = moveUp = moveDown = False
    randomTime = random.randint(2000,3000)
    randomTimer = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                hammerRect.move_ip(event.pos[0] - hammerRect.centerx, event.pos[1] - hammerRect.centery)

        if moveUp and hammerRect.top > 0:
            hammerRect.move_ip(0,-5)
        if moveRight and hammerRect.right < 400:
            hammerRect.move_ip(5,0)
        if moveDown and hammerRect.bottom < 400:
            hammerRect.move_ip(0,5)
        if moveLeft and hammerRect.left > 0:
            hammerRect.move_ip(-5,0)

        pygame.mouse.set_pos(hammerRect.centerx, hammerRect.centery)

        #gameSurface.fill(forestImage)
        forestRect.topleft = (0,0)
        gameSurface.blit(forestImage, forestRect)

        gamescoremissedobj = gamefont.render('Missed = %s' % (missedsquirrels), 1, TEXTCOLOR)
        gamescoremissedrect = gamescoremissedobj.get_rect()
        gamescoremissedrect.topleft = (10,0)
        gameSurface.blit(gamescoremissedobj, gamescoremissedrect)

        gamescorehitobj = gamefont.render('Hit = %s' % (hitsquirrels), 1, TEXTCOLOR)
        gamescorehitrect = gamescorehitobj.get_rect()
        gamescorehitrect.topleft = (10,40)
        gameSurface.blit(gamescorehitobj, gamescorehitrect)

        gameSurface.blit(hammerImage, hammerRect)
        gameSurface.blit(squirrelImage, squirrelRect)

        pygame.display.update()

        if hammerRect.colliderect(squirrelRect):
            hitsquirrels += 1
            squirrelRect.topleft = (random.randint(0, 400-40), random.randint(0,400-40))
            randomTimer = 0
            randomTime = random.randint(500,1000)
            gameSurface.blit(squirrelImage, squirrelRect)
            pygame.display.update()
                                 
        if randomTimer > randomTime:
            missedsquirrels += 1
            squirrelRect.topleft = (random.randint(0, 400-40), random.randint(0,400-40))
            randomTimer = 0
            randomTime = random.randint(500,1000)
            gameSurface.blit(squirrelImage, squirrelRect)
            pygame.display.update()

        if missedsquirrels == 6:
            break

        randomTimer += randomClock.tick()
        gameClock.tick(40)

    #gameSurface.fill(BACKGROUNDCOLOR)    
    

    gamescoremissedobj = gamefont.render('Missed = %s' % (missedsquirrels), 1, TEXTCOLOR)
    gamescoremissedrect = gamescoremissedobj.get_rect()
    gamescoremissedrect.topleft = (10,0)
    gameSurface.blit(gamescoremissedobj, gamescoremissedrect)

    gamescorehitobj = gamefont.render('Hit = %s' % (hitsquirrels), 1, TEXTCOLOR)
    gamescorehitrect = gamescorehitobj.get_rect()
    gamescorehitrect.topleft = (10,40)
    gameSurface.blit(gamescorehitobj, gamescorehitrect)

    gameoverobj = gamefont.render('GAME OVER', 1, TEXTCOLOR)
    gameoverrect = gametitleobj.get_rect()
    gameoverrect.topleft = ((400/4), (400/3))
    gameSurface.blit(gameoverobj, gameoverrect)

    gamenewobj = gamefont.render('Press any key to',1, TEXTCOLOR)
    gamenewrect = gamestartobj.get_rect()
    gamenewrect.topleft = ((400/4)-30, (400/3)+50)
    gameSurface.blit(gamenewobj, gamenewrect)

    gamenewobj = gamefont.render('play again.',1, TEXTCOLOR)
    gamenewrect = gamestartobj.get_rect()
    gamenewrect.topleft = ((400/4)+10, (400/3)+100)
    gameSurface.blit(gamenewobj, gamenewrect)

    pygame.display.update()
    presstostart()


