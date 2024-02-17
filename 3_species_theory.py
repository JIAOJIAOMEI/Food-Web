# @Author  : Mei Jiaojiao
# @Time    : 2023/11/14 08:52
# @Software: PyCharm
# @File    : 3_species_theory.py


# import libraries
import numpy as np
import matplotlib.pyplot as plt
from progressbar import progressbar as pr_bar
from scipy.integrate import odeint
import warnings
warnings.filterwarnings("ignore")

# parameters definition

# x: number of rabbits
# y: number of foxes
# z: number of wolves

x = 50
y = 10
z = 5
initial_conditions = [x, y, z]

# a : birth rate of rabbits
# b : death rate of rabbits due to predation
# c : death rate of foxes because of natural death
# d : birth rate of foxes due to predation
# e : death rate of foxes due to predation
# f : death rate of wolves because of natural death
# g : birth rate of wolves due to predation

a = 0.4
b = 0.05
c = 0.05
d = 0.02
e = 0.06
f = 0.1
g = 0.02

# dxdt = a*x - b*x*y
# dydt = -c*y + d*x*y - e*y*z
# dzdt = -f*z + g*y*z


def system(variables, t, a, b, c, d, e, f, g):
    x, y, z = variables
    dxdt = a * x - b * x * y
    dydt = -c * y + d * x * y - e * y * z
    dzdt = -f * z + g * y * z
    return [dxdt, dydt, dzdt]


t = np.linspace(0, 100, 800)  # Time points
ode_results = odeint(system, initial_conditions, t, args=(a, b, c, d, e, f, g))

plt.figure(figsize=(30, 6))
plt.plot(t, ode_results[:, 0], color="b", label="Species x")
plt.plot(t, ode_results[:, 1], color="g", label="Species y")
plt.plot(t, ode_results[:, 2], color="r", label="Species z")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.title("Population Dynamics of Three Species")
plt.savefig("3_species_theory.png", dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()
