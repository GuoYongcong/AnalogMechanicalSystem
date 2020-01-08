# -*- coding:utf-8 -*-
import pygame as pg
import game_settings as gs
import math


class Force:

    def __init__(self, surface, value, angle, pos):
        self.surface = surface
        # 横轴正方向角度为0，顺时针为正
        self.f = {'value': value, 'angle': angle, 'pos': pos}
        self.rect = None
        self.f_x = 0
        self.f_y = 0
        self.decomposite_force()

    def decomposite_force(self):
        a = math.radians(self.f['angle'])
        self.f_x = round(self.f['value'] * math.cos(a))  # 把力分解到水平方向
        self.f_y = round(self.f['value'] * math.sin(a))  # 把力分解到竖直方向

    def set_f(self, k, v):
        self.f[k] = v
        self.decomposite_force()

    def get_f(self):
        return self.f_x, self.f_y

    def draw(self, color):
        start_pos = self.f['pos']
        end_pos = (start_pos[0] + self.f_x, start_pos[1] + self.f_y)
        width = 2
        self.rect = pg.draw.line(
            self.surface, color, start_pos, end_pos, width)
        r = 3
        pg.draw.circle(self.surface, color, start_pos, r)  # 画起点
        x = 5
        a = math.atan2(x, (self.f['value'] - x))
        b = math.sqrt((self.f['value'] - x)**2 + 4)
        c = math.radians(self.f['angle']) - a
        start_pos = (self.f['pos'][0] + b * math.cos(c),
                     self.f['pos'][1] + b * math.sin(c))
        pg.draw.line(self.surface, color, start_pos, end_pos, width)
        d = math.radians(self.f['angle']) + a
        start_pos = (self.f['pos'][0] + b * math.cos(d),
                     self.f['pos'][1] + b * math.sin(d))
        pg.draw.line(self.surface, color, start_pos, end_pos, width)

    def check_click_right(self, mouse_pos, mouse_buttons):
        if self.rect is not None:
            return mouse_buttons[2] and self.rect.collidepoint(mouse_pos)
        else:
            return False

    def get_pos(self):
        return self.f['pos']

    def set_pos(self, pos_x, pos_y):
        self.f['pos'] = pos_x, pos_y

    def get_value(self):
        return self.f['value']
