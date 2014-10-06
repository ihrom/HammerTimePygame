######################################
########   Hammer Time   #############
## by Ivan Hromada and Derek Uskert ##
######################################

#Import standard libraries
import pygame, sys, random
#Import constants like KEYDOWN, MOUSEMOTION, etc. 
from pygame.locals import *

#Set some game constants
TEXTCOLOR = (255,255,255)
GAMEFPS = 30

#Always need to initialize pygame
pygame.init()

#Prepare game window variable and caption
gameSurface = pygame.display.set_mode((400,400))
pygame.display.set_caption('Hammer Time')

#Hide mouse over screen
pygame.mouse.set_visible(False)

#Initialize game speed variable(FPS)
#Initialize random clock variable
gameClock = pygame.time.Clock()
randomClock = pygame.time.Clock()

#Want to prepare the sound files here.


#Set location of background image and text 
background_position = [0,0]
gametitle_position = [(400/3)-50,(400/3)]
gamestart_position = [(400/3)-100,(400/3)+50]

#Load images and properties
hammerImage = pygame.image.load('hammer1.png')
hammerImage.set_colorkey((255,255,255))
hammerRect = hammerImage.get_rect()
squirrelImage = pygame.image.load('squirrel.png')
squirrelImage.set_colorkey((255,255,255))
squirrelRect = squirrelImage.get_rect()
#Background image must be same size as window
backgroundImage = pygame.image.load('forest1.png')

#Define function to start game with KEYDOWN
#Exits game if esc or close is chosen
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

#Initialize game font
gamefont = pygame.font.SysFont(None, 48)

#Put title and text on game window
gametitleobj = gamefont.render('Hammer Time', 1, TEXTCOLOR)
gameSurface.blit(gametitleobj, gametitle_position)
gamestartobj = gamefont.render('Press any key to start.', 1, TEXTCOLOR)
gameSurface.blit(gamestartobj, gamestart_position)

#Display window on screen
pygame.display.update()

presstostart()

#Define main game loop            
def main():
    done = False

    while not done:        
        missedsquirrels = 0
        hitsquirrels = 0
        
        hammerRect.topleft = (400/2, 400/2)
        squirrelRect.topleft = (random.randint(0, 400-40), random.randint(0,400-40))
        randomTime = random.randint(2000,3000)
        randomTimer = 0
    
        while not done:
            swing = 0
            gameSurface.blit(backgroundImage, background_position)
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True

                if event.type == MOUSEMOTION:
                    hammerRect.move_ip(event.pos[0] - hammerRect.centerx, event.pos[1] - hammerRect.centery)
                if event.type == MOUSEBUTTONDOWN:
                    swing = event.button

            #### Here is another way to control player with mouse:
            #### Get the current mouse position. This returns the position as a list of two numbers.
            #player_position = pygame.mouse.get_pos()
            #x = player_position[0]
            #y = player_position[1]
            #screen.blit(player_image, [x, y])
                
            pygame.mouse.set_pos(hammerRect.centerx, hammerRect.centery)

            gamescoremissedobj = gamefont.render('Missed = %s' % (missedsquirrels), 1, TEXTCOLOR)
            gameSurface.blit(gamescoremissedobj, (10,0))

            gamescorehitobj = gamefont.render('Hit = %s' % (hitsquirrels), 1, TEXTCOLOR)
            gameSurface.blit(gamescorehitobj, (10,40))

            gameSurface.blit(hammerImage, hammerRect)
            gameSurface.blit(squirrelImage, squirrelRect)

            pygame.display.flip()

            if hammerRect.colliderect(squirrelRect) and swing == 1:
                hitsquirrels += 1
                squirrelRect.topleft = (random.randint(0,400-40), random.randint(0,400-40))
                randomTimer = 0
                randomTime = random.randint(500,1000)
                gameSurface.blit(squirrelImage, squirrelRect)
                pygame.display.update()
                                 
            if randomTimer > randomTime:
                missedsquirrels += 1
                squirrelRect.topleft = (random.randint(0,400-40), random.randint(0,400-40))
                randomTimer = 0
                randomTime = random.randint(500,1000)
                gameSurface.blit(squirrelImage, squirrelRect)
                pygame.display.update()

            if missedsquirrels == 6:
                break

            randomTimer += randomClock.tick()
            gameClock.tick(GAMEFPS)
        

        gamescoremissedobj = gamefont.render('Missed = %s' % (missedsquirrels), 1, TEXTCOLOR) 
        gameSurface.blit(gamescoremissedobj, (10,0))

        gamescorehitobj = gamefont.render('Hit = %s' % (hitsquirrels), 1, TEXTCOLOR)
        gameSurface.blit(gamescorehitobj, (10,40))

        gameoverobj = gamefont.render('GAME OVER', 1, TEXTCOLOR)
        gameSurface.blit(gameoverobj, ((400/4), (400/3)))

        gamenewobj = gamefont.render('Press any key to',1, TEXTCOLOR)
        gameSurface.blit(gamenewobj, ((400/4)-30, (400/3)+50))

        gamenewobj = gamefont.render('play again.',1, TEXTCOLOR) 
        gameSurface.blit(gamenewobj, ((400/4)+10, (400/3)+100))

        pygame.display.flip()
        presstostart()

#Run game loop
if __name__ == "__main__":
    main()

pygame.quit()
sys.exit()
    


