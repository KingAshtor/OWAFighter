# JS Fighter project continued on by OWA development
# OWA Employees
# 1. Ashton Sisson
# 2.Harry Nelson
# 3.Daniel Williams
# 4.Nathan Cunningham
# 9.Mykahl Luciano
# Imports Pygame
# Imports modules
import pygame; #Imports pygame used to create the window and game elements
import os; #Imports os which allows the console to run like windows command line
import time; #Imports time wich allows the code to use timeing that is easier to understand

# Initiates Pygame
pygame.init()

# Makes Screen Resolutions Variables
xRes = 1000 #Sets Horizontal Resoulution (Xaxis)
yRes = 500 #Sets Vertical Resoulution (Yaxis)

# Sets the game display size to the resolution varibles
gameDisplay = pygame.display.set_mode((xRes, yRes))

# Makes Minumum and Maximum For Screen Boundries
yMin = yRes - 50
# Minumum Y
xMin = 20
xMax = xRes - 50

# Creates Gravity and air resistance
gravity = 1
terminalVelocity = 100

# Set the title
pygame.display.set_caption('OWA Fighter')

# makes the clock object
clock = pygame.time.Clock()

#makes the buttons exist and default to unpressed
buttonUp = buttonDown = buttonLeft = buttonRight = buttonUse = buttonJump = buttonJumpLast = buttonUp1 = buttonDown1 = buttonLeft1 = buttonRight1 = buttonUse1 = buttonJump1 = buttonJumpLast1 = False

#Sets default values for the fighter class
START_HP = 10;
START_SP = 20;
DEFAULT_ATK = 5;
DEFAULT_DEF = 5;
DEFAULT_TEK = 5;
direct = 0;
#sets constants names
P0NAME = 'Crash';
P0CHARA = 'crashr';
P1NAME = 'Sam';
P1CHARA = 'saml';

#makes list to store the consoles outputs
outputList = ["Start",]

enemyDirect = 'left'

punches = []
colliders = []
#makes the stuff exist
buttonUp = buttonDown = buttonLeft = buttonRight = buttonUse = buttonUp1 = buttonDown1 = buttonLeft1 = buttonRight1 = buttonUse1 = False

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
        os.system("cls") #clears the console
        os.system("color 02") #Makes green so you are a true heckermen

        #for loop used to print all the console.log data
        for item in outputList:
            print(item)




# creates class for player
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
        self.maxhp = 100
        self.direct = 0
        self.hp = START_HP # sets hp to START_HP
        self.weight = 1 # weight used to modify jump
        self.airborne = False # tracks wether you are airbourne or note

    # draws the player and its hitBox as a rectangle and also is responsible for assigning color
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.hitBox)
    # used to move the player horizontally
    def moveHorizontal(self, velocity):

        # if its its momentum is less then max speed add acceleration to increase velocity
        if abs(self.xMom) < self.maxSpeed:
            self.xMom += (velocity * self.accel)

        # If his speed is greater then or less then max speed set momentum to zero
        if self.x > xMax:
            self.x = xMax
            self.xMom = 0
        elif self.x < xMin:
            self.x = xMin
            self.xMom = 0

    # function for jumping
    def jump(self, power, direction):
        # if you are not airborne and you jump you then jump and become airbourne
        if not self.airborne:
            self.airborne = True
            self.yMom += (power * 30)

    def physics(self):
        # Horizontal acceleration and deceleration
        if self.xMom > 0:
            self.xMom -= self.decel
        elif self.xMom < 0:
            self.xMom += self.decel

        # if player is below the Minumum then return him to minimum and make them no longer fall or be airbourne
        if self.y > yMin:
            self.airborne = False
            self.y = yMin
            self.yMom = 0
            console.log('Below Min')

        # if player is airbourne then...
        if self.airborne == True:
            self.yMom += (self.weight + gravity) #get pulled down by gravity

            #if you are faster then terminalVelocity...
            if abs(self.yMom) > terminalVelocity:
                if self.yMom > terminalVelocity:
                    #if you are moving above terminalVelocity cap speed to terminalVelocity
                    self.yMom = -terminalVelocity;
                else:
                    #if below terminalVelocity then cap speed to negitive terminalVelocity
                    self.yMom = terminalVelocity;

        self.x += self.xMom #add horizontal movement
        self.y += self.yMom #add verticle movement

        #move hitbox with player
        self.hitBox = pygame.Rect( (self.x, self.y, self.w, self.h))

    def use(self):
        if self.xMom < 0:
            self.direct = -40
        elif self.xMom > 0:
            self.direct = 40
        else:
            self.direct = 0

        punches.append(PunchyBoi(self.x + self.direct, self.y))
        # console.log('punched')

        # If leaving left edge
        if self.x < xMin:
            # Put player back in boundaries
            self.x = xMin
            # Invert momentum to bounce back
            self.xMom = self.xMom * -1
            # set HP = HP - 1
            self.hp = self.hp - 1
            #log
            console.log('Out Of Bounds Left!')
            # If leaving right edge
        if self.x > 1280 - self.w:
            self.x = 1280 - self.w
            self.xMom = self.xMom * -1

        # If leaving left edge
        if self.x > xMax:
            # Put player back in boundaries
            self.x = xMax
            # Invert momentum to bounce back
            self.xMom = self.xMom * -1
            #HP = HP - 1
            self.hp = self.hp - 1
            #Log
            console.log('Out Of Bounds Right!')
            # If leaving right edge
        if self.x > 1280 - self.w:
            self.x = 1280 - self.w
            self.xMom = self.xMom * -1
        if self.hp == 0:
            self.color = (30, 60, 90 / 2)
            console.log('Game over');
            self.hp = 1;

class Baddy(Player):
    def __init__(self, x=xMax, y=yMin):
        super().__init__(x, y)
        self.color = (420 / 2, 69, 69) # Blazit

class PunchyBoi(Player):
    def __init__(self, x=xMax, y=yMin):
        super().__init__(x, y)
        self.color = (7, 85, 2)
        self.h = 32
        self.hitBox = pygame.Rect( (self.x + self.direct, self.y, self.w, self.h) )
        def draw(self):
            pygame.draw.rect(gameDisplay, self.color, self.hitBox)
            self.pos = pygame.Rect( (self.x, self.y, self.w, self.h) )
            if self.hitBox == self.pos:
                console.log('DAMAGE!')
                self.hp - 1


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


#Creates Objects
player0 = Player()
player1 = Baddy()
attk = PunchyBoi()
console.log('Players created')
lWall = LeftWall()
rWall = RightWall()
stage = Stage()
console.log('Stage created')

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
                # USE (SPACE)
                if event.key == pygame.K_g:
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
                # # Jump (SPACE)
                if event.key == pygame.K_KP0:
                    buttonJump1 = True
                # # USE (SPACE)
                if event.key == pygame.K_KP8:
                    buttonUse1 = True
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
                if event.key == pygame.K_g:
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
                if event.key == pygame.K_KP0:
                    buttonJump1 = False
                if event.key == pygame.K_KP8:
                    buttonUse1 = False

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
        if buttonUse:
            if not buttonuseLast:
                player0.use()
                buttonuseLast = True
        else:
            buttonuseLast = False
        if buttonUse1:
            if not buttonuseLast:
                player1.use()
                buttonuseLast = True
        else:
            buttonuseLast = False

        ### -------------------------------------- ###
        ### Game Functions
        ### -------------------------------------- ###
        # Move objects
        player0.physics()
        player1.physics()
        attk.physics()
        # Update screen
        gameDisplay.fill( (205,215,200) ) # Erase screen
        player0.draw()
        player1.draw()

        #draws the walls and floor
        lWall.draw()
        rWall.draw()
        stage.draw()

        for punch in punches:
            punch.draw()
            punches.remove(punch)

        #Updates the display
        pygame.display.update()

        # Wait until tick (60hz) is over
        time.sleep(.025)
        pass
