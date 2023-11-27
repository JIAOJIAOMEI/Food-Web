# @Author  : Mei Jiaojiao
# @Time    : 2023/11/23 16:37
# @Software: PyCharm
# @File    : IBMs_single.py

# import packages
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# parameters
mean_body_mass = 23
std_body_mass = 3
pop_size = 10
grid_size_x = 100
grid_size_y = 100
mean_move_dist = 0
std_move_dist = 1
time_steps = 10
possion_lambda = 4
reproduce_threshold = 4
natural_death_threshold = 0.6 * possion_lambda

# process parameters
time_steps_counter = 0
population_counter = []


# individual class 2D case
class Individual:
    def __init__(self, x, y):
        self.body_mass = np.random.normal(mean_body_mass, std_body_mass)
        self.previous_x = [x]
        self.previous_y = [y]
        self.current_x = x
        self.current_y = y
        self.age = np.random.poisson(possion_lambda)
        self.dead = False


def plot_population(population):
    plt.figure(figsize=(10, 10))
    plt.xlim(0, grid_size_x)
    plt.ylim(0, grid_size_y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Current population')
    plt.scatter([ind.current_x for ind in population], [ind.current_y for ind in population],
                s=[ind.body_mass for ind in population], c='r', alpha=0.5)
    plt.show()


def move_individual(ind):
    # move distance
    move_x = np.random.normal(mean_move_dist, std_move_dist)
    move_y = np.random.normal(mean_move_dist, std_move_dist)
    # update position
    ind.previous_x.append(ind.current_x)
    ind.previous_y.append(ind.current_y)
    ind.current_x += move_x
    ind.current_y += move_y
    # boundary conditions
    if ind.current_x < 0:
        ind.current_x = 0
    elif ind.current_x > grid_size_x:
        ind.current_x = grid_size_x
    if ind.current_y < 0:
        ind.current_y = 0
    elif ind.current_y > grid_size_y:
        ind.current_y = grid_size_y
    return ind


def reproduce_individual(ind):
    # reproduce number
    reproduce_num = np.random.choice([i for i in range(reproduce_threshold+1)])
    # make some new individuals
    new_individuals = [Individual(ind.current_x, ind.current_y) for _ in range(reproduce_num)]
    # set age to 0
    for new_ind in new_individuals:
        new_ind.age = 0
    return new_individuals


def natural_death(ind):
    if ind.age > natural_death_threshold:
        ind.dead = True
    return ind


def competition_death(ind, population):
    # check if there are multiple individuals in the same place
    # if so, the one with smaller body mass dies
    for other_ind in population:
        if other_ind.current_x == ind.current_x and other_ind.current_y == ind.current_y:
            if other_ind.body_mass < ind.body_mass:
                other_ind.dead = True
            else:
                ind.dead = True
    return ind


if __name__ == '__main__':
    population = [Individual(np.random.randint(0, grid_size_x), np.random.randint(0, grid_size_y)) for _ in
                  range(pop_size)]
    for _ in tqdm(range(time_steps)):
        population = [ind for ind in population if ind.dead == False]
        population_counter.append(len(population))
        new_individuals_list = []
        update_individuals_list = []
        for ind in population:
            ind = move_individual(ind)
            new_individuals = reproduce_individual(ind)
            new_individuals_list.extend(new_individuals)
            ind.age += 1
            ind = natural_death(ind)
            ind = competition_death(ind, population)
            update_individuals_list.append(ind)
        population = update_individuals_list
        population.extend(new_individuals_list)
    plt.figure(figsize=(10, 10))
    plt.plot(range(len(population_counter)), population_counter)
    plt.xlabel('Time steps')
    plt.ylabel('Population')
    plt.title('Population vs Time')
    plt.show()
