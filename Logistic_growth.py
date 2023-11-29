# @Author  : Mei Jiaojiao
# @Time    : 2023/11/29 22:48
# @Software: PyCharm
# @File    : Logistic_growth.py


import numpy as np
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age


class Population:
    def __init__(self, init_size, birth_rate, Low_death_rate, x_grid, y_grid, time, avg_lifespan):
        self.size = init_size
        self.birth_rate = birth_rate
        self.death_rate = Low_death_rate
        self.x_grid = x_grid
        self.y_grid = y_grid
        self.pop_limit = x_grid * y_grid
        self.time = time
        self.avg_lifespan = avg_lifespan
        self.agents = [Agent(np.random.rand() * x_grid, np.random.rand() * y_grid, 0) for _ in range(init_size)]
        self.population_history = [init_size]

    def logistic_growth(self, pop):
        pop_diff = self.birth_rate * pop * (1 - pop / self.pop_limit) - self.death_rate * pop
        pop_noise = int(np.random.normal(0, 0.000001 * pop_diff) * np.random.choice([-1, 1]))
        return pop_diff + pop_noise

    def death_probability(self, age, too_young, too_old):
        if age < too_young or age > too_old:  # Infants and elderly are more susceptible to death
            return High_death_rate
        else:
            return Low_death_rate

    def simulate(self):
        for t in range(1, self.time + 1):
            # Implement agent aging and death process
            new_agents = []
            for agent in self.agents:
                agent.age += 1
                if np.random.rand() < self.death_probability(agent.age, too_young, too_old):
                    continue  # Agent dies
                new_agents.append(agent)
            self.agents = new_agents

            # Implement logistic growth
            if self.size < self.pop_limit:
                self.size = max(0, self.size + self.logistic_growth(self.size))
                # Add newborn agents
                new_agents_count = int(self.logistic_growth(self.size))
                new_agents = [Agent(np.random.rand() * self.x_grid, np.random.rand() * self.y_grid, 0) for _ in
                              range(new_agents_count)]
                self.agents.extend(new_agents)

            self.population_history.append(len(self.agents))

    def plot_population(self):
        plt.figure(figsize=(10, 6))
        plt.plot(range(self.time + 1), self.population_history, label='Population size')
        plt.xlabel('Time')
        plt.ylabel('Population size')
        plt.title('Population Growth')
        plt.legend()
        plt.show()


# Set parameters
birth_rate = 0.015
Low_death_rate = 0.00001
High_death_rate = 0.0002
init_size = 100
x_grid = 50
y_grid = 50
time = 500
avg_lifespan = 70
too_young = 10
too_old = 60

# Create population and simulate
population = Population(init_size, birth_rate, Low_death_rate, x_grid, y_grid, time, avg_lifespan)
population.simulate()

# Plot population size
population.plot_population()
