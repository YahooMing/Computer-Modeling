import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.stats import linregress

steps = 10000
size = 101
cluster = np.zeros((size, size))
center = size // 2
cluster[center, center] = 1

def somsiedzi(x, y):
    positions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    neighbors = []
    for dx, dy in positions:
        rx = x + dx
        ry = y + dy
        if 0 <= rx < size and 0 <= ry < size and cluster[rx, ry] == 0:
            neighbors.append((rx, ry))
    return neighbors

frontier = [(center, center)]

radiuseses = []
N_values = []

for step in range(steps):
    if not frontier:
        break
    x, y = random.choice(frontier)
    new_neighbors = somsiedzi(x, y)
    if new_neighbors:
        nx, ny = random.choice(new_neighbors)
        cluster[nx, ny] = 1
        frontier.append((nx, ny))
    else:
        frontier.remove((x, y))

    if step % 100 == 0:
        positions = np.argwhere(cluster == 1)
        distances = np.sqrt((positions[:, 0] - center) ** 2 + (positions[:, 1] - center) ** 2)
        r = np.sqrt(np.mean(distances ** 2))
        radiuseses.append(r)
        N_values.append(len(positions))

plt.figure(figsize=(6, 6))
plt.imshow(cluster, cmap='Greys', origin='lower')
plt.title("model edena")
plt.axis('off')
plt.show()

log_N = np.log(N_values)
log_r = np.log(radiuseses)
d, intercept, r_value, p_value, std_err = linregress(log_N, log_r)

plt.figure()
plt.loglog(N_values, radiuseses, 'o-')
plt.loglog(N_values, np.exp(intercept) * np.array(N_values) ** d, 'r--',
           label=f'r do N^{d:.2f}')
plt.xlabel('liczba komórek')
plt.ylabel('promien klastra')
plt.title('skalowanie')
plt.grid(True)
plt.legend()
plt.show()

print(f"(1/d): {d:.3f}")
print(f"wymiar fraktalny {1/d:.3f}")
