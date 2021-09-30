import pygame

# Player class which includes all the properties of the player and it's methods.
class Player:
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

