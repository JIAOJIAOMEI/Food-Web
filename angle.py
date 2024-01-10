# @Author  : Mei Jiaojiao
# @Time    : 2023/11/30 17:11
# @Software: PyCharm
# @File    : angle.py

import numpy as np
import matplotlib.pyplot as plt


class Prey:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    # 创建猎物和捕食者的初始位置
    prey = Prey(10, 10)
    predator = Predator(0, 0)

    # 绘制猎物和捕食者的初始位置
    plt.scatter(prey.x, prey.y, c='green', label='prey')
    plt.scatter(predator.x, predator.y, c='red', label='predator')
    plt.plot([prey.x, predator.x], [prey.y, predator.y], c='grey', linestyle='--')

    # 追逐过程
    for timestep in range(1):
        # 计算捕食者朝着猎物的方向移动两个单位距离后的新位置
        prey_speed = 2
        predator_speed = 3
        angle = np.arctan2(prey.y - predator.y, prey.x - predator.x)
        prey.x = prey.x + np.cos(angle) * prey_speed
        prey.y = prey.y + np.sin(angle) * prey_speed
        predator.x = predator.x + np.cos(angle) * predator_speed
        predator.y = predator.y + np.sin(angle) * predator_speed
        # print('current predator position: ({}, {})'.format(predator.x, predator.y))
        print('current prey position: ({}, {})'.format(prey.x, prey.y))

        # 绘制追逐后的新位置
        plt.scatter(prey.x, prey.y, c='yellow', label='prey_new')
        plt.scatter(predator.x, predator.y, c='blue', label='predator_new')
        # plt.plot([prey.x, predator.x], [prey.y, predator.y], c='grey', linestyle='--')

    # 绘制图例和展示图形
    plt.legend()
    plt.savefig('angle.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
