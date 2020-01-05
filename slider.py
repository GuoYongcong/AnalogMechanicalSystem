from button import Button
import pygame as pg
import game_settings as gs
import copy
HORIZONTAL = 0  # 水平方向
VERTICAL = 1  # 竖直方向


class Slider:

    def __init__(self, game_surface, rect, slider_color, text, text_color, font_size, max_value, value=0, direction=HORIZONTAL):
        self.game_surface = game_surface
        self.rect = rect  # 边框矩形
        self.slider_color = slider_color  # 矩形颜色
        self.text = text  # 名称
        self.text_color = text_color  # 文本颜色
        self.font = pg.font.SysFont(
            'simsunnsimsun', font_size)  # 'simsunnsimsun'：宋体
        self.text_image = self.font.render(
            text, True, self.text_color, gs.BG_COLOR)  # render()把文本变成图像
        self.text_image_rect = self.text_image.get_rect()
        self.max_value = round(max_value)  # 最大值
        self.value = round(value)  # 当前值
        self.value_rect = copy.deepcopy(rect)  # 深拷贝
        self.value_image = self.font.render(
            str(self.value), True, self.text_color, gs.BG_COLOR)  # 数值转成图像
        self.value_image_rect = self.value_image.get_rect()
        self.direction = direction  # 方向
        if direction == HORIZONTAL:
            # 水平方向，名称和值分别显示在slider的左右两边
            self.value_rect.width = round(rect.width * value / max_value)
            self.value_rect.centerx = rect.left + self.value_rect.width / 2
            self.text_image_rect.centerx = rect.left - self.text_image_rect.width / 2
            self.text_image_rect.centery = rect.centery
            self.value_image_rect.centerx = rect.right + self.value_image_rect.width / 2
            self.value_image_rect.centery = rect.centery
        elif direction == VERTICAL:
            # 竖直方向，名称和值分别显示在slider的下上两边
            self.value_rect.height = round(rect.height * value / max_value)
            self.value_rect.centery = rect.bottom - self.value_rect.height / 2
            self.text_image_rect.centerx = rect.centerx
            self.text_image_rect.centery = rect.bottom + self.text_image_rect.height / 2
            self.value_image_rect.centerx = rect.centerx
            self.value_image_rect.centery = rect.top - self.value_image_rect.height / 2

    def draw(self):
        pg.draw.rect(self.game_surface, self.slider_color, self.rect, 1)  # 画边框
        self.game_surface.fill(self.slider_color, self.value_rect)  # 画实心矩形
        self.game_surface.blit(
            self.value_image, self.value_image_rect)  # 显示值的大小
        self.game_surface.blit(
            self.text_image, self.text_image_rect)  # 显示slider的名称

    def change_value(self, mouse_pos):
        if self.direction == HORIZONTAL:
            self.value_rect.width = round(mouse_pos.posx - self.rect.left)
            self.value_rect.centerx = self.rect.left + self.value_rect.width / 2
            self.value = round(
                self.max_value * self.value_rect.width / self.rect.width)
        elif self.direction == VERTICAL:
            self.value_rect.height = round(
                self.rect.bottom - mouse_pos[1])
            self.value_rect.centery = self.rect.bottom - self.value_rect.height / 2
            self.value = round(
                self.max_value * self.value_rect.height / self.rect.height)
        center = self.value_image_rect.center
        self.value_image = self.font.render(
            str(self.value), True, pg.Color('white'), gs.BG_COLOR)
        self.value_image_rect = self.value_image.get_rect()
        self.value_image_rect.center = center
