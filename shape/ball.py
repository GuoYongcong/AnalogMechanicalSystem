# -*- coding:utf-8 -*-
import pygame as pg
import math
from pygame.locals import *
import game_settings as gs
from utils import math_utils

RADIUS = 50  # 半径


class Ball:

    def __init__(self, game_surface, pos, m, v, color, is_free=True):
        self.pos = pos  # 球心的位置，例如(0,0)表示在界面左上角
        self.m = m  # 质量
        self.r = RADIUS  # 半径
        self.v = v  # v=(v_x, v_y), v_x, v_y分别表示x,y轴方向的速度，正数分别表示速向右，向下
        self.color = color  # 颜色
        self.game_surface = game_surface  # 界面
        self.forces = []
        self.supporting_forces = {}
        self.rolling_friction = {}
        self.a = (0, gs.g)
        self.rotating_degrees = 0  # 小球旋转的角度数，逆时针为正
        self.rotating_a = 0  # 小球的旋转角加速度，逆时针为正
        self.rotating_v = 0  # 小球的旋转角速度，逆时针为正
        self.cof = 0.5  # 滑动摩擦系数
        self.corf = 0.05  # 滚动摩擦系数
        self.is_free = is_free

    def move(self):
        # 计算加速度
        if len(self.supporting_forces) > 0:
            sf = None
            for item in self.supporting_forces.values():
                sf = item
            rad = math.radians(math.fabs(sf.get_angle() + 90))
            ac = gs.g * math.sin(rad)
            self.a = -ac * math.cos(rad), ac * math.sin(rad)
            self.rotate()
            vv = math.radians(self.rotating_v) * self.r
            self.v = -vv * math.cos(rad), vv * math.sin(rad)
            # if 0 == degrees:
            #     temp = math.radians(self.rotating_v) * self.r
            #     self.a = self.a[0] - temp * math.cos(
            #         degrees), self.a[1] + temp * math.sin(degrees)
        else:
            self.a = (0, gs.g)
            for f in self.forces:
                self.a = self.a[0] + (f.get_f()[0] /
                                      self.m), self.a[1] + (f.get_f()[1] / self.m)
            self.rotate()
            self.v = self.v[0] + self.a[0], self.v[1] + self.a[1]

        # 计算位置
        self.pos = (self.pos[0] + self.v[0], self.pos[1] + self.v[1])
        # 调整力在屏幕的位置
        for force in self.forces:
            pos = force.get_pos()
            force.set_pos(pos[0] + self.v[0], pos[1] + self.v[1])

    def draw(self):
        pg.draw.circle(
            self.game_surface, self.color, (round(
                self.pos[0]), round(
                self.pos[1])), self.r)
        start_pos = self.pos
        end_pos = math_utils.rotate_point_in_pygame(
            start_pos, (start_pos[0], start_pos[1] - self.r), -self.rotating_degrees)
        width = 1
        pg.draw.line(
            self.game_surface,
            Color('white'),
            (round(start_pos[0]), round(start_pos[1])),
            (round(end_pos[0]), round(end_pos[1])),
            width)

    def move_and_draw(self):
        self.move()
        self.draw()

    def get_center(self):
        return self.pos

    def append_force(self, f):
        self.forces.append(f)

    def draw_force(self, color):
        for f in self.forces:
            f.draw(color)
        # for sf in self.supporting_forces.values():
        #     sf.draw(pg.Color('yellow'))
        # for rf in self.rolling_friction.values():
        #     rf.draw(pg.Color('green'))

    def is_in_ball(self, pos):
        x = self.pos[0] - pos[0]
        y = self.pos[1] - pos[1]
        distance = math.sqrt(x ** 2 + y ** 2)
        return distance <= self.r

    def check_click_left(self, mouse_pos, mouse_buttons):
        return mouse_buttons[0] and self.is_in_ball(mouse_pos)

    def check_click_right(self, mouse_pos, mouse_buttons):
        return mouse_buttons[2] and self.is_in_ball(mouse_pos)

    def is_selected(self, color, width):
        pg.draw.circle(
            self.game_surface, color, (round(
                self.pos[0]), round(
                self.pos[1])), self.r, width)  # 画选中框

    def is_hit_the_edge(self, size):
        flag = False
        value = (-1, 1)
        for i in range(0, 2):
            if self.pos[i] <= self.r or self.pos[i] + self.r >= size[i]:
                # 如果小球碰到界面的左边或右边，则x轴方向的速度大小不变，方向相反；上边或下边则是y轴
                # 假定碰撞后动能损失一半
                times = math.sqrt(1 / 2)
                self.v = ((value[i] * self.v[0] * times),
                          (value[1 - i] * self.v[1] * times))
                self.rotating_v = value[i] * self.rotating_v * times
                flag = True
                temp = 0
                d_value = 0
                if self.pos[i] <= self.r:
                    temp = self.r
                    d_value = self.r - self.pos[i]
                else:
                    temp = size[i] - self.r
                    d_value = size[i] - (self.pos[i] + self.r)

                if 0 == i:
                    self.pos = temp, self.pos[1]
                    for force in self.forces:
                        pos = force.get_pos()
                        force.set_pos(pos[0] + d_value, pos[1])
                else:
                    self.pos = self.pos[0], temp
                    for force in self.forces:
                        pos = force.get_pos()
                        force.set_pos(pos[0], pos[1] + d_value)
        return flag

    # 判断两个小球是否相撞
    def is_hit_another(self, another):
        x = self.pos[0] - another.pos[0]
        y = self.pos[1] - another.pos[1]
        distance = math.sqrt(x ** 2 + y ** 2)
        if 2 * self.r >= distance:  # 如果两个小球相撞
            m = (self.m, another.m)
            v_x = (self.v[0], another.v[0])
            v_y = (self.v[1], another.v[1])
            v = (v_x, v_y)
            obj = (self, another)
            for i in range(0, 2):
                new_v = [0, 0]
                for j in range(0, 2):
                    p = (i + 1) % 2
                    # x轴和y轴方向分别运用动量守恒和能量守恒定理推导出此公式
                    new_v[j] = (v[j][i] * (m[i] - m[p]) + 2 *
                                m[p] * v[j][p]) / (m[0] + m[1])
                obj[i].v = ((new_v[0]), (new_v[1]))  # ()四舍五入
            return True
        else:
            return False

    def rotate(self):
        if len(self.supporting_forces) > 0:
            # sf = None
            # for item in self.supporting_forces.values():
            #     sf = item
            # degrees = math.fabs(sf.get_angle() + 90)
            # self.rotating_a = (
            #     -self.a[0] * math.cos(degrees) + self.a[1] * math.sin(degrees)) / self.r
            self.rotating_a = math_utils.distance_of_two_points(self.a, (0, 0))/2
            self.rotating_a = math.radians(self.rotating_a)
        else:
            self.rotating_a = 0
        self.rotating_v += self.rotating_a
        self.rotating_degrees = (self.rotating_degrees + self.rotating_v) % 360

    def get_v_degrees(self):
        return math.degrees(math.atan2(self.v[1], self.v[0]))

    def append_supporting_force(self, key, f):
        self.supporting_forces[key] = f

    def delete_supporting_force(self, key):
        if self.supporting_forces.get(key):
            self.supporting_forces.pop(key)

    # def append_rolling_friction(self, key, f):
    #     self.rolling_friction[key] = f
    #
    # def delete_rolling_friction(self, key):
    #     if self.rolling_friction.get(key):
    #         self.rolling_friction.pop(key)

    def get_fn(self, degrees):
        """小球对角度为degrees的斜面的正压力"""
        mg = math_utils.rotate_vector((0, self.m * gs.g), degrees)
        coe = 1 if self.v[1] < 0 else -1
        fn = math.fabs(mg[1]) * coe
        for f in self.forces:
            f1 = math_utils.rotate_vector(f.get_f(), degrees)
            fn += math.fabs(f1[1]) * coe
        return fn
