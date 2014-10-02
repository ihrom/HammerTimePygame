# Hammer Time
# by Ivan Hromada and Derek Uskert

import pygame, sys, random
from pygame.locals import *

TEXTCOLOR = (255,255,255)
GAMEFPS = 30
GAMEWINDOW = (400,400)   #Must be same size as background image.

pygame.init()

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
            
def main():
    gameClock = pygame.time.Clock()
    randomClock = pygame.time.Clock()

    hammerImage = pygame.image.load('hammer1.png')
    hammerImage.set_colorkey((255,255,255))
    hammerRect = hammerImage.get_rect()
    squirrelImage = pygame.image.load('squirrel.png')
    squirrelImage.set_colorkey((255,255,255))
    squirrelRect = squirrelImage.get_rect()
    forestImage = pygame.image.load('forest1.png')
    forestRect = forestImage.get_rect()

    gameSurface = pygame.display.set_mode(GAMEWINDOW)
    pygame.display.set_caption('Hammer Time')
    pygame.mouse.set_visible(False)

    gamefont = pygame.font.SysFont(None, 48)

    gametitleobj = gamefont.render('Hammer Time', 1, TEXTCOLOR)
    gametitlerect = gametitleobj.get_rect()
    gametitlerect.topleft = ((GAMEWINDOW[0]/3)-50, (GAMEWINDOW[1]/3))
    gameSurface.blit(gametitleobj, gametitlerect)

    gamestartobj = gamefont.render('Press any key to start.',1, TEXTCOLOR)
    gamestartrect = gamestartobj.get_rect()
    gamestartrect.topleft = ((GAMEWINDOW[0]/3)-100, (GAMEWINDOW[1]/3)+50)
    gameSurface.blit(gamestartobj, gamestartrect)

    pygame.display.update()
    presstostart()

    while True:        
        missedsquirrels = 0
        hitsquirrels = 0
        hammerRect.topleft = (GAMEWINDOW[0]/2, GAMEWINDOW[1]/2)
        squirrelRect.topleft = (random.randint(0, GAMEWINDOW[0]-40), random.randint(0,GAMEWINDOW[1]-40))
        moveLeft = moveRight = moveUp = moveDown = False
        randomTime = random.randint(2000,3000)
        randomTimer = 0
    
        while True:
            gameClock.tick(GAMEFPS)
            swing = 0

            forestRect.topleft = (0,0)
            gameSurface.blit(forestImage, forestRect)
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == MOUSEMOTION:
                    hammerRect.move_ip(event.pos[0] - hammerRect.centerx, event.pos[1] - hammerRect.centery)
                if event.type == MOUSEBUTTONDOWN:
                    swing = event.button
                
            pygame.mouse.set_pos(hammerRect.centerx, hammerRect.centery)

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

            pygame.display.flip()

            if hammerRect.colliderect(squirrelRect) and swing == 1:
                hitsquirrels += 1
                squirrelRect.topleft = (random.randint(0, GAMEWINDOW[0]-40), random.randint(0,GAMEWINDOW[1]-40))
                randomTimer = 0
                randomTime = random.randint(500,1000)
                gameSurface.blit(squirrelImage, squirrelRect)
                pygame.display.update()
                                 
            if randomTimer > randomTime:
                missedsquirrels += 1
                squirrelRect.topleft = (random.randint(0, GAMEWINDOW[0]-40), random.randint(0,GAMEWINDOW[1]-40))
                randomTimer = 0
                randomTime = random.randint(500,1000)
                gameSurface.blit(squirrelImage, squirrelRect)
                pygame.display.update()

            if missedsquirrels == 6:
                break

            randomTimer += randomClock.tick()
        

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
        gameoverrect.topleft = ((GAMEWINDOW[0]/4), (GAMEWINDOW[1]/3))
        gameSurface.blit(gameoverobj, gameoverrect)

        gamenewobj = gamefont.render('Press any key to',1, TEXTCOLOR)
        gamenewrect = gamestartobj.get_rect()
        gamenewrect.topleft = ((GAMEWINDOW[0]/4)-30, (GAMEWINDOW[1]/3)+50)
        gameSurface.blit(gamenewobj, gamenewrect)

        gamenewobj = gamefont.render('play again.',1, TEXTCOLOR)
        gamenewrect = gamestartobj.get_rect()
        gamenewrect.topleft = ((GAMEWINDOW[0]/4)+10, (GAMEWINDOW[1]/3)+100)
        gameSurface.blit(gamenewobj, gamenewrect)

        pygame.display.flip()
        presstostart()

if __name__ == "__main__":
    main()
    


