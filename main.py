# -*- coding: utf-8 -*-
import pygame as pg
from pygame.locals import *

import game_functions as gf
import game_settings as gs
from control import slider
from control.button import Button
from shape import ball, line, polygon


def run_game():
    game_surface = gf.game_init()
    buttons = []
    balls = []
    sliders = []
    lines = []
    fixed_objects = []
    free_objects = []
    # 定义Button对象
    button_size = (80, 60)
    button_pos = (gs.SIZE[0] - button_size[0] / 2,
                  gs.SIZE[1] / 2 - button_size[1])
    button_color = (255, 140, 0)
    text = "添加"
    font_size = 30
    text_color = (255, 255, 255)
    button_add = Button(game_surface, button_size,
                        button_color, button_pos, text, font_size, text_color)
    buttons.append(button_add)
    text = "启动"
    button_pos = (gs.SIZE[0] - button_size[0] / 2,
                  gs.SIZE[1] / 2 + button_size[1])
    button_control = Button(
        game_surface,
        button_size,
        button_color,
        button_pos,
        text,
        font_size,
        text_color)
    buttons.append(button_control)

    text = "删除"
    button_color = pg.Color('red')
    button_pos = (gs.SIZE[0] - button_size[0] / 2,
                  gs.SIZE[1] / 2)
    button_undo = Button(game_surface, button_size,
                         button_color, button_pos, text, font_size, text_color)
    buttons.append(button_undo)

    # 定义Slider对象
    text = "力的大小"
    max_value = 100
    value = max_value / 2
    slider_color = Color('red')
    font_size = 18
    rect_1 = Rect(0, 0, 20, 100)
    rect_1.center = button_pos[0], (gs.SIZE[1] / 6)
    slider_1 = slider.Slider(
        game_surface,
        rect_1,
        slider_color,
        text,
        text_color,
        font_size,
        max_value,
        value,
        slider.VERTICAL)
    sliders.append(slider_1)
    text = "力的方向"
    max_value = 360
    value = max_value / 2
    rect_2 = Rect(0, 0, 20, 100)
    rect_2.center = button_pos[0], (gs.SIZE[1] * 5 / 6)
    slider_2 = slider.Slider(
        game_surface,
        rect_2,
        slider_color,
        text,
        text_color,
        font_size,
        max_value,
        value,
        slider.VERTICAL)
    sliders.append(slider_2)

    # 定义Line对象
    width = 5
    pos_x = gs.SIZE[0] - buttons[0].button_size[0]
    start_pos = (pos_x, 0)
    end_pos = (pos_x, gs.SIZE[1])
    line_1 = line.Line(game_surface, gs.LINE_COLOR,
                       start_pos, end_pos, width)
    lines.append(line_1)

    width = 5
    pos_x = gs.SIZE[0] - gs.MENU_SIZE[0] - width / 2
    start_pos = (pos_x, 0)
    end_pos = (pos_x, gs.SIZE[1])
    line_2 = line.Line(game_surface, gs.LINE_COLOR,
                       start_pos, end_pos, width)
    lines.append(line_2)

    width = 5
    pos_y = gs.SIZE[1] / 2
    start_pos = (line_1.start_pos[0], pos_y)
    end_pos = (line_2.start_pos[0], pos_y)
    line_3 = line.Line(game_surface, gs.LINE_COLOR,
                       start_pos, end_pos, width)
    lines.append(line_3)

    width = 10
    pos_x = -1
    start_pos = (pos_x, 0)
    end_pos = (pos_x, gs.SIZE[1])
    line_4 = line.Line(game_surface, gs.LINE_COLOR,
                       start_pos, end_pos, width)
    lines.append(line_4)

    # 定义固定物体
    height = gs.SIZE[1] / 8
    rect = Rect(0, gs.SIZE[1] - height, gs.SIZE[0] -
                gs.MENU_SIZE[0], height)
    points = [rect.bottomleft, rect.bottomright, rect.topright, rect.topleft]
    color = Color('white')
    cof = 0.5
    m = 50
    fixed_object_1 = polygon.Polygon(
        game_surface, points, color, cof, m, False)
    fixed_objects.append(fixed_object_1)

    # 定义自由物体
    width = gs.SIZE[0] / 5
    height = gs.SIZE[1] / 8
    left = width
    top = gs.SIZE[1] / 2 - height
    rect = Rect(left, top, width, height)
    color = Color('black')
    cof = 0.5
    m = 100
    # free_object_1 = rectangle.Rectangle(
    #     game_surface, rect, color, cof, G, True)
    points = [rect.bottomleft, rect.bottomright, rect.topright, rect.topleft]
    free_object_1 = polygon.Polygon(
        game_surface, points, color, cof, m, True)
    free_objects.append(free_object_1)

    pos = ((gs.SIZE[0] / 2) + 80, (gs.SIZE[1] / 2) + 40)
    v = (0, 0)
    m = 5
    color = pg.Color('black')
    free_object_2 = ball.Ball(game_surface, pos, m, v, color, True)
    free_objects.append(free_object_2)
    color = pg.Color('white')
    rect = Rect(0, gs.SIZE[1] - height, gs.SIZE[0] -
                gs.MENU_SIZE[0], height)
    pos = gs.SIZE[0] - gs.MENU_SIZE[0], gs.SIZE[1] - height
    # pos = (gs.SIZE[0] / 2), rect.top
    points = [(pos[0] - 250, pos[1]), (pos[0], pos[1]),
              (pos[0], pos[1] - height*2)]
    fixed_object_2 = polygon.Polygon(game_surface, points, color, cof, True)
    fixed_objects.append(fixed_object_2)
    game_active = False
    while True:
        gf.update(game_surface, game_active, balls,
                  buttons, sliders, lines, fixed_objects, free_objects)
        game_active = gf.check_event(
            game_surface, game_active, balls, buttons, sliders, free_objects)


if __name__ == '__main__':
    run_game()
