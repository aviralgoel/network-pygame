import pygame
from network import Network  # importing Network class from our network file to add networking capabilities to the client
from player import Player # importing Player class from player file

# desired height, width and title of the player game window rendered using pygame
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


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
    p1 = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60) # make sure the game runs 60FPS
        p2 = n.send(p1)
        # check for game over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p1.move() #update p1 postion
        redrawWindow(win, p1, p2) #refresh screen


main()
