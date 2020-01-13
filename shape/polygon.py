# -*- coding:utf-8 -*-
import pygame as pg
from utils import math_utils
import math
import game_settings as gs


class Polygon:

    def __init__(self, surface, points, color, cof, m, is_free=True):
        self.surface = surface
        self.points = points
        self.color = color
        self.cof = cof  # 摩擦系数
        self.corf = 0.05 # 滚动摩擦系数
        self.m = m  # 质量
        self.forces = []
        self.rotating_a = 0
        self.rotating_v = 0
        self.rad = 0
        self.is_free = is_free

    def move(self):
        self.rotate()

    def draw(self, width=0):
        pg.draw.polygon(self.surface, self.color, self.points, width)

    def move_and_draw(self):
        self.move()
        self.draw()

    def check_click_left(self, mouse_pos, mouse_buttons):
        """检测是否点击了鼠标左键"""
        return mouse_buttons[0] and math_utils.point_in_polygon(
            self.points, mouse_pos)

    def check_click_right(self, mouse_pos, mouse_buttons):
        """检测是否点击了鼠标右键"""
        return mouse_buttons[2] and math_utils.point_in_polygon(
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
        if len(self.points) == 4:
            # fixed_point = math_utils.add_op(self.points[0], self.points[3])
            # fixed_point = math_utils.times(fixed_point, 1/2)
            fixed_point = self.points[0]
            width = math_utils.distance_of_two_points(self.points[0], self.points[1])
            height = math_utils.distance_of_two_points(self.points[1], self.points[2])
            i = self.m * (width**2 + height**2) / 3  # 转动惯量
            d = width / 2   # 力臂
            f = self.m * gs.g   # 力的大小
            sin = math.sin(math.radians(90) - self.rad)
            M = d * f * sin     # 力矩
            self.rotating_a = M / i
            for force in self.forces:
                d = math_utils.distance_of_two_points(force.get_pos(), fixed_point)
                degrees = force.get_angle()
                f = force.get_value()
                sin = math.sin(math.radians(degrees) - self.rad)
                M = d * f * sin
                self.rotating_a += M / i
            self.rotating_v -= self.rotating_a
            self.rad += math.radians(self.rotating_v)
            pg.draw.line(self.surface, pg.Color('red'),fixed_point, fixed_point,5)
            for i in range(len(self.points)):
                self.points[i] = math_utils.rotate_point_in_pygame(fixed_point, self.points[i], self.rotating_v)
            pg.draw.polygon(
                self.surface, self.color, self.points)
            # 修正力的位置
            for force in self.forces:
                new_pos = math_utils.rotate_point_in_pygame(fixed_point, force.get_pos(), self.rotating_v)
                force.set_pos(new_pos[0], new_pos[1])

