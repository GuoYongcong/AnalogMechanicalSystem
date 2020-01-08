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
        self.rotate()
        s = math.radians(self.rotating_v) * self.r
        # 计算加速度
        self.a = (0, gs.g)
        for f in self.forces:
            self.a = self.a[0] + round(f.get_f()[0] / \
                                       self.m), self.a[1] + round(f.get_f()[1] / self.m)
        for sf in self.supporting_forces.values():
            self.a = self.a[0] + round(sf.get_f()[0] / \
                                       self.m), self.a[1] + round(sf.get_f()[1] / self.m)

        # 计算速度
        self.v = self.v[0] + self.a[0], self.v[1] + self.a[1]
        # 计算位置
        self.pos = (self.pos[0] + self.v[0], self.pos[1] + self.v[1])
        # 调整力在屏幕的位置
        for force in self.forces:
            pos = force.get_pos()
            force.set_pos(pos[0] + self.v[0], pos[1] + self.v[1])

    def draw(self):
        pg.draw.circle(
            self.game_surface, self.color, self.pos, self.r)
        start_pos = self.pos
        end_pos = math_utils.rotate_point_in_pygame(
            start_pos, (0, self.r), self.rotating_degrees)
        width = 1
        pg.draw.line(
            self.game_surface,
            Color('white'),
            start_pos,
            end_pos,
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
        for sf in self.supporting_forces.values():
            sf.draw(pg.Color('yellow'))
        for rf in self.rolling_friction.values():
            rf.draw(pg.Color('green'))

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
        pg.draw.circle(self.game_surface, color,
                       self.pos, self.r, width)  # 画选中框

    def is_hit_the_edge(self, size):
        flag = False
        value = (-1, 1)
        for i in range(0, 2):
            if self.pos[i] <= self.r or self.pos[i] + self.r >= size[i]:
                # 如果小球碰到界面的左边或右边，则x轴方向的速度大小不变，方向相反；上边或下边则是y轴
                # 假定碰撞后动能损失一半
                self.v = (round(value[i] * self.v[0] / math.sqrt(2)),
                          round(value[1 - i] * self.v[1] / math.sqrt(2)))
                flag = True
                temp = 0
                d_value = 0
                if self.pos[i] <= self.r:
                    temp = self.r
                    d_value = self.r - self.pos[i]
                else:
                    temp = size[i] - self.r
                    d_value = size[i] - (self.pos[i] + self.r)

                temp = round(temp)
                d_value = round(d_value)
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
                obj[i].v = (round(new_v[0]), round(new_v[1]))  # round()四舍五入
            return True
        else:
            return False

    def rotate(self):
        rf_v = 0
        for rf in self.rolling_friction.values():
            rf_v += rf.get_value()
        moment = rf_v * self.r  # 合外力矩
        inertia = (self.m * self.r**2) / 2  # 圆形的转动惯量
        self.rotating_a = moment / inertia
        self.rotating_a = - self.rotating_a
        self.rotating_v += self.rotating_a
        self.rotating_degrees = (self.rotating_degrees + self.rotating_v) % 360

    def get_v_degrees(self):
        return math.degrees(math.atan2(self.v[1], self.v[0]))

    def append_supporting_force(self, key, f):
        self.supporting_forces[key] = f

    def delete_supporting_force(self, key):
        if self.supporting_forces.get(key):
            self.supporting_forces.pop(key)

    def append_rolling_friction(self, key, f):
        self.rolling_friction[key] = f

    def delete_rolling_friction(self, key):
        if self.rolling_friction.get(key):
            self.rolling_friction.pop(key)

    def get_fn(self, degrees):
        """小球对角度为degrees的斜面的正压力"""
        mg = math_utils.rotate_vector((0, self.m * gs.g), degrees)
        coe = 1 if self.v[1] < 0 else -1
        fn = math.fabs(mg[1]) * coe
        for f in self.forces:
            f1 = math_utils.rotate_vector(f.get_f(),degrees)
            fn += math.fabs(f1[1]) * coe
        return fn
