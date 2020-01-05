import math


def rotate_point(x, y, angle):
    angle = math.radians(angle)
    x1 = x * math.cos(angle) - y * math.sin(angle)
    y1 = x * math.sin(angle) + y * math.cos(angle)
    return round(x1), round(y1)


def support(shape1, shape2, vector):
    """给定两个凸体，该函数返回这两个凸体明可夫斯基差形状中的一个点"""
    p1 = get_farthest_point_in_direction(shape1, vector)
    n_vector = -vector[0], -vector[1]
    p2 = get_farthest_point_in_direction(shape2, n_vector)
    return p1[0]-p2[0], p1[1] - p2[1]


def get_farthest_point_in_direction(shape, vector):
    """某个方向上选择最远的点"""
    max_value_point = shape[0][0]*vector[0] + shape[0][1]*vector[1], shape[0]
    for p in shape:
        value = p[0] * vector[0] + p[1] * vector[1]
        if value > max_value_point[0]:
            max_value_point = value, p
    return max_value_point[1]

