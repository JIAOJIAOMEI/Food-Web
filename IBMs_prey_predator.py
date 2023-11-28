# @Author  : Mei Jiaojiao
# @Time    : 2023/11/27 15:15
# @Software: PyCharm
# @File    : IBMs_prey_predator.py

# import packages
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# parameters
prey_mean_body_mass = 23
prey_std_body_mass = 3
prey_pop_size = 1000
grid_size_x = 10
grid_size_y = 10
prey_mean_move_dist = 0
prey_std_move_dist = 1
predator_mean_move_dist = 0.5
predator_std_move_dist = 1
time_steps = 10
prey_possion_lambda = 4
predator_possion_lambda = 6
prey_reproduce_threshold = 2
prey_natural_death_threshold = 0.9 * prey_possion_lambda
predator_pop_size = 100000
predator_natrual_death_threshold = 0.8 * predator_possion_lambda
predator_search_radius = 10

# process parameters
time_steps_counter = 0


# individual class 2D case
class Prey:
    def __init__(self, x, y):
        self.body_mass = np.random.normal(prey_mean_body_mass, prey_std_body_mass)
        self.previous_x = [x]
        self.previous_y = [y]
        self.current_x = x
        self.current_y = y
        self.age = np.random.poisson(prey_possion_lambda)
        self.dead = False


class Predator:
    def __init__(self, x, y):
        self.previous_x = [x]
        self.previous_y = [y]
        self.current_x = x
        self.current_y = y
        self.age = np.random.poisson(predator_possion_lambda)
        self.dead = True
        self.reproduce = False


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


def move_individual(ind, mean_move_dist, std_move_dist):
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


def prey_reproduce_individual(ind):
    # reproduce number
    reproduce_num = np.random.choice([i for i in range(prey_reproduce_threshold + 1)])
    # make some new individuals
    new_individuals = [Prey(ind.current_x, ind.current_y) for _ in range(reproduce_num)]
    # set age to 0
    for new_ind in new_individuals:
        new_ind.age = 0
    return new_individuals


def prey_natural_death(ind):
    if ind.age > prey_natural_death_threshold:
        ind.dead = True
    return ind


def predator_natrual_death(ind):
    if ind.age > predator_natrual_death_threshold:
        ind.dead = True
    return ind


def prey_competition_death(ind, population):
    # check if there are multiple individuals in the same place
    # if so, the one with smaller body mass dies
    for other_ind in population:
        if other_ind.current_x == ind.current_x and other_ind.current_y == ind.current_y:
            if other_ind.body_mass < ind.body_mass:
                other_ind.dead = True
            else:
                ind.dead = True
    return ind


def predation(predator, predator_pop, prey_pop, predator_search_radius):
    preys_found = []
    predators_found = []
    prey_distance_list = []
    predator_distance_list = []
    new_predator_pop = []
    for prey in prey_pop:
        distance = np.sqrt((prey.current_x - predator.current_x) ** 2 + (prey.current_y - predator.current_y) ** 2)
        prey_distance_list.append(distance)
        if distance <= predator_search_radius:
            preys_found.append(prey)
    predator_pop.remove(predator)
    if len(predator_pop) > 0:
        for other_predator in predator_pop:
            distance = np.sqrt(
                (other_predator.current_x - predator.current_x) ** 2 + (other_predator.current_y - predator.current_y) ** 2)
            predator_distance_list.append(distance)
            if distance <= predator_search_radius:
                predators_found.append(other_predator)

    if len(preys_found) - len(predators_found) == 0:
        for i in range(len(preys_found)):
            prey = preys_found[i]
            predator = predators_found[i]
            prey.dead = True
            predator.dead = False
            predator.previous_x.append(predator.current_x)
            predator.previous_y.append(predator.current_y)
            predator.current_x = prey.current_x
            predator.current_y = prey.current_y
            predator.age += 1

    elif len(preys_found) - len(predators_found) > 0:
        predator.reproduce = True
        for i in range(len(predators_found)):
            prey = preys_found[i]
            predator = predators_found[i]
            prey.dead = True
            predator.dead = False
            predator.previous_x.append(predator.current_x)
            predator.previous_y.append(predator.current_y)
            predator.current_x = prey.current_x
            predator.current_y = prey.current_y
            predator.age += 1
        # reproduce
        if predator.reproduce:
            new_predator_pop = [Predator(predator.current_x+np.random.normal(0,1), predator.current_y+np.random.normal(0,1)) for _ in range(2)]
            predator.reproduce = False
            new_predator_pop.extend(new_predator_pop)

    return new_predator_pop, preys_found, predators_found


def simulation():
    prey_pop = [Prey(np.random.randint(0, grid_size_x), np.random.randint(0, grid_size_y)) for _ in
                range(prey_pop_size)]
    predator_pop = [Predator(np.random.randint(0, grid_size_x), np.random.randint(0, grid_size_y)) for _ in
                    range(predator_pop_size)]
    prey_pop_counter = []
    predator_pop_counter = []
    for _ in tqdm(range(time_steps)):
        prey_pop = [ind for ind in prey_pop if ind.dead == False]
        prey_pop_counter.append(len(prey_pop))
        predator_pop_counter.append(len([ind for ind in predator_pop if ind.dead == False]))
        new_prey_pop = []
        new_predator_pop = []
        # prey move
        for i in range(len(prey_pop)):
            prey_pop[i] = move_individual(prey_pop[i], prey_mean_move_dist, prey_std_move_dist)
        for i in range(len(prey_pop)):
            prey_pop[i] = prey_competition_death(prey_pop[i], prey_pop)
        for i in range(len(prey_pop)):
            new_prey_pop.extend(prey_reproduce_individual(prey_pop[i]))
        # predators move
        for i in range(len(predator_pop)):
            predator_pop[i] = move_individual(predator_pop[i], predator_mean_move_dist, predator_std_move_dist)
        # predation
        predator_checked_list = []
        preys_checked_list = []
        while len(predator_pop) > 0:
            predator = predator_pop[0]
            new_predator_pop, preys_found, predators_found = predation(predator, predator_pop, prey_pop,
                                                                       predator_search_radius)
            new_predator_pop.extend(new_predator_pop)
            predator_checked_list.extend(predators_found)
            preys_checked_list.extend(preys_found)
            if preys_found:
                for prey in preys_found:
                    prey_pop.remove(prey)
            if predators_found:
                for predator in predators_found:
                    predator_pop.remove(predator)
        prey_pop = preys_checked_list
        predator_pop = predator_checked_list
        for i in range(len(predator_pop)):
            predator_pop[i] = predator_natrual_death(predator_pop[i])
        prey_pop.extend(new_prey_pop)
        predator_pop.extend(new_predator_pop)

    return prey_pop_counter, predator_pop_counter


if __name__ == '__main__':
    prey_pop_counter, predator_pop_counter = simulation()
    plt.figure(figsize=(10, 10))
    plt.plot(range(len(prey_pop_counter)), prey_pop_counter, color='b', alpha=0.5, linestyle='--',label='prey')
    plt.plot(range(len(predator_pop_counter)), predator_pop_counter, color='r', alpha=0.5, linestyle='--',label='predator')
    plt.legend()
    plt.show()
