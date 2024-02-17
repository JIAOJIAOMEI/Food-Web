# @Author  : Mei Jiaojiao
# @Time    : 2024/2/16 20:39
# @Software: PyCharm
# @File    : Animal.py
import numpy as np


class Animal:
    def __init__(self, species_type, x_radius, y_radius, lifespan, speed, energy, number_of_offspring, world_size,
                 new_births):
        self.species_type = species_type
        self.x_radius_mean = x_radius[0]
        self.x_radius_std = x_radius[1]
        self.y_radius_mean = y_radius[0]
        self.y_radius_std = y_radius[1]
        self.lifespan_mean = lifespan[0]
        self.lifespan_std = lifespan[1]
        self.speed_mean = speed[0]
        self.speed_std = speed[1]
        self.energy_mean = energy[0]
        self.energy_std = energy[1]
        self.new_births_mean = new_births[0]
        self.new_births_std = new_births[1]
        self.max_offspring_mean = number_of_offspring[0]
        self.max_offspring_std = number_of_offspring[1]
        self.world_width = world_size[0]
        self.world_height = world_size[1]
        self.is_alive = True
        self.age = 0

    def get_x_radius(self):
        return np.random.normal(self.x_radius_mean, self.x_radius_std)

    def get_y_radius(self):
        return np.random.normal(self.y_radius_mean, self.y_radius_std)

    def get_lifespan(self, **kwargs):
        return np.random.normal(self.lifespan_mean, self.lifespan_std)

    def get_speed(self):
        return np.random.normal(self.speed_mean, self.speed_std)

    def get_init_energy(self):
        return np.random.normal(self.energy_mean, self.energy_std)

    def get_max_offspring(self):
        return np.random.normal(self.max_offspring_mean, self.max_offspring_std)

    def get_x(self):
        return np.random.uniform(0, self.world_width)

    def get_y(self):
        return np.random.uniform(0, self.world_height)

    def die(self):
        self.is_alive = False

    def increase_age(self):
        self.age += 1

    def new_birth_each_time(self):
        return np.random.normal(self.new_births_mean, self.new_births_std)
