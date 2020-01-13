# -*- coding:utf-8 -*-
import pygame as pg
import math
import sys
from shape import ball, force
import game_settings as gs
from random import randint
from utils import contact_utils

FPSClock = pg.time.Clock()  # 创建Clock对象
object_selected = None  # 当前选中的自由物体
sum_of_forces = 0  # 添加的力的总数
force_selected = None  # 当前选中的力


def game_init():
    pg.init()
    game_surface = pg.display.set_mode(gs.SIZE)
    pg.display.set_caption('力学模拟系统')  # 标题
    return game_surface


def check_event(game_surface, game_active, balls,
                buttons, sliders, free_objects):
    for event in pg.event.get():
        if event.type == pg.QUIT:  # 退出
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:  # 按下鼠标
            mouse_buttons = pg.mouse.get_pressed()  # 获得鼠标上三个按键的按压状态
            mouse_pos = pg.mouse.get_pos()
            game_active = check_click(
                game_surface, game_active, mouse_pos,
                mouse_buttons, buttons, sliders, free_objects)
    return game_active


def click_button_add(game_surface, game_active,
                     button_clicked, sliders, free_objects):
    if not game_active and None != object_selected:
        f = add_force(game_surface, sliders, free_objects)
        object_selected.append_force(f)
        global force_selected
        force_selected = f
        global sum_of_forces
        sum_of_forces += 1
    return game_active


def click_button_delete(game_surface, game_active,
                        button_clicked, sliders, free_objects):
    if force_selected is not None:
        object_selected.forces.remove(force_selected)
        global force_selected
        force_selected = None
        global sum_of_forces
        sum_of_forces -= 1
    return game_active


def click_button_launch(game_surface, game_active,
                        button_clicked, sliders, free_objects):
    button_clicked.set_text('暂停')
    global force_selected
    force_selected = None
    global object_selected
    object_selected = None
    game_active = True
    return game_active


def click_button_pause(game_surface, game_active,
                       button_clicked, sliders, free_objects):
    button_clicked.set_text('启动')
    game_active = False
    return game_active


# click_button_events:全局变量
click_button_events = {'添加': click_button_add,
                       '删除': click_button_delete,
                       '启动': click_button_launch,
                       '暂停': click_button_pause}


def set_value_of_force(slider, free_objects):
    f_value = slider.value
    force_selected.set_f('value', f_value)


def set_angle_of_force(slider, free_objects):
    f_angle = slider.value
    force_selected.set_f('angle', f_angle)


def set_pos_of_force(mouse_pos, free_objects):
    force_selected.set_f('pos', mouse_pos)


# set_force:全局变量
set_force = {'力的大小': set_value_of_force,
             '力的方向': set_angle_of_force}


def check_click(game_surface, game_active, mouse_pos,
                mouse_buttons, buttons, sliders, free_objects):
    for button in buttons:
        # collidepoint()函数判断鼠标是否点击了按钮
        if mouse_buttons[0] and button.button_rect.collidepoint(mouse_pos):
            button_clicked = button
            try:
                game_active = click_button_events[button.text](
                    game_surface, game_active, button_clicked, sliders, free_objects)
            except KeyError as error:
                pass
    for slider in sliders:
        # collidepoint()函数判断鼠标是否点击了slider
        if mouse_buttons[0] and slider.rect.collidepoint(mouse_pos):
            slider.change_value(mouse_pos)
            if None != force_selected:
                set_force[slider.text](slider, free_objects)

    for free_object in free_objects:
        if not game_active:
            if free_object.check_click_right(mouse_pos, mouse_buttons):
                if object_selected != free_object:
                    global object_selected
                    object_selected = free_object
                    free_object.is_selected(pg.Color('green'), 2)
                    game_active = False
            if free_object.check_click_left(mouse_pos, mouse_buttons):
                if None != force_selected and force_selected in free_object.forces:
                    set_pos_of_force(mouse_pos, free_objects)
            for f in free_object.forces:
                if f.check_click_right(mouse_pos, mouse_buttons):
                    global force_selected
                    force_selected = f
    return game_active


def get_sliders_value(sliders):
    f = 0
    a = 0
    for slider in sliders:
        if '力的大小' == slider.text:
            f = slider.value
        if '力的方向' == slider.text:
            a = slider.value
    return f, a


def add_force(surface, sliders, free_objects):

    f = 0  # 力的大小
    a = 0  # 力的方向
    f, a = get_sliders_value(sliders)
    pos = object_selected.get_center()
    F = force.Force(surface, f, a, pos)
    return F


def add_ball(game_surface, sliders):
    pos = (round(gs.SIZE[0] / 2), round(gs.SIZE[1] / 2))
    v = orthogonal_decomposition_of_velocity(sliders)
    m = 5
    colors = ['white', 'red', 'blue', 'green', 'yellow']
    color = pg.Color(colors[randint(0, 4)])
    b = ball.Ball(game_surface, pos, m, v, color)
    b.draw()
    draw_direction(b, sliders)
    pg.display.flip()
    return b


def orthogonal_decomposition_of_velocity(sliders):
    """对slider显示的力的进行正交分解，分解为v_x, v_y"""
    v = 0  # 力的大小
    a = 0  # 力的方向
    for slider in sliders:
        if slider.text == "力的大小":
            v = slider.value
        elif slider.text == "力的方向":
            a = slider.value
    v_x = (v * math.cos(math.radians(a)))  # radians()返回一个角度的弧度值
    v_y = (v * math.sin(math.radians(a)))
    return v_x, v_y


def draw_direction(ball, sliders):
    """在小球上面画力的的方向线"""
    a = 0
    for slider in sliders:
        if slider.text == "力的方向":
            a = slider.value
    color = pg.Color('black')
    start_pos = ball.pos
    x = round(ball.r * math.cos(math.radians(a)))
    y = round(ball.r * math.sin(math.radians(a)))
    end_pos = (start_pos[0] + x, start_pos[1] + y)
    width = 2
    pg.draw.line(ball.game_surface, color, start_pos, end_pos, width)


def update(game_surface, game_active, balls, buttons,
           sliders, lines, fixed_objects, free_objects):
    game_surface.fill(gs.BG_COLOR)  # 设置游戏界面的背景色，相当于清屏
    # 刷新菜单界面
    game_surface.fill(gs.BG_COLOR, pg.Rect(
        (gs.SIZE[0] - gs.MENU_SIZE[0], 0), gs.MENU_SIZE))
    for button in buttons:
        button.draw()
    for slider in sliders:
        slider.draw()
    for line in lines:
        line.draw()
    for fixed_object in fixed_objects:
        fixed_object.draw()

    display_game_active(game_surface, game_active)
    display_number_of_force(game_surface, free_objects)
    if game_active:

        width = 5
        pos_x = gs.SIZE[0] - gs.MENU_SIZE[0] - width / 2
        start_pos = (pos_x, 0)
        end_pos = (pos_x, gs.SIZE[1])

        for free_object in free_objects:
            free_object.move()
            # 跟其他自由物体进行碰撞检测
            for other_object in free_objects:
                if other_object is not free_object:
                    contact_utils.contact_test(other_object, free_object)
            # 跟其他固定物体进行碰撞检测
            for fixed_object in fixed_objects:
                contact_utils.contact_test(free_object, fixed_object)
            free_object.is_hit_the_edge(
                (gs.SIZE[0] - gs.MENU_SIZE[0], gs.SIZE[1]))
            free_object.draw()
            free_object.draw_force(pg.Color('red'))
    else:
        for free_object in free_objects:
            free_object.draw()
            free_object.draw_force(pg.Color('red'))
    if object_selected is not None:
        object_selected.is_selected(
            pg.Color('green'), 2)
    if force_selected is not None:
        if force_selected in object_selected.forces:
            force_selected.draw(pg.Color('green'))
        else:
            global force_selected
            force_selected = None

    pg.display.flip()  # 把画的东西显示出来
    FPSClock.tick(gs.FPS)


def display_text(surface, text, text_color, font_size, text_center):
    text = str(text)
    text_color = text_color  # 文本颜色
    font = pg.font.SysFont('simsunnsimsun', font_size)  # 宋体
    text_image = font.render(
        text, True, text_color)  # render()把文本变成图像
    text_image_rect = text_image.get_rect()
    text_image_rect.center = text_center
    surface.blit(text_image, text_image_rect)


def display_game_active(game_surface, game_active):
    text = ''
    if game_active:
        text = '运行'
    else:
        text = '暂停'
    display_text(game_surface, text, pg.Color('red'), 36, (800, 50))


def display_number_of_force(game_surface, free_objects):
    number = sum_of_forces
    text = '添加的力的总数：' + str(number)
    display_text(game_surface, text, pg.Color('red'), 27, (800, 100))
    if object_selected is not None:
        number = len(object_selected.forces)
    else:
        number = 0
    text = '选中的物体添加的力的数量：' + str(number)
    display_text(game_surface, text, pg.Color('red'), 27, (800, 150))
