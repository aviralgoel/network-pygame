import pygame

width = 500
height = 500
win = pygame.display.set_mode((width, height)) # game window object w/ width and height
pygame.display.set_caption("Client") # game window title

clientNumber = 0


class Player(): # Player class
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.stepSize = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

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

        self.rect = (self.x, self.y, self.width, self.height)

#Game Screen Render function
# 1. Draws the window object on screen
# 2. Draws the player on window
# 3. Refresh/Update the screen with above
def redrawWindow(win,player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()

# Game main update loop
# 1. Start the game, create player object and start the clock
# 2. while game not over
##      run 60fps, if game not quitted then, move player(player input check) and
# 3. Update player input
# 4. Render screen
def main():
    run = True
    p = Player(50,50,100,100,(0,255,0))
    clock = pygame.time.Clock()

    while run:
        #test comment
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)

main()