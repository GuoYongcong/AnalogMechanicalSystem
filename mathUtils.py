import math


def rotate_point(x, y, angle):
    angle = math.radians(angle)
    x1 = x * math.cos(angle) - y * math.sin(angle)
    y1 = x * math.sin(angle) + y * math.cos(angle)
    return round(x1), round(y1)
