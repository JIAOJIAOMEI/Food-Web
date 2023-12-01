# @Author  : Mei Jiaojiao
# @Time    : 2023/12/1 08:44
# @Software: PyCharm
# @File    : exprandomtest.py
import numpy as np
from matplotlib import pyplot as plt

birth_lambda=0.08

list = [np.random.exponential(1/birth_lambda) for i in range(1000)]

print(list)

print(np.mean(list))