import pygame


def_color = (10, 10, 10)


class Stage:
    def __init__(self, rect=(0, 480-64, 720, 64), color=def_color):
        self.rect = rect
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
