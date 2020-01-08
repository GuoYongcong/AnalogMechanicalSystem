import math
from shape.ball import Ball
from shape.rectangle import Rectangle
from shape.triangle import Triangle
from shape.force import Force
from utils import math_utils
import pygame as pg
import game_settings as gs


def contact_test(shape1, shape2):
    """
    碰撞检测
    shape1 : 主动碰撞物体
    shape2 : 被动碰撞物体
    """
    if isinstance(shape1, Ball):
        if isinstance(shape2, Ball):
            ball_contact_ball(shape1, shape2)
        elif isinstance(shape2, Rectangle):
            ball_contact_rectangle(shape1, shape2)
        elif isinstance(shape2, Triangle):
            ball_contact_triangle(shape1, shape2)
    elif isinstance(shape1, Rectangle):
        if isinstance(shape2, Ball):
            ball_contact_rectangle(shape2, shape1)
        elif isinstance(shape2, Rectangle):
            rectangle_contact_rectangle(shape1, shape2)


def ball_contact_ball(ball1, ball2):
    x = ball1.pos[0] - ball2.pos[0]
    y = ball1.pos[1] - ball2.pos[1]
    distance = math.sqrt(x ** 2 + y ** 2)
    if ball1.r + ball2.r > distance:  # 如果两个小球相撞
        # 修正两个小球的位置
        dx = dx_two_points(ball1.pos, ball2.pos, ball1.r + ball2.r)
        dy = dy_two_points(ball1.pos, ball2.pos, ball1.r + ball2.r)
        dx_coe = 1
        dy_coe = 1
        if ball1.pos[0] < ball2.pos[0]:
            dx_coe = -1
        if ball1.pos[1] < ball2.pos[1]:
            dy_coe = -1
        ball1.pos = ball1.pos[0] + \
            round(dx_coe * dx), ball1.pos[1] + round(dy_coe * dy)
        if ball2.is_free:
            # 计算两个小球碰撞后的速度
            m = (ball1.m, ball2.m)
            v_x = (ball1.v[0], ball2.v[0])
            v_y = (ball1.v[1], ball2.v[1])
            v = (v_x, v_y)
            obj = (ball1, ball2)
            for i in range(0, 2):
                new_v = [0, 0]
                for j in range(0, 2):
                    p = (i + 1) % 2
                    # x轴和y轴方向分别运用动量守恒和能量守恒定理推导出此公式
                    new_v[j] = (v[j][i] * (m[i] - m[p]) + 2 *
                                m[p] * v[j][p]) / (m[0] + m[1])
                obj[i].v = (round(new_v[0]), round(new_v[1]))  # round()四舍五入
        else:
            ball1.v = ball1.v[0] * dx_coe, ball1.v[1] * dy_coe


def ball_contact_rectangle(ball, rect):
    ball_pos = ball.pos
    rect_rect = rect.rect
    if ball_pos[0] < rect_rect.left:
        closest_x = rect_rect.left
        dx1 = -1  # ball
        dx2 = 1  # rect
    elif ball_pos[0] > rect_rect.left + rect_rect.width:
        closest_x = rect_rect.left + rect_rect.width
        dx1 = 1
        dx2 = -1
    else:
        closest_x = ball_pos[0]
        dx1 = 0
        dx2 = 0
    if ball_pos[1] < rect_rect.top:
        closest_y = rect_rect.top
        dy1 = -1    # ball
        dy2 = 1     # rect
    elif ball_pos[1] > rect_rect.top + rect_rect.height:
        closest_y = rect_rect.top + rect_rect.height
        dy1 = 1
        dy2 = -1
    else:
        closest_y = ball_pos[1]
        dy1 = 0
        dy2 = 0
    distance = math_utils.distance_of_two_points(
        ball_pos, (closest_x, closest_y))
    # 判断矩形上距离圆形的最近点与圆心的距离是否小于圆的半径
    if distance < ball.r:
        dx = dx_two_points(ball_pos, (closest_x, closest_y), ball.r)
        dx = round(dx / 2)
        dy = dy_two_points(ball_pos, (closest_x, closest_y), ball.r)
        dy = round(dy / 2)
        dx1 = dx1 * dx
        dx2 = dx2 * dx
        dy1 = dy1 * dy
        dy2 = dy2 * dy
        # ball.pos = ball.pos[0] + dx1, ball.pos[1] + dy1
        # rect.rect = rect.rect.move(dx2, dy2)


def ball_contact_triangle(ball, triangle):
    closest_point = None  # 三角形边上垂直距离圆心最近的点中，直线距离最近的点
    min_d = ball.r  # closest_point垂直距离圆心的距离
    closest_border = []
    for k in range(3):
        a = triangle.points[k]
        b = triangle.points[(k + 1) % 3]
        c = ball.pos
        #   找三角形边上距离圆心最近的点p
        ab = math_utils.sub_op(b, a)
        ac = math_utils.sub_op(c, a)
        ac_len = math_utils.v_len(ac)
        ab_len = math_utils.v_len(ab)
        if ac_len > 0:
            ap_len = math_utils.dot_op(ac, ab) / ab_len
        else:
            ap_len = 0
        if ap_len <= 0:
            p = a
        elif ap_len >= ab_len:
            p = b
        else:
            times = ap_len / ab_len
            ap = math_utils.times(ab, times)
            p = math_utils.add_op(a, ap)
        d = math_utils.distance_of_two_points(p, c)
        if d < min_d:
            min_d = d
            closest_point = p
            closest_border.clear()
            closest_border.append(a)
            closest_border.append(b)
    if min_d < ball.r:
        # 小球反弹
        v_degrees = ball.get_v_degrees()
        dy = closest_border[0][1] - closest_border[1][1]
        dx = closest_border[0][0] - closest_border[1][0]
        angle = math.degrees(math.atan2(dy, dx))   # 斜面角度
        if angle < 0:
            angle += 180
        if ball.v[1] > 0:
            angle = -angle
        degrees = 2 * (180 - v_degrees - angle)
        new_v = math_utils.rotate_vector(ball.v, degrees)
        # 假定碰撞后动能损失一半
        times = math.sqrt(1 / 2)
        new_v = math_utils.times(new_v, times)
        ball.v = round(new_v[0]), round(new_v[1])
        # pg.draw.line(
        #     ball.game_surface,
        #     pg.Color('red'),
        #     closest_border[0],
        #     closest_border[1],
        #     5)
        # 斜面对小球的支持力
        dy = closest_border[0][1] - closest_border[1][1]
        dx = closest_border[0][0] - closest_border[1][0]
        angle = math.degrees(math.atan2(dy, dx))  # 斜面角度
        f_v = ball.m * gs.g * math.cos(angle)
        f_degrees = -90 + angle
        f = Force(ball.game_surface, f_v, f_degrees, ball.pos)
        ball.append_supporting_force(hash(triangle), f)
        if min_d > 0:
            closest_point_to_ball_pos = math_utils.sub_op(
                ball.pos, closest_point)
            pos_to_new_pos = math_utils.times(
                closest_point_to_ball_pos,
                (ball.r - min_d) / min_d)
            new_pos = math_utils.add_op(pos_to_new_pos, ball.pos)
            ball.pos = round(new_pos[0]), round(new_pos[1])
    else:
        ball.delete_supporting_force(hash(triangle))


def rectangle_contact_rectangle(rect1, rect2):
    if rect2.rect.collidepoint(rect1.rect.bottomright):
        dy = rect2.rect.top - rect1.rect.bottomright[1]


def dx_two_points(p1, p2, s):
    """参数s表示修正后两点的距离"""
    ds = s - math_utils.distance_of_two_points(p1, p2)
    return ds * math.fabs(p1[0] - p2[0]) / s


def dy_two_points(p1, p2, s):
    """参数s表示修正后两点的距离"""
    ds = s - math_utils.distance_of_two_points(p1, p2)
    return ds * math.fabs(p1[1] - p2[1]) / s
