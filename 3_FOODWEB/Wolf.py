# @Author  : Mei Jiaojiao
# @Time    : 2024/2/16 20:56
# @Software: PyCharm
# @File    : Wolf.py
import numpy as np

from Animal import Animal


class Wolf(Animal):
    def __init__(self, species_type, x_radius, y_radius, lifespan, speed, energy, number_of_offspring, world_size,
                 new_births, wolf_birth_energy_cost, wolf_reproduce_energy_threshold, wolf_energy_needed_factor,
                 wolf_energy_reduction_factor, energy_gain_factor):
        super().__init__(species_type, x_radius, y_radius, lifespan, speed, energy, number_of_offspring, world_size,
                         new_births)

        self.x = self.get_x()
        self.y = self.get_y()
        self.x_radius = self.get_x_radius()
        self.y_radius = self.get_y_radius()
        self.lifespan = self.get_lifespan()
        self.speed = self.get_speed()
        self.energy = self.get_init_energy()
        self.max_offspring = self.get_max_offspring()
        self.new_birth_per_year = self.new_birth_each_time()
        self.wolf_birth_energy_cost_mean = wolf_birth_energy_cost[0]
        self.wolf_birth_energy_cost_std = wolf_birth_energy_cost[1]
        self.wolf_reproduce_energy_threshold = wolf_reproduce_energy_threshold
        self.wolf_energy_needed_factor = wolf_energy_needed_factor
        self.age = 0
        self.is_alive = True
        self.will_move = None
        self.is_too_old = False
        self.next_x = None
        self.next_y = None
        self.energy_reduction_factor = wolf_energy_reduction_factor
        self.energy_gain_factor = energy_gain_factor

    def energy_needed(self):
        return self.energy_mean * self.wolf_energy_needed_factor - self.energy

    def energy_renew(self):
        self.energy = self.energy * self.energy_gain_factor

    def too_old(self):
        if self.age < self.lifespan < self.age + 1:
            self.is_too_old = True
        return self.is_too_old

    def too_old_to_die(self):
        if self.age > self.lifespan:
            self.is_alive = False

    def too_staving_to_die(self):
        if self.energy < 0:
            self.is_alive = False

    def next_move(self, angle):
        self.next_x = self.x + self.speed * np.cos(angle)
        self.next_y = self.y + self.speed * np.sin(angle)

    def check_world_edge(self):
        if self.x < 0:
            self.x = 0
        if self.x > self.world_width:
            self.x = self.world_width
        if self.y < 0:
            self.y = 0
        if self.y > self.world_height:
            self.y = self.world_height

    def energy_cost_per_birth(self):
        return np.random.normal(self.wolf_birth_energy_cost_mean, self.wolf_birth_energy_cost_std)
