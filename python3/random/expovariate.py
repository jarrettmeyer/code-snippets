import random
import matplotlib.pyplot as plt

values = []

MEAN = 3.0
N_VALUES = 1000

for i in range(N_VALUES):
    value = random.expovariate(1.0 / MEAN)
    values.append(value)

plt.plot(values)
plt.show()

n_bins = max(50, int(N_VALUES/10))
plt.hist(values, bins=n_bins)
plt.show()
