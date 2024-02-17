# @Author  : Mei Jiaojiao
# @Time    : 2023/12/1 10:41
# @Software: PyCharm
# @File    : Two_Species_3rd.py

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tqdm import tqdm


class Species:
    def __init__(self, params):
        self.params = params
        self.x_grid = params['x_grid']
        self.y_grid = params['y_grid']
        self.species_name = params['species_name']
        self.species_average_life_span = params['species_average_life_span']
        self.species_offspring_possion_mean = params['species_offspring_possion_mean']
        self.init_species_size = params['init_species_size']
        self.activity_radius_max = params['activity_radius_max']
        self.speed_max = params['speed_max']
        self.birth_rate = params['birth_rate']

    def birth_time(self, agent, current_time):
        agent.birth_time = current_time
        return agent.birth_time

    def death_time(self, agent, current_time):
        agent.death_time = np.random.poisson(self.species_average_life_span) + current_time
        return agent.death_time

    def num_offspring(self, agent):
        agent.num_offspring = np.random.poisson(self.species_offspring_possion_mean)
        return agent.num_offspring

    def activity_radius(self, agent):
        mean = self.activity_radius_max / 2
        std = self.activity_radius_max / 6
        agent.activity_radius = np.random.normal(mean, std)
        return agent.activity_radius


class Prey(Species):
    def __init__(self, ID, x, y, params, current_time, status=None):
        super().__init__(params)
        self.ID = ID
        self.birth_time = self.birth_time(self, current_time)
        self.death_time = self.death_time(self, current_time)
        self.num_offspring = self.num_offspring(self)
        self.activity_radius = self.activity_radius(self)
        self.status = status
        self.x = np.random.rand() * self.x_grid if x is None else x
        self.y = np.random.rand() * self.y_grid if y is None else y
        self.speed = np.random.rand() * self.speed_max
        self.being_caught = False

    def enemy_action(self, current_time, predators):
        if not self.being_caught:
            for predator in predators:
                distance = np.sqrt((self.x - predator.x) ** 2 + (self.y - predator.y) ** 2)
                if distance <= (self.activity_radius + predator.activity_radius):
                    self.being_caught = True
                    time_for_predation = 1
                    self.death_time = time_for_predation + current_time
                    predator.death_time += time_for_predation
                    for _ in range(2):
                        if np.random.rand() < predator.birth_rate:
                            predator.num_offspring += 1
                elif distance <= self.activity_radius_max + predator.activity_radius_max:
                    angle = np.arctan2(self.y - predator.y, self.x - predator.x)
                    # for prey, it should run away from predator
                    self.x = self.x + np.cos(angle) * self.speed
                    self.y = self.y + np.sin(angle) * self.speed
                    # for predator, it should chase prey
                    predator.x = predator.x + np.cos(angle) * predator.speed
                    predator.y = predator.y + np.sin(angle) * predator.speed
                    # if self.x > self.x_grid:
                    #     self.status = 'dead'
                    # elif self.x < 0:
                    #     self.status = 'dead'
                    # if self.y > self.y_grid:
                    #     self.status = 'dead'
                    # elif self.y < 0:
                    #     self.status = 'dead'
                    # if predator.x > self.x_grid:
                    #     predator.status = 'dead'
                    # elif predator.x < 0:
                    #     predator.status = 'dead'
                    # if predator.y > self.y_grid:
                    #     predator.status = 'dead'
                    # elif predator.y < 0:
                    #     predator.status = 'dead'
                    if self.x > self.x_grid:
                        self.x = self.x_grid
                    elif self.x < 0:
                        self.x = 0
                    if self.y > self.y_grid:
                        self.y = self.y_grid
                    elif self.y < 0:
                        self.y = 0
                    if predator.x > self.x_grid:
                        predator.x = self.x_grid
                    elif predator.x < 0:
                        predator.x = 0
                    if predator.y > self.y_grid:
                        predator.y = self.y_grid
                    elif predator.y < 0:
                        predator.y = 0
                else:
                    pass


def generate_new_offspring(population, current_time, ID_Count):
    new_offspring = []
    current_pop_size = len(population)
    for agent in population:
        while agent.num_offspring > 0:
            if np.random.rand() < agent.birth_rate:
                agent.num_offspring -= 1
                # prepare for new offspring
                ID = ID_Count
                ID_Count += 1
                x = agent.x + np.random.normal(0, 1) * np.random.choice([-1, 1])
                y = agent.y + np.random.normal(0, 1) * np.random.choice([-1, 1])
                if agent.species_name == 'prey':
                    new_offspring.append(Prey(ID, x, y, prey_params, current_time + 1, None))
                if agent.species_name == 'predator':
                    new_offspring.append(Predator(ID, x, y, predator_params, current_time + 1, None))
                current_pop_size += 1
            else:
                break
    return new_offspring, ID_Count


class Predator(Species):
    def __init__(self, ID, x, y, params, current_time, status=None):
        super().__init__(params)
        self.ID = ID
        self.birth_time = self.birth_time(self, current_time)
        self.death_time = self.death_time(self, current_time)
        self.num_offspring = self.num_offspring(self)
        self.activity_radius = self.activity_radius(self)
        self.status = status
        self.x = np.random.rand() * self.x_grid if x is None else x
        self.y = np.random.rand() * self.y_grid if y is None else y
        self.speed = np.random.rand() * self.speed_max
        self.eat = False
        self.not_eat = 0

    def prey_action(self, current_time, preys):
        for prey in preys:
            if prey.being_caught:
                continue
            else:
                distance = np.sqrt((self.x - prey.x) ** 2 + (self.y - prey.y) ** 2)
                if distance <= (self.activity_radius + prey.activity_radius):
                    prey.being_caught = True
                    self.eat = True
                    time_for_predation = 1
                    prey.death_time = time_for_predation + current_time
                    self.death_time += time_for_predation
                    for _ in range(2):
                        if np.random.rand() < self.birth_rate:
                            self.num_offspring += 1
                elif distance <= self.activity_radius_max + prey.activity_radius_max:
                    angle = np.arctan2(self.y - prey.y, self.x - prey.x)
                    # for predator, it should chase prey
                    self.x = self.x + np.cos(angle) * self.speed
                    self.y = self.y + np.sin(angle) * self.speed
                    # for prey, it should run away from predator
                    prey.x = prey.x + np.cos(angle) * prey.speed
                    prey.y = prey.y + np.sin(angle) * prey.speed
                    # if self.x > self.x_grid:
                    #     self.status = 'dead'
                    # elif self.x < 0:
                    #     self.status = 'dead'
                    # if self.y > self.y_grid:
                    #     self.status = 'dead'
                    # elif self.y < 0:
                    #     self.status = 'dead'
                    # if prey.x > self.x_grid:
                    #     prey.status = 'dead'
                    # elif prey.x < 0:
                    #     prey.status = 'dead'
                    # if prey.y > self.y_grid:
                    #     prey.status = 'dead'
                    # elif prey.y < 0:
                    #     prey.status = 'dead'
                    if self.x > self.x_grid:
                        self.x = self.x_grid
                    elif self.x < 0:
                        self.x = 0
                    if self.y > self.y_grid:
                        self.y = self.y_grid
                    elif self.y < 0:
                        self.y = 0
                    if prey.x > self.x_grid:
                        prey.x = self.x_grid
                    elif prey.x < 0:
                        prey.x = 0
                    if prey.y > self.y_grid:
                        prey.y = self.y_grid
                    elif prey.y < 0:
                        prey.y = 0
                else:
                    pass


def update_predators_status(population, current_time):
    for agent in population:
        if current_time - 1 <= agent.death_time <= current_time:
            agent.status = 'dead'
        elif current_time - 1 <= agent.birth_time <= current_time:
            agent.status = 'active'
        if not agent.eat:
            agent.not_eat += 1
        if agent.not_eat == 2:
            agent.status = 'dead'


def update_prey_status(population, current_time):
    for agent in population:
        if current_time - 1 <= agent.death_time <= current_time:
            agent.status = 'dead'
        elif current_time - 1 <= agent.birth_time <= current_time:
            agent.status = 'active'


# Prey and Predator params
x_grid = 28
y_grid = 28
time = 200
prey_params = {
    'x_grid': x_grid,
    'y_grid': y_grid,
    'species_name': 'prey',
    'species_average_life_span': 20,
    'species_offspring_possion_mean': 3,
    'init_species_size': 60,
    'activity_radius_max': 2,
    'speed_max': 2,
    'birth_rate': 0.35
}
predator_params = {
    'x_grid': x_grid,
    'y_grid': y_grid,
    'species_name': 'predator',
    'species_average_life_span': 8,
    'species_offspring_possion_mean': 0.7,
    'init_species_size': 30,
    'activity_radius_max': 3,
    'speed_max': 4,
    'birth_rate': 0.35
}

# Create prey and predator populations
preys = [Prey(i, None, None, prey_params, 0, 'active') for i in range(prey_params['init_species_size'])]
predators = [Predator(i, None, None, predator_params, 0, 'active') for i in
             range(predator_params['init_species_size'])]

# show all the radius of preys
# for prey in preys:
#     print(prey.activity_radius)
#
# # show all the radius of predators
# for predator in predators:
#     print(predator.activity_radius)


def Current_landscape(preys, predators, curren_time):
    prey_pos = np.array([[prey.x, prey.y] for prey in preys])
    prey_radius = [prey.activity_radius for prey in preys]
    predator_pos = np.array([[predator.x, predator.y] for predator in predators])
    predator_radius = [predator.activity_radius for predator in predators]

    prey_image = OffsetImage(plt.imread('prey.png'), zoom=0.01)
    predator_image = OffsetImage(plt.imread('predator.png'), zoom=0.035)

    plt.figure(figsize=(10, 6))
    plt.scatter(prey_pos[:, 0], prey_pos[:, 1], s=10, label='prey')
    plt.scatter(predator_pos[:, 0], predator_pos[:, 1], s=10, label='predator')

    for i in range(len(prey_pos)):
        imagebox = AnnotationBbox(prey_image, prey_pos[i], frameon=False, alpha=1)
        plt.gcf().gca().add_artist(imagebox)
        circle = plt.Circle(prey_pos[i], prey_radius[i], color='b', fill=False)
        plt.gcf().gca().add_artist(circle)

    for i in range(len(predator_pos)):
        imagebox = AnnotationBbox(predator_image, predator_pos[i], frameon=False, alpha=1)
        plt.gcf().gca().add_artist(imagebox)
        circle = plt.Circle(predator_pos[i], predator_radius[i], color='r', fill=False)
        plt.gcf().gca().add_artist(circle)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='upper right', fontsize=10)
    plt.title('Current Landscape')
    plt.savefig('Current_Landscape' + str(curren_time) + '.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()


def pop_history_plot(pop_history):
    plt.figure(figsize=(12, 10))
    prey_history = [i[0] for i in pop_history]
    predator_history = [i[1] for i in pop_history]
    Smooth_prey_history = []
    Smooth_predator_history = []
    for i in range(len(prey_history)):
        if i == 0:
            Smooth_prey_history.append(prey_history[i])
            Smooth_predator_history.append(predator_history[i])
        else:
            Smooth_prey_history.append(0.2 * prey_history[i] + 0.8 * Smooth_prey_history[i - 1])
            Smooth_predator_history.append(0.2 * predator_history[i] + 0.8 * Smooth_predator_history[i - 1])

    # subplot 1
    plt.subplot(2, 1, 1)
    plt.plot([i for i in range(len(pop_history))], [i[0] for i in pop_history], label='prey', color='b')
    plt.plot([i for i in range(len(pop_history))], [i[1] for i in pop_history], label='predator', color='r')
    plt.xlabel('time')
    plt.ylabel('population size')
    plt.title('Population size over time')
    plt.grid()
    plt.legend(loc='upper right', fontsize=10)
    plt.subplot(2, 1, 2)
    plt.plot([i for i in range(len(pop_history))], Smooth_prey_history, label='Smooth_prey', color='b', linestyle='--')
    plt.plot([i for i in range(len(pop_history))], Smooth_predator_history, label='Smooth_predator', color='r',
             linestyle='--')
    plt.xlabel('time')
    plt.ylabel('population size')
    plt.title('Population size over time')
    plt.grid()
    plt.legend(loc='upper right', fontsize=10)
    plt.savefig('Population_size_over_time.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()


# create main function
if __name__ == '__main__':
    # set time

    # set ID
    Prey_ID_Count = prey_params['init_species_size']
    Predator_ID_Count = predator_params['init_species_size']
    # set pop_history
    pop_history = []

    for current_time in tqdm(range(1, time + 1)):
        # print('current time: ', current_time)

        # get alive prey and predator
        preys_alive = [prey for prey in preys if prey.status == 'active']
        predators_alive = [predator for predator in predators if predator.status == 'active']

        # record population history
        pop_history.append([len(preys_alive), len(predators_alive)])
        print('prey and predator population size: ',pop_history[-1])

        # check distance between prey and predator
        for prey in preys_alive:
            prey.enemy_action(current_time, predators_alive)
        for predator in predators_alive:
            predator.prey_action(current_time, preys_alive)

        # generate new offspring
        preys_new_offspring, Prey_ID_Count = generate_new_offspring(preys_alive, current_time, Prey_ID_Count)
        predators_new_offspring, Predator_ID_Count = generate_new_offspring(predators_alive, current_time,
                                                                            Predator_ID_Count)

        # update if prey and predator are alive
        update_prey_status(preys, current_time)
        update_predators_status(predators, current_time)

        # add new offspring to population
        preys.extend(preys_new_offspring)
        predators.extend(predators_new_offspring)

        if len(preys_alive) == 0:
            print('all prey are dead')
            break

        if len(predators_alive) == 0:
            print('all predator are dead')
            break

    pop_history_plot(pop_history)