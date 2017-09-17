# -*- coding:utf-8 -*-

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

a = np.arange(15).reshape(3, 5)

b = np.array([2,3,4])
b1 = np.array([1.2, 3.5, 5.1])

c = np.zeros((3,4))

# dtype can also be specified
# (2,3,4) 表示 2 個 3X4 的Table
d = np.ones((2,3,4), dtype=np.int32) 

ary1 = np.arange(10, 30, 5)
flot1 = np.arange(0, 2, 0.3)  # it accepts float arguments

ary2 = np.linspace(0, 2, 9) # 9 numbers from 0 to 2

num1 = np.linspace(0, 2*pi, 10)

num2 = np.sin(num1)

# Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
mu, sigma = 2, 0.5
v = np.random.normal(mu,sigma,10000)
# Plot a normalized histogram with 50 bins
plt.hist(v, bins=50, normed=1)       # matplotlib version (plot)
plt.show()

print(a)
print(b.dtype)
print(b1.dtype)
print(c)
print(d)
print(ary1)
print(flot1)
print(ary2)
print(num1)
print(num2)