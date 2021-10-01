import pygame
from network import Network
from button import Button
import pickle
pygame.font.init()  # start the pygame text render services

width = 700
height = 700
win = pygame.display.set_mode((width, height))  # start the pygame game window render service
pygame.display.set_caption("Client")

# the screen renderer method for the game this method runs about 60 times per second (60FPS) and draws/refreshes the
# game on the screen it requires three parameters, the pygame canvas window (to be drawn on), the Game class object (
# the game to draw) and the player (according to which to draw)
def redrawWindow(win, game, p):
    win.fill((128,128,128))

    # there are not enough players to start the game
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        # if both players played the move, display those moves
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0: # if I played, show my move
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went: #if player 1 played but not me, then show him as locked
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else: # none of the players played, then show waiting
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1: # if player 2 played and am player 2, show my move
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))
        # according to the above situations, decide the text to render on screen
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
# the game loop method, this method updates the state of the game for the player
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()  # establish the connection with the server
    player = int(n.getP())  # get the ID of the player for the game session decided and returned by the server to the client
    print("You are player", player)

    # game loop
    while run:
        clock.tick(60)
        try:
            game = n.send("get") # send the server a string to request the state of the game in Game class object
        except:
            run = False
            print("Couldn't get game")
            break

        # if both players played the move
        if game.bothWent():
            redrawWindow(win, game, player) # redraw the screen
            pygame.time.delay(500) # wait
            try:
                game = n.send("reset") # send the server signal to reset the round
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            # display the winning/losing screen to appropriate player
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get(): # check if the user tried to quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # if the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text) # send info to the server as string about which move button is played
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player) # redraw the screen


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()