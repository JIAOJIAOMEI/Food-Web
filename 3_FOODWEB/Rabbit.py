# @Author  : Mei Jiaojiao
# @Time    : 2024/2/16 20:47
# @Software: PyCharm
# @File    : Rabbit.py
import numpy as np
from Animal import Animal


class Rabbit(Animal):
    def __init__(self, species_type, x_radius, y_radius, lifespan, speed, energy, number_of_offspring, world_size,
                 new_births, rabbit_birth_energy_cost, rabbit_reproduce_energy_threshold, rabbit_energy_needed_factor,
                 rabbit_energy_reduction_factor):
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
        self.age = 0
        self.is_alive = True
        self.will_move = None
        self.is_too_old = False
        self.next_x = None
        self.next_y = None
        self.rabbit_birth_energy_cost_mean = rabbit_birth_energy_cost[0]
        self.rabbit_birth_energy_cost_std = rabbit_birth_energy_cost[1]
        self.rabbit_reproduce_energy_threshold = rabbit_reproduce_energy_threshold
        self.rabbit_energy_needed_factor = rabbit_energy_needed_factor
        self.energy_reduction_factor = rabbit_energy_reduction_factor

    def energy_renew(self):
        self.energy = self.energy * self.rabbit_energy_needed_factor - self.energy_mean * self.energy_reduction_factor

    def too_old(self):
        if self.age < self.lifespan < self.age + 1:
            self.is_too_old = True
        return self.is_too_old

    def next_move(self, angle):
        self.next_x = self.x + self.speed * np.cos(angle)
        self.next_y = self.y + self.speed * np.sin(angle)

    def too_old_to_die(self):
        if self.age > self.lifespan:
            self.is_alive = False

    def too_staving_to_die(self):
        if self.energy < 0:
            self.is_alive = False

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
        return np.random.normal(self.rabbit_birth_energy_cost_mean, self.rabbit_birth_energy_cost_std)
