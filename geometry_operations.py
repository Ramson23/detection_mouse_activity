import math

def get_angle(x_1, y_1, x_2, y_2):

    """угол измеряется от -180 до 180 градусов;
       в данном случае измеряется угол между осью Ох и вектором
    """

    if x_2 == x_1:
        return 90 if y_2 > y_1 else -90

    alfa = math.atan(abs(y_2 - y_1) / abs(x_2 - x_1)) * 180 / math.pi
    if x_2 < x_1:
        if y_2 > y_1:
            alfa = 180 - alfa
        else:
            alfa = -180 + alfa
    else:
        if y_2 < y_1:
            alfa = -alfa

    return alfa

def get_dist(x_1, y_1, x_2, y_2):
    return math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)