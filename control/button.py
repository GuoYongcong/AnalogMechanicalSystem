# -*- coding:utf-8 -*-
import pygame as pg
import game_settings as gs


class Button:

    def __init__(self, game_surface, button_size, button_color, button_pos, text, font_size, text_color):
        self.button_size = button_size  # 按钮大小
        self.button_color = button_color  # 按钮颜色
        self.game_surface = game_surface
        self.button_rect = pg.Rect((0, 0), self.button_size)
        self.button_rect.center = button_pos
        self.text = text
        self.text_color = text_color  # 文本颜色
        self.font = pg.font.SysFont('simsunnsimsun', font_size)  # 宋体
        self.text_to_image()

    def text_to_image(self):
        self.text_image = self.font.render(
            self.text, True, self.text_color, self.button_color)  # render()把文本变成图像
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.button_rect.center

    def draw(self):
        """先画按钮，在画文本图像"""
        self.game_surface.fill(self.button_color, self.button_rect)
        self.game_surface.blit(self.text_image, self.text_image_rect)

    def set_text(self, text):
        self.text = text
        self.text_to_image()
