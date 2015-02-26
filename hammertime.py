import pygame, random
from pygame.locals import *

#--- Global constants ---
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

#--- Classes ---
class Background(pygame.sprite.Sprite):
    """This class represents the screen background"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("forest1.png")

class Startgame(object):
    """This class begins intro window"""
    
    def __init__(self):
        """Add some kind of intro screen here:"""
        #pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("forest1.png")

    def check_start(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                return True
        return False

    def start_window(self,screen):
        """Prepare player to play"""
        screen.fill(BLACK)

        titlefont = pygame.font.SysFont('stencil', 48)
        titletext = titlefont.render("Hammer Time", True, WHITE)
        titletext.set_alpha(100)
        screen.blit(titletext,[(40),(100)])

        startfont = pygame.font.SysFont(None, 48)
        starttext = startfont.render("Click to start", True, WHITE)
        screen.blit(starttext,[(100),(200)])


class SpriteSheet(object):
    """Grab images out of sprite sheet."""
    sprite_sheet = None

    def __init__(self, file_name):
        """Constructor to load file"""
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """Grab single image from sheet"""
        #Create a new blank image
        image = pygame.Surface([width, height]).convert()

        #Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))

        #Set transparent color
        image.set_colorkey((160,40,200))

        return image    
    
class Hammer(pygame.sprite.Sprite):
    """ This class represents the hammer """
    swing = False
    
    def __init__(self):
        """ Sprite constructor """
        self.swing = False

        #Call parent constructor
        super().__init__()

        sprite_sheet = SpriteSheet("squirrel_hammerSpriteSheet1.png")
        #Load the image
        self.image = sprite_sheet.get_image(18,20,27,22)
        
        #Get position of image with rect()
        self.rect = self.image.get_rect()

        #print("A hammer is created!")

    def update_pos(self):
        """ Update the hammer location """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def swing_hammer(self):
        """Check if hammer was swung"""
        mousebuttons = pygame.mouse.get_pressed()
        self.swing = mousebuttons[0]
        

class Squirrel(pygame.sprite.Sprite):
    """ This class represents the squirrel """
    squirrel_frames = []
        
    def __init__(self):
        """ Sprite constructor """
        #Call parent's constructor
        super().__init__()

        sprite_sheet = SpriteSheet("squirrel_hammerSpriteSheet1.png")
        #Grab images
        image = sprite_sheet.get_image(133,13,52,39)
        self.squirrel_frames.append(image)
        image = sprite_sheet.get_image(133,76,52,39)
        self.squirrel_frames.append(image)
        image = sprite_sheet.get_image(197,13,52,39)
        self.squirrel_frames.append(image)
        image = sprite_sheet.get_image(197,76,52,39)
        self.squirrel_frames.append(image)

        self.image = self.squirrel_frames[0]

        self.rect = self.image.get_rect()

        #print("A squirrel is created!")

    def reset_pos(self):
        """ Update the squirrel image and location """
        self.image = self.squirrel_frames[random.randrange(0,3)]
        self.rect.x = random.randrange(0,380)
        self.rect.y = random.randrange(0,380)
        
        
class Game(object):
    """ This is the Game class object """

    #--- Class attributes ---
    # Sprites
    hammer = None
    squirrel = None

    # Initialize game settings
    game_over = False
    missed = 0
    hit = 0
    squirrel_clock = None
    timer = 0
    setTime = 1000
    rect_y = -400

    #--- Class methods ---
    # Set up game
    def __init__(self):
        """ This method initializes game """
        self.game_over = False
        self.missed = 0
        self.hit = 0
        self.squirrel_clock = pygame.time.Clock()
        self.timer = 0
        self.setTime = random.randint(5000,6000)
        self.rect_y = -400

        #Create background
        self.background = Background()
    
        #Create hammer
        self.hammer = Hammer()

        #Create squirrel
        self.squirrel = Squirrel()
        self.squirrel.reset_pos()
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
                if self.game_over:
                    self.__init__()
        return False

    def beginfader(self,screen,mainclock):
        """Creates fading displays"""
        fade_counter = 0
        while fade_counter < 30:
            self.background.image.set_alpha(30)
            screen.blit(self.background.image,[0,0])
            fade_counter += 1
            pygame.display.flip()
            mainclock.tick(10)

    def game_action(self):
        """ This methods runs for each frame loop """

        if not self.game_over:
            self.hammer.update_pos()
            self.hammer.swing_hammer()
        
            # Check collision
            if self.hammer.rect.colliderect(self.squirrel.rect) and self.hammer.swing == True:
                self.hit += 1
                self.timer = 0
                self.setTime = random.randint(500,1000)
                self.squirrel.reset_pos()
                #print("Ouch!",self.hit)
                                 
            if self.timer > self.setTime:
                self.missed += 1
                self.timer = 0
                self.setTime = random.randint(500,1000)
                self.squirrel.reset_pos()
                #print("Missed me!",self.missed)

            if self.missed == 6:
                self.game_over = True

            self.timer += self.squirrel_clock.tick()

    def game_screen(self,screen):
        """ Update the screen every loop """
        self.background.image.set_alpha(None)     #A value of 10 makes trails with hammer!!!
        screen.blit(self.background.image,[0,0])
        
        if self.game_over:
            #screen.fill(BLACK)
            if self.rect_y < 0:
                pygame.draw.rect(screen, BLACK, [0,self.rect_y,400,400])
                self.rect_y += 2

            if self.rect_y == 0:
                screen.fill(BLACK)            
                endfont = pygame.font.SysFont(None, 48)
                text1 = endfont.render("Game Over", True, WHITE)
                screen.blit(text1,[(400/4), (400/3)])
                text2 = endfont.render("Press any key", True, WHITE)
                screen.blit(text2,[(400/4)-30, (400/3)+50])
                text3 = endfont.render("to play again", True, WHITE)
                screen.blit(text3,[(400/4)+10, (400/3)+100])            

        if not self.game_over:
            datafont = pygame.font.SysFont(None, 38)
            missed_text = datafont.render("missed = %s" %(self.missed),True,WHITE)
            screen.blit(missed_text,[10,10])
            hit_text = datafont.render("hit = %s" %(self.hit),True,WHITE)
            screen.blit(hit_text,[10,48])
            screen.blit(self.hammer.image,self.hammer.rect)
            screen.blit(self.squirrel.image,self.squirrel.rect)
        
            
def main():
    """ Main program """
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Hammer Time")
    
    done = False
    clicked = False

    gameclock = pygame.time.Clock()

    start_game = Startgame()
    
    while not clicked:
        clicked = start_game.check_start()
        start_game.start_window(screen)
        pygame.display.flip()
        gameclock.tick(60)

    pygame.mouse.set_visible(False)
    game = Game()
    game.beginfader(screen,gameclock)
    
    while not done:
        done = game.process_events()
        game.game_action()
        game.game_screen(screen)
        pygame.display.flip()
        gameclock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

        
        
        

        
