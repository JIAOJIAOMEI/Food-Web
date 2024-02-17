# @Author  : Mei Jiaojiao
# @Time    : 2024/2/17 12:53
# @Software: PyCharm
# @File    : Predation.py
from ObserveEnvironment import preys_within_range, energy_consume_weights


def predation(preys_pop, predator):
    olf_flag = predator.too_old()
    energy_needed = predator.energy_needed()
    if energy_needed > 0:
        nearby_preys = preys_within_range(preys_pop, predator)
        if nearby_preys:
            nearby_energy = sum([prey.energy for prey in nearby_preys])
            if nearby_energy > energy_needed:
                nearby_preys, weights = energy_consume_weights(nearby_preys, predator)
                energy_consumption = [energy_needed * w for w in weights]
                predator.energy = predator.energy + sum(
                    [min(energy_consumption[i], nearby_preys[i].energy) for i in range(len(nearby_preys))])
                predator.energy = predator.energy - predator.energy_mean * predator.energy_reduction_factor
                for k in range(len(nearby_preys)):
                    nearby_preys[k].energy = nearby_preys[k].energy - energy_consumption[k]
                    if nearby_preys[k].energy <= 0:
                        nearby_preys[k].die()
                        preys_pop.remove(nearby_preys[k])
                predator.will_move = False
            else:
                predator.energy = predator.energy + nearby_energy
                predator.energy = predator.energy - predator.energy_mean * predator.energy_reduction_factor
                predator.will_move = True if not olf_flag else False

                for prey in nearby_preys:
                    prey.die()
                    preys_pop.remove(prey)
        else:
            predator.will_move = True if not olf_flag else False
            predator.energy = predator.energy - predator.energy_mean * predator.energy_reduction_factor
    else:
        predator.will_move = False
        predator.energy = predator.energy - predator.energy_mean * predator.energy_reduction_factor

    return preys_pop
