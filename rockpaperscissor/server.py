import socket
from _thread import *
import pickle
from game import Game
import time
import pygame

width = 700
height = 700
server = "192.168.48.129"
port = 5677

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
win = pygame.display.set_mode((width, height))  # start the pygame game window render service
pygame.display.set_caption("Server Stats")
pygame.font.init()



connected = set()
games = {}
idCount = 0
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

def updateStats(currentPlayers, currentTime, currentPlayerIP):

    win.fill((128, 128, 128))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Welcome to our Host-to-Play Game", 1, (255, 0, 0), True)
    win.blit(text, (width / 2 - text.get_width() / 2, -200 + height / 2 - text.get_height() / 2))
    font = pygame.font.SysFont("comicsans", 30)
    text2 = font.render("You are hosting a server", 1, (255, 0, 0), True)
    win.blit(text2, (width / 2 - text2.get_width() / 2, -100 + height / 2 - text2.get_height() / 2))
    font = pygame.font.SysFont("comicsans", 20)
    text2 = font.render("Total Players on your server: " + str(currentPlayers), 1, (255, 0, 0), True)
    win.blit(text2, (width / 2 - text2.get_width() / 2, -80 + height / 2 - text2.get_height() / 2))
    text2 = font.render("Total Server Runtime: " + str(currentTime), 1, (0, 235, 0), True)
    win.blit(text2, (width / 2 - text2.get_width() / 2, -140 + height / 2 - text2.get_height() / 2))
    text2 = font.render(("Latest Player Info" + str(currentPlayerIP)), 1, (0, 235, 0), True)
    win.blit(text2, (width / 2 - text2.get_width() / 2, -180 + height / 2 - text2.get_height() / 2))
    pygame.display.update()


def checkForConnection():
    global idCount
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    start_time = time.time()
    while True:

        conn, addr = s.accept()
        print("Player with IP address: ",addr, " connected")

        idCount += 1
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            p = 1
        updateStats(idCount, (time.time() - start_time), addr)
        start_new_thread(threaded_client, (conn, p, gameId))


updateStats(0, 0, 0)
checkForConnection()




