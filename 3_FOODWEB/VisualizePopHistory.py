# @Author  : Mei Jiaojiao
# @Time    : 2024/2/16 17:27
# @Software: PyCharm
# @File    : VisualizePopHistory.py
import time

import matplotlib.pyplot as plt


def pop_history_plot(pop_history,message_show):
    plt.figure(figsize=(12, 10))

    rabbit_history = [i[0] for i in pop_history]
    fox_history = [i[1] for i in pop_history]
    wolf_history = [i[2] for i in pop_history]

    Smooth_rabbit_history = []
    Smooth_fox_history = []
    Smooth_wolf_history = []

    for i in range(len(rabbit_history)):
        if i == 0:
            Smooth_rabbit_history.append(rabbit_history[i])
            Smooth_fox_history.append(fox_history[i])
            Smooth_wolf_history.append(wolf_history[i])
        else:
            Smooth_rabbit_history.append(0.2 * rabbit_history[i] + 0.8 * Smooth_rabbit_history[i - 1])
            Smooth_fox_history.append(0.2 * fox_history[i] + 0.8 * Smooth_fox_history[i - 1])
            Smooth_wolf_history.append(0.2 * wolf_history[i] + 0.8 * Smooth_wolf_history[i - 1])

    plt.subplot(1, 1, 1)
    plt.plot([i for i in range(len(pop_history))], rabbit_history, label='rabbit', color='b')
    plt.plot([i for i in range(len(pop_history))], fox_history, label='fox', color='r')
    plt.plot([i for i in range(len(pop_history))], wolf_history, label='wolf', color='g')
    plt.xlabel('time')
    plt.ylabel('population size')
    plt.title('Population size over time')
    plt.text(0, 0, message_show, fontsize=20, color='black')
    plt.grid()
    plt.legend(loc='upper right', fontsize=10)
    # plt.subplot(2, 1, 2)
    # plt.plot([i for i in range(len(pop_history))], Smooth_rabbit_history, label='Smooth_rabbit', color='b')
    # plt.plot([i for i in range(len(pop_history))], Smooth_fox_history, label='Smooth_fox', color='r')
    # plt.plot([i for i in range(len(pop_history))], Smooth_wolf_history, label='Smooth_wolf', color='g')
    # plt.xlabel('time')
    # plt.ylabel('population size')
    # plt.title('Population size over time (smoothed)')
    # plt.grid()
    # plt.legend(loc='upper right', fontsize=10)
    plt.savefig('Population_size_over_time.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()
    plt.close()



def draw_rectangle(rabbit, fox, wolf, grid_width, grid_height):
    rabbits = [[rabbit[i].x, rabbit[i].y] for i in range(len(rabbit))]
    foxes = [[fox[i].x, fox[i].y] for i in range(len(fox))]
    wolves = [[wolf[i].x, wolf[i].y] for i in range(len(wolf))]
    plt.figure(figsize=(12, 10))
    plt.plot([0, 0], [0, grid_height], color='black')
    plt.plot([0, grid_width], [0, 0], color='black')
    plt.plot([0, grid_width], [grid_height, grid_height], color='black')
    plt.plot([grid_width, grid_width], [0, grid_height], color='black')

    for i in range(len(rabbit)):
        plt.plot([rabbit[i].x - rabbit[i].x_radius, rabbit[i].x + rabbit[i].x_radius],
                 [rabbit[i].y - rabbit[i].y_radius, rabbit[i].y - rabbit[i].y_radius], color='blue')
        plt.plot([rabbit[i].x - rabbit[i].x_radius, rabbit[i].x + rabbit[i].x_radius],
                 [rabbit[i].y + rabbit[i].y_radius, rabbit[i].y + rabbit[i].y_radius], color='blue')
        plt.plot([rabbit[i].x - rabbit[i].x_radius, rabbit[i].x - rabbit[i].x_radius],
                 [rabbit[i].y - rabbit[i].y_radius, rabbit[i].y + rabbit[i].y_radius], color='blue')
        plt.plot([rabbit[i].x + rabbit[i].x_radius, rabbit[i].x + rabbit[i].x_radius],
                 [rabbit[i].y - rabbit[i].y_radius, rabbit[i].y + rabbit[i].y_radius], color='blue')
    plt.scatter([i[0] for i in rabbits], [i[1] for i in rabbits], color='blue', s=100, label='Rabbit')

    for i in range(len(fox)):
        plt.plot([fox[i].x - fox[i].x_radius, fox[i].x + fox[i].x_radius],
                 [fox[i].y - fox[i].y_radius, fox[i].y - fox[i].y_radius], color='red')
        plt.plot([fox[i].x - fox[i].x_radius, fox[i].x + fox[i].x_radius],
                 [fox[i].y + fox[i].y_radius, fox[i].y + fox[i].y_radius], color='red')
        plt.plot([fox[i].x - fox[i].x_radius, fox[i].x - fox[i].x_radius],
                 [fox[i].y - fox[i].y_radius, fox[i].y + fox[i].y_radius], color='red')
        plt.plot([fox[i].x + fox[i].x_radius, fox[i].x + fox[i].x_radius],
                 [fox[i].y - fox[i].y_radius, fox[i].y + fox[i].y_radius], color='red')
    plt.scatter([i[0] for i in foxes], [i[1] for i in foxes], color='red', s=100, label='Fox')

    for i in range(len(wolf)):
        plt.plot([wolf[i].x - wolf[i].x_radius, wolf[i].x + wolf[i].x_radius],
                 [wolf[i].y - wolf[i].y_radius, wolf[i].y - wolf[i].y_radius], color='green')
        plt.plot([wolf[i].x - wolf[i].x_radius, wolf[i].x + wolf[i].x_radius],
                 [wolf[i].y + wolf[i].y_radius, wolf[i].y + wolf[i].y_radius], color='green')
        plt.plot([wolf[i].x - wolf[i].x_radius, wolf[i].x - wolf[i].x_radius],
                 [wolf[i].y - wolf[i].y_radius, wolf[i].y + wolf[i].y_radius], color='green')
        plt.plot([wolf[i].x + wolf[i].x_radius, wolf[i].x + wolf[i].x_radius],
                 [wolf[i].y - wolf[i].y_radius, wolf[i].y + wolf[i].y_radius], color='green')
    plt.scatter([i[0] for i in wolves], [i[1] for i in wolves], color='green', s=100, label='Wolf')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='upper right', fontsize=10)
    plt.title('Agent distribution')
    plt.grid(False)
    plt.savefig('Agent_distribution.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()

