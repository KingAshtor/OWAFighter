# JS Fighter project continued on by OWA development
# OWA Employees
# 1. Ashton Sisson
# 2.Harry Nelson
# 3.Daniel Williams
# 4.Nathan Cunningham
# 9.Mykahl Luciano

# Imports Pygame
import pygame;
import os;

# Initiates Pygame
pygame.init()

# Makes Screen Resoulution Variables
xRes = 1000
yRes = 500

# Minumum Y
yMin = yRes - 50
# Minumum and Maximum X
xMin = 20
xMax = xRes - 50

# Sets the display size
gameDisplay = pygame.display.set_mode((xRes, yRes))

# Set the title
pygame.display.set_caption('OWA Fighter')

# make the clock object
clock = pygame.time.Clock()

#Sets default values for the fighter class
START_HP = 9;
START_SP = 20;
DEFAULT_ATK = 5;
DEFAULT_DEF = 5;
DEFAULT_TEK = 5;

#sets constants names
P0NAME = 'Crash';
P0CHARA = 'crashr';
P1NAME = 'Sam';
P1CHARA = 'saml';

#makes log
outputList = ["Start",]

#makes the stuff exist
buttonUp = buttonDown = buttonLeft = buttonRight = buttonUse = buttonUp1 = buttonDown1 = buttonLeft1 = buttonRight1 = buttonUse1 = False

class console():
    def log(phrase):
        outputList.append(phrase)
        console.refresh()
    def unlog(phrase):
        outputList.remove(phrase)
        console.refresh()
    def refresh():
        os.system("cls")
        os.system("color 02")
        for item in outputList:
            print(item)


class LeftWall():
    def __init__(self, x=0, y=0):
        self.x = x # X Position
        self.y = y # Y Position
        self.w = 19 # Width
        self.h = 550 # Height
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h) )
        self.color = (30, 60, 90 / 2) # Bluezit
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.hitBox)

class RightWall():
    def __init__(self, x=983, y=0):
        self.x = x # X Position
        self.y = y # Y Position
        self.w = 19 # Width
        self.h = 550 # Height
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h) )
        self.color = (30, 60, 90 / 2) # Bluezit
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.hitBox)

class Stage():
    def __init__(self, x=0, y=0):
        self.x = x # X Position
        self.y = 481 # Y Position
        self.w = 3200 # Width
        self.h = 32 # Height
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h) )
        self.color = (30, 60, 90 / 2) # Bluezit

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.hitBox)

# creates class for player
class Player():
    def __init__(self, x=xMin, y=yMin):
        self.x = x # X Position
        self.y = y # Y Position
        self.w = 32 # Width
        self.h = 32 # Height
        self.direction = 'down'
        self.xMom = 0 # X Momentum
        self.accel = 2 # Acceledasration
        self.decel = 1 # Deceleration
        self.maxSpeed = 10 # Maximum speed
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h) )
        self.color = (69, 69, 420 / 2) # Bluezit
        self.hp = START_HP
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.hitBox)
    def moveHorizontal(self, velocity):
        if abs(self.xMom) < self.maxSpeed:
            self.xMom = self.xMom + (velocity * self.accel)

        if self.x > xMax:
            self.x = xMax
            self.xMom = 0
        elif self.x < xMin:
            self.x = xMin
            self.xMom = 0

    def physics(self):
        # Horizontal
        if self.xMom > 0:
            self.xMom = self.xMom - self.decel
        elif self.xMom < 0:
            self.xMom = self.xMom + self.decel

        self.x = self.x + self.xMom
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h))
        # If leaving left edge
        if self.x < xMin:
            # Put player back in boundaries
            self.x = xMin
            # Invert momentum to bounce back
            self.xMom = self.xMom * -1
            # If leaving right edge
        if self.x > 1280 - self.w:
            self.x = 1280 - self.w
            self.xMom = self.xMom * -1

        if self.x > xMax:
            # Put player back in boundaries
            self.x = xMax
            # Invert momentum to bounce back
            self.xMom = self.xMom * -1
            # If leaving right edge
        if self.x > 1280 - self.w:
            self.x = 1280 - self.w
            self.xMom = self.xMom * -1


class Baddy(Player):
    def __init__(self, x=xMax, y=yMin):
        super().__init__(x, y)
        self.color = (420 / 2, 69, 69) # Blazit


player0 = Player()
player1 = Baddy()
lWall = LeftWall()
rWall = RightWall()
stage = Stage()
console.log('Players created')

while True:
        ### -------------------------------------- ###
        ### Keyboard Events for Controls
        ### -------------------------------------- ###
        # Look for events
        for event in pygame.event.get():
            # If one of the events was "QUIT"
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                # Escape key quits the game
                if event.key == pygame.K_ESCAPE:
                    quit()
                # UP (W)
                if event.key == pygame.K_w:
                    buttonUp = True
                # LEFT (A)
                if event.key == pygame.K_a:
                    buttonLeft = True
                # DOWN (S)
                if event.key == pygame.K_s:
                    buttonDown = True
                # RIGHT (D)
                if event.key == pygame.K_d:
                    buttonRight = True
                # USE (SPACE)
                if event.key == pygame.K_SPACE:
                    buttonUse = True
            # player 1
                # UP (Up Arrow)
                if event.key == pygame.K_UP:
                    buttonUp1 = True
                # LEFT (left arrow)
                if event.key == pygame.K_LEFT:
                    buttonLeft1 = True
                # DOWN (Down Arrow)
                if event.key == pygame.K_DOWN:
                    buttonDown1 = True
                # RIGHT (Right arrow)
                if event.key == pygame.K_RIGHT:
                    buttonRight1 = True
                # # USE (SPACE)
                # if event.key == pygame.K_SPACE:
                #     buttonUse1 = True
            # If the event is a key RELEASE (up)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    buttonUp = False
                if event.key == pygame.K_a:
                    buttonLeft = False
                if event.key == pygame.K_s:
                    buttonDown = False
                if event.key == pygame.K_d:
                    buttonRight = False
                if event.key == pygame.K_SPACE:
                    buttonUse = False
                #player1
                if event.key == pygame.K_UP:
                    buttonUp1 = False
                if event.key == pygame.K_LEFT:
                    buttonLeft1 = False
                if event.key == pygame.K_DOWN:
                    buttonDown1 = False
                if event.key == pygame.K_RIGHT:
                    buttonRight1 = False
                # if event.key == pygame.K_SPACE:
                #     buttonUse1 = False

        if buttonLeft:
            player0.moveHorizontal(-1)
        if buttonRight:
            player0.moveHorizontal(1)
        if buttonLeft1:
            player1.moveHorizontal(-1)
        if buttonRight1:
            player1.moveHorizontal(1)
        else:
            buttonuseLast = False
        ### -------------------------------------- ###
        ### Game Functions
        ### -------------------------------------- ###
        # Move objects
        player0.physics()
        player1.physics()
        # Update screen
        gameDisplay.fill( (0,0,0) ) # Erase screen
        player0.draw()
        player1.draw()
        lWall.draw()
        rWall.draw()
        stage.draw()

        pygame.display.update()
        # Wait until tick (60hz) is over
        clock.tick(60)
        pass
