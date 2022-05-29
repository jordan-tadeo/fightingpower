from turtle import colormode
import pygame
from network import Network

pygame.display.set_caption("Client")
clientNumber = 0

##########################################################################
# Not "client" related exaclty: window creation, character class etc.    #
# We can modify this portion and move to their own folders later         #
##########################################################################
width = 500
height = 500
win = pygame.display.set_mode((width, height))

class Character():
    def __init__(self, x, y, width, height, color):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._rect = (x, y, width, height)
        self._vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self._color, self._rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self._x -= self._vel

        if keys[pygame.K_RIGHT]:
            self._x += self._vel

        if keys[pygame.K_UP]:
            self._y -= self._vel

        if keys[pygame.K_DOWN]:
            self._y += self._vel

        self.update()

    def update(self):
        self._rect = (self._x, self._y, self._width, self._height)

def redrawWindow(win, player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

###########################################################################

###########################################################################
# Helper functions to send and recieve Client positions between server    #
# and client as tuple                                                     #
###########################################################################

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

############################################################################


def main():
    run = True
    n = Network()

    # Get starting position to send to client for their character
    startPos = read_pos(n.getPos())

    p = Character(startPos[0], startPos[1], 100, 100, (0,255,0))
    p2 = Character(0, 0, 100, 100, (255,255,0))

    clock = pygame.time.Clock()

    while run:
        # 60 FPS
        clock.tick(60)

        # Sending Player 2 position to server
        p2Pos = read_pos(n.send(make_pos((p._x, p._y))))
        p2._x = p2Pos[0]
        p2._y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)

main()