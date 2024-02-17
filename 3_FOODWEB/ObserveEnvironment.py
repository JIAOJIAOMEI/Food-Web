# @Author  : Mei Jiaojiao
# @Time    : 2024/2/16 18:08
# @Software: PyCharm
# @File    : ObserveEnvironment.py
import numpy as np


def preys_within_range(prey_pop, predator):
    preys_nearby = []
    for i in range(len(prey_pop)):
        if abs(predator.x - prey_pop[i].x) > predator.x_radius or abs(predator.y - prey_pop[i].y) > predator.y_radius:
            continue
        else:
            preys_nearby.append(prey_pop[i])
    return preys_nearby


def enemies_nearby(enemy_pop, prey, eyesight):
    enemies_nearby_list = []
    for i in range(len(enemy_pop)):
        if abs(prey.x - enemy_pop[i].x) > eyesight * prey.x_radius or abs(
                prey.y - enemy_pop[i].y) > eyesight * prey.y_radius:
            continue
        else:
            enemies_nearby_list.append(enemy_pop[i])
    return enemies_nearby_list


def find_nearest_prey(preys_nearby, predator):
    distance = []
    for i in range(len(preys_nearby)):
        distance.append(abs(preys_nearby[i].x - predator.x) + abs(preys_nearby[i].y - predator.y))
    nearest_prey = preys_nearby[distance.index(min(distance))]
    return nearest_prey


def find_nearest_enemy(predators_pop, prey):
    distance = []
    for i in range(len(predators_pop)):
        distance.append(abs(predators_pop[i].x - prey.x) + abs(predators_pop[i].y - prey.y))
    nearest_predator = predators_pop[distance.index(min(distance))]
    return nearest_predator


def next_move_direction(prey, predator):
    angle = np.arctan2(prey.y - predator.y, prey.x - predator.x)
    return angle


def custom_compare(item):
    return item[0], item[1].energy, item[1].age


def energy_consume_weights(nearby_preys, predator):
    if len(nearby_preys) == 1:
        return nearby_preys, [1]
    else:
        distance = [np.sqrt((predator.x - prey.x) ** 2 + (predator.y - prey.y) ** 2) for prey in nearby_preys]
        sum_distance = sum(distance)
        distance_prey = list(zip(distance, nearby_preys))
        distance_prey.sort(reverse=False, key=custom_compare)
        distance, nearby_preys = zip(*distance_prey)
        weights = [d / sum_distance for d in distance]
        weights.sort(reverse=True)
    return nearby_preys, weights
