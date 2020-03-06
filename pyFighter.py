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
import time;

# Initiates Pygame
pygame.init()

# Makes Screen Resolutions Variables
xRes = 1000 #Sets Horizontal Resoulution (Xaxis)
yRes = 500 #Sets Vertical Resoulution (Yaxis)

# Sets the display size
gameDisplay = pygame.display.set_mode((xRes, yRes))

# Makes Minumum and Maximum Screen Boundries
yMin = yRes - 50
xMin = 20
xMax = xRes - 50

x = 15
y = yRes - 40
# Creates Gravity and air resistance
gravity = 1
terminalVelocity = 100

# Set the title
pygame.display.set_caption('OWA Fighter')

# make the clock object
clock = pygame.time.Clock()

#Sets default values for the fighter class
START_HP = 100;
START_SP = 20;
DEFAULT_ATK = 5;
DEFAULT_DEF = 5;
DEFAULT_TEK = 5;

#sets constants names for fighters
P0NAME = 'Crash';
P0CHARA = 'crashr';
P1NAME = 'Sam';
P1CHARA = 'saml';

#makes list to store the console
outputList = ["Start",]

#makes console.log
class console():
    # makes console.log command
    def log(phrase):
        #console.log adds the varible "phrase" to the list outputList then it refreshes terminal
        outputList.append(phrase)
        console.refresh()
    # makes console.unlog command
    def unlog(phrase):
        #console.unlog removes the varible "phrase" from the list outputList then it refreshes terminal
        outputList.remove(phrase)
        console.refresh()
    #makes the console.refresh command
    def refresh():
        # Console clears using the commamd prompt comand cls then it makes it look cool by changing the colors and then lists the entire outputList
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

#makes the buttons exist and default to unpressed
buttonUp = buttonDown = buttonLeft = buttonRight = buttonUse = buttonJump = buttonJumpLast = buttonUp1 = buttonDown1 = buttonLeft1 = buttonRight1 = buttonUse1 = buttonJump1 = buttonJumpLast1 = False
#
# # creates class for player
class Player():
    def __init__(self, x=xMin, y=yMin):
        self.x = x # X Position
        self.y = y # Y Position
        self.w = 32 # Width
        self.h = 32 # Height
        self.direction = 'down'
        self.xMom = 0 # X Momentum
        self.yMom = 0 # y Momentum
        self.accel = 4 # Acceledasration
        self.decel = 2 # Deceleration
        self.maxSpeed = 10 # Maximum speed
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h) )
        self.color = (69, 69, 420 / 2) # Bluezit
        self.hp = START_HP
        self.maxhp = START_HP
        self.maxWidth = 300
        self.weight = 1
        self.airborne = False
        self.dead = False
    def draw(self, barX, barY):
        pygame.draw.rect(gameDisplay, self.color, self.hitBox)
        bgColor = (255, 0, 0)
        fgColor = (0, 255, 0)
        barWidth = (self.hp / self.maxhp) * self.maxWidth
        bgBar = pygame.Rect( (barX, barY, self.maxWidth, 8) )
        fgBar = pygame.Rect( (barX, barY, barWidth, 8) )
        pygame.draw.rect(gameDisplay, bgColor, bgBar)
        if self.dead == False:
            pygame.draw.rect(gameDisplay, fgColor, fgBar)

        if self.hp == 0:
            self.dead = True
    def moveHorizontal(self, velocity):
        if abs(self.xMom) < self.maxSpeed:
            self.xMom += (velocity * self.accel)

        if self.x > xMax:
            self.x = xMax
            self.xMom = 0
        elif self.x < xMin:
            self.x = xMin
            self.xMom = 0

    def jump(self, power, direction):
        if not self.airborne:
            self.airborne = True
            self.yMom += (power * 30)

    def physics(self):
        # Horizontal
        if self.xMom > 0:
            self.xMom -= self.decel
        elif self.xMom < 0:
            self.xMom += self.decel

        if self.y > yMin:
            self.airborne = False
            self.y = yMin
            self.yMom = 0
            console.log('Below Min')

        if self.airborne == True:
            self.yMom += (self.weight + gravity)
            if abs(self.yMom) > terminalVelocity:
                if self.yMom > terminalVelocity:
                    self.yMom = -terminalVelocity;
                else:
                    self.yMom = terminalVelocity;

        self.x += self.xMom
        self.y += self.yMom
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h))
        # If leaving left edge
        if self.x < xMin:
            # Put player back in boundaries
            self.x = xMin
            # Invert momentum to bounce back
            self.xMom = self.xMom * -1
            # set HP = HP - 1
            self.hp = self.hp - 1
            #log
            console.log('working')
            # If leaving right edge
        if self.x > 1280 - self.w:
            self.x = 1280 - self.w
            self.xMom = self.xMom * -1

        if self.x > xMax:
            # Put player back in boundaries
            self.x = xMax
            # Invert momentum to bounce back
            self.xMom = self.xMom * -1
            #HP = HP - 1
            self.hp = self.hp - 1
            #Log
            console.log('working')
            # If leaving right edge
        if self.x > 1280 - self.w:
            self.x = 1280 - self.w
            self.xMom = self.xMom * -1

        # if self.y < 0:
            # Put player back in boundaries
            # self.y = yMin

        if self.hp == 0:
            self.color = (30, 60, 90 / 2)
            console.log('Game over');
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
                # JUMP (SPACE)
                if event.key == pygame.K_SPACE:
                    buttonJump = True
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
                # # Jump (SPACE)
                if event.key == pygame.K_KP0:
                    buttonJump1 = True
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
                    buttonJump = False
                #player1
                if event.key == pygame.K_UP:
                    buttonUp1 = False
                if event.key == pygame.K_LEFT:
                    buttonLeft1 = False
                if event.key == pygame.K_DOWN:
                    buttonDown1 = False
                if event.key == pygame.K_RIGHT:
                    buttonRight1 = False
                if event.key == pygame.K_KP0:
                    buttonJump1 = False

        if buttonLeft:
            player0.moveHorizontal(-1)
        if buttonRight:
            player0.moveHorizontal(1)
        if buttonJump:
            if not buttonJumpLast:
                player0.jump(-1, 1)
                buttonJumpLast = True
        else:
            buttonJumpLast = False

        if buttonLeft1:
            player1.moveHorizontal(-1)
        if buttonRight1:
            player1.moveHorizontal(1)
        if buttonJump1:
            if not buttonJumpLast1:
                player1.jump(-1, 1)
                buttonJumpLast1 = True
        else:
            buttonJumpLast1 = False
        ### -------------------------------------- ###
        ### Game Functions
        ### -------------------------------------- ###
        # Move objects
        player0.physics()
        player1.physics()
        # Update screen
        gameDisplay.fill( (0,0,0) ) # Erase screen
        player0.draw(20,0)
        player1.draw(683,0)
        lWall.draw()
        rWall.draw()
        stage.draw()
        # healthCounter.draw()
        pygame.display.update()
        # Wait until tick (60hz) is over
        time.sleep(.025)
        pass
