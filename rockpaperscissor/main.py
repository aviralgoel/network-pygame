import os
import pygame
from button import Button

width = 700
height = 700
win = pygame.display.set_mode((width, height))  # start the pygame game window render service
pygame.display.set_caption("Main Menu")
pygame.font.init()
run = True;


def drawWindow():
    win.fill((128, 128, 128))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Welcome to our Host-to-Play Game", 1, (255, 0, 0), True)
    win.blit(text, (width / 2 - text.get_width() / 2, -200 + height / 2 - text.get_height() / 2))
    font = pygame.font.SysFont("comicsans", 30)
    text2 = font.render("What would you like to do?", 1, (255, 0, 0), True)
    win.blit(text2, (width / 2 - text2.get_width() / 2, -100 + height / 2 - text2.get_height() / 2))
    for btn in btns:
        btn.draw(win)
    pygame.display.update()


btns = [Button("Client", 75, 300, (0, 0, 230)), Button("Server", 275, 300, (0, 0, 0)),
        Button("Quit", 475, 300, (255, 0, 0))]


def userInput():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for btn in btns:
                if btn.click(pos):
                    if btn.text == "Client":
                        pygame.quit()
                        run = False
                        os.system('python client.py')
                        exit()
                    elif btn.text == "Server":
                        pygame.quit()
                        os.system('python server.py')
                        exit()
                        run = False







if __name__ == "__main__":
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        drawWindow()
        userInput()
