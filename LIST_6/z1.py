import random
import numpy as np
import matplotlib.pyplot as plt

n_liczb = 1000000
n_kubelkow = 10000

# Tu wyczytałem że podstawowo python używa Mersenne Twister
# https://docs.python.org/3/library/random.html#random.Random
# więc nie ma sensu implementować osobno tego algorytmu

# tu generuje te liczby z użyciem Mernenne Twister
samples1 = [random.random() for _ in range(n_liczb)]

# tu próbuje generować z użyciem modulo: Linear Congruential Generator
# Xn+1 = (a * Xn +C)mod m
# a - mnożnik
# c = increment
# m = moduł
# https://en.wikipedia.org/wiki/Linear_congruential_generator
# wybrałem wartości z drugiego wiersza z "Parameters in common use"

a = 1103515245
c = 12345
m = 2**31
x = 1

samples2 = []

for _ in range(n_liczb):
    x = (a *x +c)%m
    samples2.append(x/m) # dziele przez m żeby liczby wychodziły od 0 do 1

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex = True)

# ax1.hist(samples1, bins=n_kubelkow, color='red', alpha = 0.7)
# ax1.set_title('mersenne twister')

# ax2.hist(samples2, bins=n_kubelkow, color='green', alpha = 0.7)
# ax2.set_title('z modulo')

# plt.xlabel('przedziały')
# plt.tight_layout()
# plt.show()



plt.figure(figsize=(12, 6))
plt.hist(samples1, bins=n_kubelkow, alpha=0.5, label='Mersenne Twister', color='red', density=True)
plt.hist(samples2, bins=n_kubelkow, alpha=0.5, label='LCG (modulo)', color='green', density=True)
plt.title('Porównanie rozkładów pseudolosowych')
plt.xlabel('Przedziały wartości')
plt.ylabel('Gęstość')
plt.legend()
plt.tight_layout()
plt.show()
#dlaczego sie różnią?
#mersenne twister ma znacznie większy moduł 2^19937 - 1 a LCG ma 2^32