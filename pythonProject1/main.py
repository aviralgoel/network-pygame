import pygame
from network import Network  # importing Network class from our network file to add networking capabilities to the client

# desired height, width and title of the player game window rendered using pygame
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# client number
clientNumber = 0


# Player class which includes all the properties of the player and it's methods.
class Player():
    def __init__(self, x, y, width, height, color):  # constructor
        self.x = x  # player's x position
        self.y = y  # player's y position
        self.width = width  # player's width
        self.height = height  # player's height
        self.color = color  # player's color
        self.rect = (x, y, width, height)
        self.stepSize = 3  # player's moving amount per input event

    # method to draw player rect on screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    # detect user input
    def move(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.stepSize

        if keys[pygame.K_RIGHT]:
            self.x += self.stepSize

        if keys[pygame.K_UP]:
            self.y -= self.stepSize

        if keys[pygame.K_DOWN]:
            self.y += self.stepSize

        self.update()

    # update player position variables for redrawing
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


# this function takes a screen and returns a tuple of two integers
# it is used for converting player co-ordinates from string to int format
def read_pos(posStr):
    posStr = posStr.split(",")
    return int(posStr[0]), int(posStr[1])

# this function takes a tuple and returns a string
# it is used for converting player co-ordinates from int to string format
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# Game Screen Render function
# 1. Draws the window object on screen
# 2. Draws the player1 on window
# 3. Draws the player2 on window
# 4. Refresh/Update the screen with above

def redrawWindow(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

# Game main update loop
# 1. Start the game, create player object, network object and start the clock
# 2. get player1 position from the Network class
# 3. initialize player 1 and player 2

# 2. while game not over
##      run 60fps, if game not quitted then, move player(player input check) and
# 3. Update player input
# 4. Render screen

def main():
    run = True
    n = Network() # Establish connection to server (if the connection is not established, game breaks down, socket object throws an error)
    startPos = read_pos(n.getPos())
    p1 = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(0, 0, 100, 100, (255, 0, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60) # make sure the game runs 60FPS
        p2Pos = read_pos(n.send(make_pos((p1.x, p1.y)))) #get p2 position by sending p1 position
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update() # update p2 position

        # check for game over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p1.move() #update p1 postion
        redrawWindow(win, p1, p2) #refresh screen


main()
