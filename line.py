# -*- coding:utf-8 -*-
import pygame as pg
from pygame.locals import *
import game_settings as gs


class Line:

    def __init__(self, game_surface, color,
                 start_pos, end_pos, width):
        self.game_surface = game_surface
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width

    def draw(self):
        pg.draw.line(self.game_surface, self.color,
                     self.start_pos, self.end_pos, self.width)
