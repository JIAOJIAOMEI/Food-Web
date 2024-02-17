# @Author  : Mei Jiaojiao
# @Time    : 2024/2/3 13:46
# @Software: PyCharm
# @File    : Agent based 3 species food web.py

# import libraries
import math
import numpy as np
import matplotlib.pyplot as plt
import random


def boundry_detect(current_pozition, circle_center, radius):
    '''
    judge if a point is included in a circle, if it is out of the circle, return the nearest point on the circle
    :param current_pozition:
    :param circle_center:
    :param radius:
    :return:
    '''
    distance = math.sqrt((current_pozition[0] - circle_center[0]) ** 2 + (current_pozition[1] - circle_center[1]) ** 2)
    if distance > radius:
        x = circle_center[0] + radius * (current_pozition[0] - circle_center[0]) / distance
        y = circle_center[1] + radius * (current_pozition[1] - circle_center[1]) / distance
        return [x, y]
    else:
        return current_pozition

