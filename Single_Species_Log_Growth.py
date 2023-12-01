# @Author  : Mei Jiaojiao
# @Time    : 2023/11/30 08:42
# @Software: PyCharm
# @File    : Single_Species_Log_Growth.py


import matplotlib
matplotlib.use('qtagg')
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("error")


class Agent:
    def __init__(self, x, y, birth_rate, death_rate, ID, birth_time=None, status=None):
        self.ID = ID
        self.x = x
        self.y = y
        self.birth_time = birth_time if birth_time else np.random.exponential(1 / birth_rate)
        self.death_time = np.random.exponential(1 / death_rate)
        # check if birth time is larger than death time
        while self.birth_time > self.death_time:
            self.death_time = np.random.exponential(1 / death_rate)
        self.num_offspring = np.random.poisson(3)
        self.status = status


class Population:
    def __init__(self, init_size, birth_rate, death_rate, x_grid, y_grid, ID_Count):
        self.ID_Count = ID_Count
        self.size = init_size
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.x_grid = x_grid
        self.y_grid = y_grid
        self.pop_limit = x_grid * y_grid
        self.time = 0
        self.population_history = [self.size]
        self.time_history = [self.time]

        self.agents = [Agent(np.random.rand() * x_grid, np.random.rand() * y_grid,
                             birth_rate, death_rate, i, self.time, status='active') for i in range(init_size)]

    def update_agents_will_be_born(self):
        for agent in self.agents:
            if self.time - 1 <= agent.birth_time <= self.time:
                agent.status = 'active'

    def get_agents_will_die(self):
        agents_will_die = []
        for agent in self.agents:
            if self.time - 1 <= agent.death_time <= self.time:
                agent.status = 'dead'
                agents_will_die.append(agent)
        return agents_will_die

    def get_agents_alive(self):
        agents_alive = []
        for agent in self.agents:
            if agent.status == 'active':
                agents_alive.append(agent)
        return agents_alive

    def plot_population(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.time_history, self.population_history)
        plt.xlabel('time')
        plt.ylabel('population size')
        plt.title('Population size over time')
        plt.show()


def simulation(x_grid, y_grid, birth_rate, death_rate, time, init_size, location_noise=0.1):
    ID_Count = init_size
    population = Population(init_size, birth_rate, death_rate, x_grid, y_grid, ID_Count)

    for _ in tqdm(range(time)):
        population.time += 1
        population.time_history.append(population.time)

        agents_alive = population.get_agents_alive()
        population.size = len(agents_alive)
        population.population_history.append(population.size)
        for agent in agents_alive:
            while agent.num_offspring > 0:
                agent.num_offspring -= 1
                if np.random.rand() < (1 - population.size / population.pop_limit):
                    population.ID_Count += 1
                    x = agent.x + np.random.choice([-1, 1]) * np.random.rand() * location_noise
                    y = agent.y + np.random.choice([-1, 1]) * np.random.rand() * location_noise
                    new_agent = Agent(x, y, birth_rate, death_rate, population.ID_Count)
                    # update new_agent death_time
                    new_agent.birth_time += population.time
                    new_agent.death_time += population.time
                    population.agents.append(new_agent)
                    population.size += 1

        population.update_agents_will_be_born()
        agents_will_die = population.get_agents_will_die()
        for agent in agents_will_die:
            population.agents.remove(agent)

    population.plot_population()


simulation(100, 100, 0.0015, 0.001, 15000, 40)
