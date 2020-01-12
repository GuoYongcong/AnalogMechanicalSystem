# -*- coding:utf-8 -*-
import pygame as pg
from utils import math_utils
import math

class Polygon:

    def __init__(self, surface, points, color, cof, m, is_free=True):
        self.surface = surface
        self.points = points
        self.color = color
        self.cof = cof  # 摩擦系数
        self.corf = 0.05 # 滚动摩擦系数
        self.m = m  # 质量
        self.forces = []
        self.angle = 0
        self.is_free = is_free

    def move(self):
        pass

    def draw(self, width=0):
        pg.draw.polygon(self.surface, self.color, self.points, width)

    def move_and_draw(self):
        # self.rotate()
        self.move()
        self.draw()

    def check_click_left(self, mouse_pos, mouse_buttons):
        """检测是否点击了鼠标左键"""
        return mouse_buttons[0] and math_utils.point_in_triangle(
            self.points, mouse_pos)

    def check_click_right(self, mouse_pos, mouse_buttons):
        """检测是否点击了鼠标右键"""
        return mouse_buttons[2] and math_utils.point_in_triangle(
            self.points, mouse_pos)

    def is_selected(self, color, width):
        pg.draw.polygon(self.surface, color, self.points, width)  # 画选中框

    def append_force(self, f):
        self.forces.append(f)

    def draw_force(self, color):
        for f in self.forces:
            f.draw(color)

    def is_hit_the_edge(self, size):
        # TODO
        return False

    def get_center(self):
        cx = 0
        cy = 0
        for p in self.points:
            cx += p[0]
            cy += p[1]
        cx = (cx / len(self.points))
        cy = (cy / len(self.points))
        return cx, cy

    def rotate(self):
        self.angle = (self.angle - 3) % 360
        fixed_point = self.points[0]
        for i in range(len(self.points)):
            dx = self.points[i][0] - fixed_point[0]
            dy = self.points[i][1] - fixed_point[1]
            self.points[i] = (math_utils.rotate_point_in_pygame(fixed_point, (dx, dy), self.angle))

        pg.draw.polygon(
            self.surface, self.color, self.points)
