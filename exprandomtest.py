# @Author  : Mei Jiaojiao
# @Time    : 2023/12/1 08:44
# @Software: PyCharm
# @File    : exprandomtest.py
import numpy as np
from matplotlib import pyplot as plt

birth_lambda=0.3
death_lambda=0.15

list = [np.random.exponential(1/birth_lambda) for i in range(1000)]
list_2 = [np.random.exponential(1/death_lambda) for i in range(1000)]

print(list)

plt.hist(list, bins=1000,color='red')
plt.hist(list_2, bins=1000,color='blue')
plt.xlabel('Time stamp')
plt.ylabel('Frequency')
plt.legend(['birth','death'])
plt.savefig('exprandomtest1.png')
plt.show()