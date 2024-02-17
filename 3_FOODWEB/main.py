# @Author  : Mei Jiaojiao
# @Time    : 2024/2/16 21:29
# @Software: PyCharm
# @File    : main.py
import time

import numpy as np
from tqdm import tqdm

from Fox import Fox
from ObserveEnvironment import enemies_nearby
from ObserveEnvironment import find_nearest_enemy
from ObserveEnvironment import find_nearest_prey, next_move_direction
from Predation import predation
from Rabbit import Rabbit
from Reproduction import check_reproduction_ability
from VisualizePopHistory import pop_history_plot
from Wolf import Wolf

# set the world size
world_size = [100, 100]

# rabbit eyesight
eyesight = 5

# set the number of animals
# num_wolf, num_fox, num_rabbit = 15, 85, 220
num_wolf, num_fox, num_rabbit = 15, 85, 220
# set the number of time steps
num_time_steps = 100

# set the energy seed
rabbit_energy_mean, rabbit_energy_std = 100, 20
fox_energy_mean, fox_energy_std = 150, 10
wolf_energy_mean, wolf_energy_std = 450, 10

# set new birth energy cost
rabbit_birth_energy_cost_mean, rabbit_birth_energy_cost_std = 10, 5
fox_birth_energy_cost_mean, fox_birth_energy_cost_std = 25, 10
wolf_birth_energy_cost_mean, wolf_birth_energy_cost_std = 100, 50

# set the speed seed
rabbit_speed_mean, rabbit_speed_std = 1, 0.2
fox_speed_mean, fox_speed_std = 1.7, 0.3
wolf_speed_mean, wolf_speed_std = 5, 0.5

# set the lifespan seed
rabbit_lifespan_mean, rabbit_lifespan_std = 2, 0.2
fox_lifespan_mean, fox_lifespan_std = 6, 0.5
wolf_lifespan_mean, wolf_lifespan_std = 4, 0.4

# set the offspring seed
rabbit_offspring_mean, rabbit_offspring_std = 6, 2
fox_offspring_mean, fox_offspring_std = 2.5, 1
wolf_offspring_mean, wolf_offspring_std = 2, 0.5

# set the x radius seed
rabbit_x_radius_mean, rabbit_x_radius_std = 0.8, 0.1
fox_x_radius_mean, fox_x_radius_std = 2.8, 0.2
wolf_x_radius_mean, wolf_x_radius_std = 5, 0.5

# set the y radius seed
rabbit_y_radius_mean, rabbit_y_radius_std = 0.5, 0.1
fox_y_radius_mean, fox_y_radius_std = 1.8, 0.2
wolf_y_radius_mean, wolf_y_radius_std = 5, 2

# set new births per time step
rabbit_new_births_mean, rabbit_new_births_std = 2, 0.3
fox_new_births_mean, fox_new_births_std = 1.5, 0.3
wolf_new_births_mean, wolf_new_births_std = 1.65, 0.4

# energy needed factor
rabbit_energy_needed_factor = 1.5
fox_energy_needed_factor = 1.7
wolf_energy_needed_factor = 1.2

# energy threshold for reproduction
rabbit_reproduce_energy_threshold = 0.6
fox_reproduce_energy_threshold = 0.75
wolf_reproduce_energy_threshold = 0.88

# energy_reduction_factor
rabbit_energy_reduction_factor = 0.61
fox_energy_reduction_factor = 0.2
wolf_energy_reduction_factor = 0.3

fox_energy_gain_factor = 1.1
wolf_energy_gain_factor = 1.2

rabbit_x_radius = [rabbit_x_radius_mean, rabbit_x_radius_std]
rabbit_y_radius = [rabbit_y_radius_mean, rabbit_y_radius_std]
rabbit_lifespan = [rabbit_lifespan_mean, rabbit_lifespan_std]
rabbit_speed = [rabbit_speed_mean, rabbit_speed_std]
rabbit_energy = [rabbit_energy_mean, rabbit_energy_std]
rabbit_offspring = [rabbit_offspring_mean, rabbit_offspring_std]
rabbit_new_births = [rabbit_new_births_mean, rabbit_new_births_std]
rabbit_birth_energy_cost = [rabbit_birth_energy_cost_mean, rabbit_birth_energy_cost_std]

fox_x_radius = [fox_x_radius_mean, fox_x_radius_std]
fox_y_radius = [fox_y_radius_mean, fox_y_radius_std]
fox_lifespan = [fox_lifespan_mean, fox_lifespan_std]
fox_speed = [fox_speed_mean, fox_speed_std]
fox_energy = [fox_energy_mean, fox_energy_std]
fox_offspring = [fox_offspring_mean, fox_offspring_std]
fox_new_births = [fox_new_births_mean, fox_new_births_std]
fox_birth_energy_cost = [fox_birth_energy_cost_mean, fox_birth_energy_cost_std]

wolf_x_radius = [wolf_x_radius_mean, wolf_x_radius_std]
wolf_y_radius = [wolf_y_radius_mean, wolf_y_radius_std]
wolf_lifespan = [wolf_lifespan_mean, wolf_lifespan_std]
wolf_speed = [wolf_speed_mean, wolf_speed_std]
wolf_energy = [wolf_energy_mean, wolf_energy_std]
wolf_offspring = [wolf_offspring_mean, wolf_offspring_std]
wolf_new_births = [wolf_new_births_mean, wolf_new_births_std]
wolf_birth_energy_cost = [wolf_birth_energy_cost_mean, wolf_birth_energy_cost_std]

parameters = {
    'num_rabbit': num_rabbit,
    'num_fox': num_fox,
    'num_wolf': num_wolf,
    'world_size': world_size,
    'rabbit_x_radius': rabbit_x_radius,
    'rabbit_y_radius': rabbit_y_radius,
    'rabbit_lifespan': rabbit_lifespan,
    'rabbit_speed': rabbit_speed,
    'rabbit_energy': rabbit_energy,
    'rabbit_offspring': rabbit_offspring,
    'rabbit_new_births': rabbit_new_births,
    'rabbit_birth_energy_cost': rabbit_birth_energy_cost,
    'rabbit_reproduce_energy_threshold': rabbit_reproduce_energy_threshold,
    'rabbit_energy_needed_factor': rabbit_energy_needed_factor,
    'rabbit_energy_reduction_factor': rabbit_energy_reduction_factor,
    'fox_x_radius': fox_x_radius,
    'fox_y_radius': fox_y_radius,
    'fox_lifespan': fox_lifespan,
    'fox_speed': fox_speed,
    'fox_energy': fox_energy,
    'fox_offspring': fox_offspring,
    'fox_new_births': fox_new_births,
    'fox_birth_energy_cost': fox_birth_energy_cost,
    'fox_reproduce_energy_threshold': fox_reproduce_energy_threshold,
    'fox_energy_needed_factor': fox_energy_needed_factor,
    'fox_energy_reduction_factor': fox_energy_reduction_factor,
    'wolf_x_radius': wolf_x_radius,
    'wolf_y_radius': wolf_y_radius,
    'wolf_lifespan': wolf_lifespan,
    'wolf_speed': wolf_speed,
    'wolf_energy': wolf_energy,
    'wolf_offspring': wolf_offspring,
    'wolf_new_births': wolf_new_births,
    'wolf_birth_energy_cost': wolf_birth_energy_cost,
    'wolf_reproduce_energy_threshold': wolf_reproduce_energy_threshold,
    'wolf_energy_needed_factor': wolf_energy_needed_factor,
    'wolf_energy_reduction_factor': wolf_energy_reduction_factor,
    'fox_energy_gain_factor': fox_energy_gain_factor,
    'wolf_energy_gain_factor': wolf_energy_gain_factor
}


# run the simulation
def simulation(parameters, num_time_steps, message):
    num_rabbit = parameters['num_rabbit']
    num_fox = parameters['num_fox']
    num_wolf = parameters['num_wolf']
    # pop history
    pop_history = [[num_rabbit, num_fox, num_wolf]]

    # create the animals
    rabbits_alive = [
        Rabbit('Rabbit',
               parameters['rabbit_x_radius'],
               parameters['rabbit_y_radius'],
               parameters['rabbit_lifespan'],
               parameters['rabbit_speed'],
               parameters['rabbit_energy'],
               parameters['rabbit_offspring'],
               parameters['world_size'],
               parameters['rabbit_new_births'],
               parameters['rabbit_birth_energy_cost'],
               parameters['rabbit_reproduce_energy_threshold'],
               parameters['rabbit_energy_needed_factor'],
               parameters['rabbit_energy_reduction_factor']) for _ in range(num_rabbit)]

    foxes_alive = [
        Fox('Fox',
            parameters['fox_x_radius'],
            parameters['fox_y_radius'],
            parameters['fox_lifespan'],
            parameters['fox_speed'],
            parameters['fox_energy'],
            parameters['fox_offspring'],
            parameters['world_size'],
            parameters['fox_new_births'],
            parameters['fox_birth_energy_cost'],
            parameters['fox_reproduce_energy_threshold'],
            parameters['fox_energy_needed_factor'],
            parameters['fox_energy_reduction_factor'],
            parameters['fox_energy_gain_factor']) for _ in range(num_fox)]

    wolves_alive = [
        Wolf('Wolf',
             parameters['wolf_x_radius'],
             parameters['wolf_y_radius'],
             parameters['wolf_lifespan'],
             parameters['wolf_speed'],
             parameters['wolf_energy'],
             parameters['wolf_offspring'],
             parameters['world_size'],
             parameters['wolf_new_births'],
             parameters['wolf_birth_energy_cost'],
             parameters['wolf_reproduce_energy_threshold'],
             parameters['wolf_energy_needed_factor'],
             parameters['wolf_energy_reduction_factor'],
             parameters['wolf_energy_gain_factor']) for _ in range(num_wolf)]

    for current_time in tqdm(range(1, num_time_steps + 1)):

        print(colorama.Fore.GREEN + "[INFO] Rabbits : Foxes : Wolves = ", len(rabbits_alive), " : ", len(foxes_alive),
              " : ",
              len(wolves_alive))

        if not wolves_alive or not foxes_alive or not rabbits_alive:
            print(colorama.Fore.RED + "[INFO] Species extinct at time step ", current_time)
            pop_history_plot(pop_history, message)
            break
        else:
            for wolf in wolves_alive:
                foxes_alive = predation(foxes_alive, wolf)
                if not foxes_alive:
                    print(colorama.Fore.RED + "[INFO] Foxes extinct at time step ", current_time)
                    pop_history_plot(pop_history, message)
                    break
                else:
                    continue

        if not foxes_alive:
            print(colorama.Fore.RED + "[INFO] Foxes extinct at time step ", current_time)
            pop_history_plot(pop_history, message)
            break
        else:
            for fox in foxes_alive:
                rabbits_alive = predation(rabbits_alive, fox)
                if not rabbits_alive:
                    print(colorama.Fore.RED + "[INFO] Rabbits extinct at time step ", current_time)
                    pop_history_plot(pop_history, message)
                    break
                else:
                    continue

        if not rabbits_alive:
            print(colorama.Fore.RED + "[INFO] Rabbits extinct at time step ", current_time)
            pop_history_plot(pop_history, message)
            break

        # check the rabbits if they are too old and renew their energy
        for rabbit in rabbits_alive:
            rabbit.energy_renew()
            old_rabbit = rabbit.too_old()
            rabbit.will_move = True if not old_rabbit else False

        # calculate the next move for each animal
        moving_wolves = [wolf for wolf in wolves_alive if wolf.will_move]
        for wolf in moving_wolves:
            nearest_fox = find_nearest_prey(foxes_alive, wolf)
            angle = next_move_direction(nearest_fox, wolf)
            wolf.next_move(angle)

        moving_foxes = [fox for fox in foxes_alive if fox.will_move]
        for fox in moving_foxes:
            nearest_rabbit = find_nearest_prey(rabbits_alive, fox)
            angle = next_move_direction(nearest_rabbit, fox)
            fox.next_move(angle)

        moving_rabbits = [rabbit for rabbit in rabbits_alive if rabbit.will_move]
        for rabbit in moving_rabbits:
            my_enemies_nearby = enemies_nearby(moving_foxes, rabbit, eyesight)
            if my_enemies_nearby:
                nearest_fox = find_nearest_enemy(my_enemies_nearby, rabbit)
                angle = next_move_direction(rabbit, nearest_fox)
                rabbit.next_move(angle)
            else:
                rabbit.next_x = rabbit.x
                rabbit.next_y = rabbit.y

        # move the animals
        for animal in moving_rabbits + moving_foxes + moving_wolves:
            animal.x = animal.next_x
            animal.y = animal.next_y
            animal.check_world_edge()

        # reproduce the animals
        rabbits_for_reproduction = [rabbit for rabbit in rabbits_alive if
                                    rabbit.energy > rabbit.energy_mean * rabbit_reproduce_energy_threshold and rabbit.max_offspring > 0]
        foxes_for_reproduction = [fox for fox in foxes_alive if
                                  fox.energy > fox.energy_mean * fox_reproduce_energy_threshold and fox.max_offspring > 0]
        wolves_for_reproduction = [wolf for wolf in wolves_alive if
                                   wolf.energy > wolf.energy_mean * wolf_reproduce_energy_threshold and wolf.max_offspring > 0]

        new_wolves_list = []
        for wolf in wolves_for_reproduction:
            num_of_offspring, energy_cost = check_reproduction_ability(wolf)
            if num_of_offspring > 0:
                wolf.max_offspring -= num_of_offspring

                for i in range(int(num_of_offspring)):
                    new_wolf = Wolf('Wolf', wolf_x_radius, wolf_y_radius, wolf_lifespan, wolf_speed, wolf_energy,
                                    wolf_offspring, world_size, wolf_new_births, wolf_birth_energy_cost,
                                    wolf_reproduce_energy_threshold, wolf_energy_needed_factor,
                                    wolf_energy_reduction_factor, wolf_energy_gain_factor)
                    # new_wolf.x = wolf.x + np.random.uniform(-wolf.x_radius, wolf.x_radius)
                    # new_wolf.y = wolf.y + np.random.uniform(-wolf.y_radius, wolf.y_radius)
                    # new_wolf.check_world_edge()
                    new_wolf.lifespan = new_wolf.get_lifespan() + current_time
                    new_wolves_list.append(new_wolf)
                wolf.energy -= energy_cost

        new_foxes_list = []
        for fox in foxes_for_reproduction:
            num_of_offspring, energy_cost = check_reproduction_ability(fox)
            if num_of_offspring > 0:
                fox.max_offspring -= num_of_offspring
                for i in range(num_of_offspring):
                    new_fox = Fox('Fox', fox_x_radius, fox_y_radius, fox_lifespan, fox_speed, fox_energy, fox_offspring,
                                  world_size, fox_new_births, fox_birth_energy_cost, fox_reproduce_energy_threshold,
                                  fox_energy_needed_factor, fox_energy_reduction_factor, fox_energy_gain_factor)
                    # new_fox.x = fox.x + np.random.uniform(-fox.x_radius, fox.x_radius)
                    # new_fox.y = fox.y + np.random.uniform(-fox.y_radius, fox.y_radius)
                    # new_fox.check_world_edge()
                    new_fox.lifespan = new_fox.get_lifespan() + current_time
                    new_foxes_list.append(new_fox)
                fox.energy -= energy_cost

        new_rabbits_list = []
        for rabbit in rabbits_for_reproduction:
            num_of_offspring, energy_cost = check_reproduction_ability(rabbit)
            if num_of_offspring > 0:
                rabbit.max_offspring -= num_of_offspring
                for i in range(num_of_offspring):
                    new_rabbit = Rabbit('Rabbit', rabbit_x_radius, rabbit_y_radius, rabbit_lifespan, rabbit_speed,
                                        rabbit_energy, rabbit_offspring, world_size, rabbit_new_births,
                                        rabbit_birth_energy_cost,
                                        rabbit_reproduce_energy_threshold, rabbit_energy_needed_factor,
                                        rabbit_energy_reduction_factor)
                    # new_rabbit.x = rabbit.x + np.random.uniform(-rabbit.x_radius, rabbit.x_radius)
                    # new_rabbit.y = rabbit.y + np.random.uniform(-rabbit.y_radius, rabbit.y_radius)
                    # new_rabbit.check_world_edge()
                    new_rabbit.lifespan = new_rabbit.get_lifespan() + current_time
                    new_rabbits_list.append(new_rabbit)
                rabbit.energy -= energy_cost

        print(colorama.Fore.BLUE + "[INFO] New births: ", len(new_rabbits_list), " : ", len(new_foxes_list), " : ",
              len(new_wolves_list))

        for rabbit in rabbits_alive:
            rabbit.increase_age()
            rabbit.too_old_to_die()
            rabbit.too_staving_to_die()
            rabbits_alive.remove(rabbit) if not rabbit.is_alive else None

        for fox in foxes_alive:
            fox.energy_renew()
            fox.increase_age()
            fox.too_old_to_die()
            fox.too_staving_to_die()
            foxes_alive.remove(fox) if not fox.is_alive else None

        for wolf in wolves_alive:
            wolf.increase_age()
            wolf.energy_renew()
            wolf.too_old_to_die()
            wolf.too_staving_to_die()
            wolves_alive.remove(wolf) if not wolf.is_alive else None

        for animal in rabbits_alive + foxes_alive + wolves_alive:
            animal.next_x = None
            animal.next_y = None
            animal.will_move = None

        # combine the animals
        rabbits_alive += new_rabbits_list
        foxes_alive += new_foxes_list
        wolves_alive += new_wolves_list

        # record the population history
        pop_history.append([len(rabbits_alive), len(foxes_alive), len(wolves_alive)])


import colorama

for _ in range(1):
    time.sleep(0.3)
    simulation(parameters, num_time_steps=100,message=None)

