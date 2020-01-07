import math


def rotate_point_in_pygame(fixed_point, end_point, angle):
    angle = math.radians(angle)
    x1 = end_point[0] * math.cos(angle) - end_point[1] * math.sin(angle)
    y1 = end_point[0] * math.sin(angle) + end_point[1] * math.cos(angle)

    return round(fixed_point[0] + x1), round(fixed_point[1] - y1)


def support(shape1, shape2, vector):
    """给定两个凸体，该函数返回这两个凸体明可夫斯基差形状中的一个点"""
    p1 = get_farthest_point_in_direction(shape1, vector)
    n_vector = -vector[0], -vector[1]
    p2 = get_farthest_point_in_direction(shape2, n_vector)
    return p1[0] - p2[0], p1[1] - p2[1]


def get_farthest_point_in_direction(shape, vector):
    """某个方向上选择最远的点"""
    max_value_point = shape[0][0] * vector[0] + \
        shape[0][1] * vector[1], shape[0]
    for p in shape:
        value = p[0] * vector[0] + p[1] * vector[1]
        if value > max_value_point[0]:
            max_value_point = value, p
    return max_value_point[1]


def point_in_triangle(triangle, point):
    """判断一个点是否在一个三角形中"""
    p1 = sub_op(triangle[2], triangle[0])
    p2 = sub_op(triangle[1], triangle[0])
    p3 = sub_op(point, triangle[0])
    dot11 = dot_op(p1, p1)
    dot12 = dot_op(p1, p2)
    dot13 = dot_op(p1, p3)
    dot22 = dot_op(p2, p2)
    dot23 = dot_op(p2, p3)
    temp = 1 / (dot11 * dot22 - dot12 * dot12)
    u = (dot22 * dot13 - dot12 * dot23) * temp
    if u < 0 or u > 1:
        return False
    v = (dot11 * dot23 - dot12 * dot13) * temp
    if v < 0 or v > 1:
        return False
    return u + v <= 1


def dot_op(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    return result


def add_op(vector1, vector2):
    vector = []
    for i in range(len(vector1)):
        vector.append(vector1[i] + vector2[i])
    return tuple(vector)


def sub_op(vector1, vector2):
    vector = []
    for i in range(len(vector1)):
        vector.append(vector1[i] - vector2[i])
    return tuple(vector)


def v_len(vector):
    length = 0
    for v in vector:
        length += v**2
    return math.sqrt(length)


def times(vector, t):
    new_vector = []
    for v in vector:
        new_vector.append(v * t)
    return tuple(new_vector)


def two_shapes_intersect(shape1, shape2):
    """判断两个凸多边形四是否相交"""

    return False


def distance_of_two_points(point_a, point_b):
    x = point_a[0] - point_b[0]
    y = point_a[1] - point_b[1]
    distance = math.sqrt(x**2 + y**2)
    return distance


def rotate_vector(vector, degrees):
    radians = math.radians(degrees)
    x1 = vector[0] * math.cos(radians) - vector[1] * math.sin(radians)
    y1 = vector[0] * math.sin(radians) + vector[1] * math.cos(radians)
    return round(x1), round(y1)
