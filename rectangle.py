# -*- coding:utf-8 -*-
import pygame as pg
from pygame.locals import *
import math
import game_settings as gs
import force
import game_functions as gf
import mathUtils


class Rectangle:

    def __init__(self, surface, rect, color, cof, G, is_free=True):
        self.surface = surface
        self.rect = rect
        self.color = color
        self.cof = cof  # 摩擦系数
        self.G = G  # 重力
        self.forces = []
        self.rect_2 = None
        self.angle = 0
        self.is_free = is_free

    def move(self):
        self.rotate()
        pass

    def draw(self, width=0):
        pg.draw.rect(self.surface, self.color, self.rect, width)

    def move_and_draw(self):
        self.move()
        # self.draw()

    def check_click_left(self, mouse_pos, mouse_buttons):
        return mouse_buttons[0] and self.rect.collidepoint(mouse_pos)

    def check_click_right(self, mouse_pos, mouse_buttons):
        return mouse_buttons[2] and self.rect.collidepoint(mouse_pos)

    def is_selected(self, color, width):
        pg.draw.rect(self.surface, color, self.rect, width)  # 画选中框

    def get_center(self):
        return self.rect.center

    def append_force(self, f):
        self.forces.append(f)

    def draw_force(self, color):
        for f in self.forces:
            f.draw(color)

    def is_hit_the_edge(self, size):
        return False

    def rotate(self):
        self.angle += 1
        width, height = self.rect.size
        BL = self.rect.bottomleft
        BR = width, 0
        TR = width, height
        TL = 0, height

        BR = mathUtils.rotate_point(BR[0], BR[1], self.angle)
        TR = mathUtils.rotate_point(TR[0], TR[1], self.angle)
        TL = mathUtils.rotate_point(TL[0], TL[1], self.angle)
        points = []
        points.append(BL)
        points.append((BL[0] + BR[0], BL[1] - BR[1]))
        points.append((BL[0] + TR[0], BL[1] - TR[1]))
        points.append((BL[0] + TL[0], BL[1] - TL[1]))

        pg.draw.polygon(
            self.surface, self.color, points)

    def set_rect(self, rect):
        self.rect = rect
