# -*- coding:utf-8 -*-
import pygame as pg
from utils import math_utils


class Rectangle:

    def __init__(self, surface, rect, color, cof, G, is_free=True):
        self.surface = surface
        self.rect = rect
        self.color = color
        self.cof = cof  # 摩擦系数
        self.corf = 0.05 # 滚动摩擦系数
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
        """检测是否点击了鼠标左键"""
        return mouse_buttons[0] and self.rect.collidepoint(mouse_pos)

    def check_click_right(self, mouse_pos, mouse_buttons):
        """检测是否点击了鼠标右键"""
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
        self.angle = (self.angle - 1)%360

        width, height = self.rect.size
        bl = self.rect.bottomleft
        br = width, 0
        tr = width, height
        tl = 0, height

        br = math_utils.rotate_point_in_pygame(bl, br, self.angle)
        tr = math_utils.rotate_point_in_pygame(bl, tr, self.angle)
        tl = math_utils.rotate_point_in_pygame(bl, tl, self.angle)
        points = [bl, br, tr, tl]

        pg.draw.polygon(
            self.surface, self.color, points)

    def set_rect(self, rect):
        self.rect = rect
