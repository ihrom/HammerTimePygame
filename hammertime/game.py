import pygame, random
from pygame.locals import *
from .loader import load_image, load_sound
from .getscore import *

#--- Global constants ---
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

#--- Classes ---
class Background(pygame.sprite.Sprite):
    """This class represents the screen background"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('forest2')

class Startgame(object):
    """This class begins intro window"""
    def __init__(self):
        """Add some kind of intro screen here:"""
        #pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("forest1.png")

    def check_start(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                return True
        return False

    def start_window(self,screen,score):
        """Prepare player to play"""
        screen.fill(BLACK)

        titlefont = pygame.font.SysFont('stencil', 48)
        titletext = titlefont.render("Hammer Time", True, WHITE)
        screen.blit(titletext,[75,(SCREEN_HEIGHT/4)])

        startfont0 = pygame.font.SysFont('timesnewroman', 20)
        scoretext = startfont0.render("(High Score = %s)" %(score),True,WHITE)
        screen.blit(scoretext,[165,(SCREEN_HEIGHT/4 + 50)])

        startfont1 = pygame.font.SysFont('timesnewroman', 30)
        starttext = startfont1.render("Click to start", True, WHITE)
        screen.blit(starttext,[160,(SCREEN_HEIGHT/4 + 200)])


class SpriteSheet(object):
    """Grab images out of sprite sheet."""
    sprite_sheet = None

    def __init__(self, file_name):
        """Constructor to load file"""
        self.sprite_sheet = load_image(file_name)

    def get_image(self, x, y, width, height):
        """Grab single image from sheet"""
        #Create a new blank image
        image = pygame.Surface([width, height])

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

        sprite_sheet = SpriteSheet('squirrel_hammerSpriteSheet1')
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

        sprite_sheet = SpriteSheet('squirrel_hammerSpriteSheet1')
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
        self.rect.x = random.randrange(0,350)
        self.rect.y = random.randrange(0,300)
        
        
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
    rect_y = -480

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
        self.rect_y = -480

        #Create background
        self.background = Background()
    
        #Create hammer
        self.hammer = Hammer()

        #Create squirrel
        self.squirrel = Squirrel()
        self.squirrel.reset_pos()

        pygame.mouse.set_visible(False)
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == MOUSEBUTTONDOWN and self.rect_y == 0:
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
            mainclock.tick(15)

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

    def game_screen(self,screen,score):
        """ Update the screen every loop """
        self.background.image.set_alpha(None)     #A value of 10 makes trails with hammer!!!
        screen.blit(self.background.image,[0,0])
        #pygame.draw.rect(screen, BLACK, [0,360,400,50])
        
        if self.game_over:
            #screen.fill(BLACK)
            if self.hit > score:
                save_high_score(self.hit)
                
            if self.rect_y < 0:
                pygame.draw.rect(screen, BLACK, [0,self.rect_y,480,480])
                self.rect_y += 2

            if self.rect_y == 0:
                screen.fill(BLACK)
                endfont1 = pygame.font.SysFont('broadway', 52)
                endfont2 = pygame.font.SysFont('timesnewroman', 40)
                text1 = endfont1.render("GAME OVER", True, WHITE)
                screen.blit(text1,[75, 100])
                text2 = endfont2.render("Score: %s" %(self.hit), True, WHITE)
                screen.blit(text2,[170, 175])
                text3 = endfont2.render("Play again?", True, WHITE)
                screen.blit(text3,[150, 300])
                pygame.mouse.set_visible(True)

        if not self.game_over:
            datafont = pygame.font.SysFont(None, 20)
            missed_text = datafont.render("missed = %s" %(self.missed),True,WHITE)
            screen.blit(missed_text,[10,460])
            hit_text = datafont.render("hit = %s" %(self.hit),True,WHITE)
            screen.blit(hit_text,[10,440])
            screen.blit(self.hammer.image,self.hammer.rect)
            screen.blit(self.squirrel.image,self.squirrel.rect)
        
            
def run():
    """ Main program """
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Hammer Time")
    
    done = False
    clicked = False

    gameclock = pygame.time.Clock()

    start_game = Startgame()

    high_score = get_high_score()

    theme = load_sound('HammerTheme1')
    theme.play()

    while not clicked:
        clicked = start_game.check_start()
        start_game.start_window(screen,high_score)
        pygame.display.flip()
        gameclock.tick(60)

    theme.stop()
    pygame.mouse.set_visible(False)
    game = Game()
    game.beginfader(screen,gameclock)
    
    while not done:
        done = game.process_events()
        game.game_action()
        game.game_screen(screen,high_score)
        pygame.display.flip()
        gameclock.tick(60)

    pygame.quit()

#if __name__ == "__main__":
    #main()

        
        
        

        
