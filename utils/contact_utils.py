import math

import game_settings as gs
from shape.ball import Ball
from shape.force import Force
from shape.polygon import Polygon
from utils import math_utils
import pygame as pg


def contact_test(shape1, shape2):
    """
    碰撞检测
    shape1 : 主动碰撞物体
    shape2 : 被动碰撞物体
    """
    if isinstance(shape1, Ball):
        if isinstance(shape2, Ball):
            ball_contact_ball(shape1, shape2)
        elif isinstance(shape2, Polygon):
            ball_contact_polygon(shape1, shape2)
    elif isinstance(shape1, Polygon):
        if isinstance(shape2, Polygon):
            polygon_contact_polygon(shape1, shape2)


def dx_two_points(p1, p2, s):
    """参数s表示修正后两点的距离"""
    ds = s - math_utils.distance_of_two_points(p1, p2)
    return ds * math.fabs(p1[0] - p2[0]) / s


def dy_two_points(p1, p2, s):
    """参数s表示修正后两点的距离"""
    ds = s - math_utils.distance_of_two_points(p1, p2)
    return ds * math.fabs(p1[1] - p2[1]) / s


def  get_closest_point(polygon, point):
    closest_point = None  # 多边形边上垂直距离点point最近的点中，直线距离最近的点
    min_d = gs.MAX_VALUE  # closest_point垂直距离点point的距离
    closest_border = []
    for k in range(len(polygon.points)):
        a = polygon.points[k]
        b = polygon.points[(k + 1) % len(polygon.points)]
        c = point
        #   找多边形边上距离点point最近的点p
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
    return closest_point, min_d, closest_border


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
            (dx_coe * dx), ball1.pos[1] + (dy_coe * dy)
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
                obj[i].v = ((new_v[0]), (new_v[1]))  # ()四舍五入
        else:
            ball1.v = ball1.v[0] * dx_coe, ball1.v[1] * dy_coe


def ball_contact_polygon(ball, polygon):
    # closest_point   # 多边形边上垂直距离圆心最近的点中，直线距离最近的点
    # min_d   # closest_point垂直距离圆心的距离
    # closest_border = []
    closest_point, min_d, closest_border = get_closest_point(polygon, ball.pos)
    if min_d <= ball.r:
        # 小球反弹
        v_degrees = ball.get_v_degrees()
        dy = closest_border[0][1] - closest_border[1][1]
        dx = closest_border[0][0] - closest_border[1][0]
        angle = math.degrees(math.atan2(dy, dx))  # 斜面角度
        if angle < 0:
            angle += 180
        if ball.v[1] > 0:
            angle = -angle
        degrees = 2 * (180 - v_degrees - angle)
        new_v = math_utils.rotate_vector(ball.v, degrees)
        # 假定碰撞后动能损失一半
        times = math.sqrt(1 / 2)
        new_v = math_utils.times(new_v, times)
        ball.v = (new_v[0]), (new_v[1])
        # 斜面对小球的支持力
        angle = math.degrees(math.atan2(dy, dx))  # 斜面角度
        f_v = ball.m * gs.g * math.cos(math.radians(angle))
        f_degrees = -90 + angle
        f = Force(ball.game_surface, f_v, f_degrees, ball.pos)
        ball.append_supporting_force(hash(polygon), f)
        # 斜面对小球的滚动摩擦
        min_corf = ball.corf if ball.corf < polygon.corf else polygon.corf
        dy1 = math.fabs(dy)
        dx1 = math.fabs(dx)
        degrees1 = math.degrees(math.atan2(dy1, dx1))
        fn = ball.get_fn(degrees1)
        rf_v = fn * min_corf * 100
        angle = 0  # TODO
        pos = (closest_point[0]), (closest_point[1])
        rf = Force(ball.game_surface, rf_v, angle, pos)
        # ball.append_rolling_friction(hash(polygon), rf)
        # 修正小球位置
        if min_d > 0:
            closest_point_to_ball_pos = math_utils.sub_op(
                ball.pos, closest_point)
            pos_to_new_pos = math_utils.times(
                closest_point_to_ball_pos,
                (ball.r - min_d) / min_d)
            new_pos = math_utils.add_op(pos_to_new_pos, ball.pos)
            ball.pos = (new_pos[0]), (new_pos[1])
    else:
        ball.delete_supporting_force(hash(polygon))
        # ball.delete_rolling_friction(hash(polygon))


def polygon_contact_polygon(polygon1, polygon2):

    for point in polygon1.points:
        if math_utils.point_in_polygon(polygon2.points, point) is True:
            closest_point, min_d, closest_border = get_closest_point(polygon2, point)
            if min_d > 0:
                for p in polygon1.points:
                    dy = closest_border[0][1] - closest_border[1][1]
                    dx = closest_border[0][0] - closest_border[1][0]
                    angle = math.degrees(math.atan2(dy, dx))  # 斜面角度
                    degrees = -90 + angle

                    closest_point_to_ball_pos = math_utils.sub_op(
                        p, closest_point)
                    pos_to_new_pos = math_utils.times(
                        closest_point_to_ball_pos,
                        (ball.r - min_d) / min_d)
                    new_pos = math_utils.add_op(pos_to_new_pos, ball.pos)
                    ball.pos = (new_pos[0]), (new_pos[1])
            return True

    for point in polygon2.points:
        if math_utils.point_in_polygon(polygon1.points, point) is True:
            return True
    return False

