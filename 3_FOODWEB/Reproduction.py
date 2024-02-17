# @Author  : Mei Jiaojiao
# @Time    : 2024/2/17 14:24
# @Software: PyCharm
# @File    : Reproduction.py
import numpy as np


def check_reproduction_ability(animal):
    expected_births = animal.new_birth_each_time()
    expected_energy_cost_per_birth = animal.energy_cost_per_birth()
    ablitity_to_reproduce = animal.energy % expected_energy_cost_per_birth
    num_of_offspring = min(expected_births, ablitity_to_reproduce)
    num_of_offspring = int(np.floor(num_of_offspring))
    if num_of_offspring > 0:
       return num_of_offspring, expected_energy_cost_per_birth * num_of_offspring
    else:
        return 0, 0

