import numpy as np
import matplotlib.pyplot as plt

n_krokow = 1000
n_spacerow = 10000

sample = np.random.choice([-1,1], size=(n_spacerow, n_krokow))
endpoints = np.sum(sample, axis=1)

plt.hist(endpoints, bins=100, color = 'blue', edgecolor='black')
plt.title("histogram")
plt.xlabel("pozycja końcowa")
plt.ylabel("liczba spacerów")
plt.grid(True)
plt.show()

odl1 = np.sum(np.abs(endpoints) == 1)
odl2 = np.sum(np.abs(endpoints) == 30)

print(odl1)
print(odl2)