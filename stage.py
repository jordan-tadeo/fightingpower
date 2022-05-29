import pygame


def_color = (190, 210, 255)


class Stage:
    def __init__(self, rects=[(0, 480-64, 720, 64)], color=def_color):
        self.rects = rects
        self.color = color

    def draw(self, win):
        for r in self.rects:
            pygame.draw.rect(win, self.color, r)
