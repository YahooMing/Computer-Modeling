import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.stats import linregress

size = 201
center = size // 2
max_particles = 10000

cluster = np.zeros((size, size), dtype=bool)
cluster[center, center] = True

def is_neighbor(x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            if cluster[x + dx, y + dy]:
                return True
    return False

def compute_radius():
    positions = np.argwhere(cluster)
    distances = np.sqrt((positions[:, 0] - center)**2 + (positions[:, 1] - center)**2)
    return np.mean(distances)

radii = []
particle_counts = []

for i in range(1, max_particles):
    angle = random.uniform(0, 2 * np.pi)
    radius = size // 2 - 1
    x = int(center + radius * np.cos(angle))
    y = int(center + radius * np.sin(angle))

    while True:
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        x += dx
        y += dy
        if x <= 1 or x >= size - 2 or y <= 1 or y >= size - 2:
            break
        if is_neighbor(x, y):
            cluster[x, y] = True
            break

    if i % 100 == 0:
        r = compute_radius()
        radii.append(r)
        particle_counts.append(i)



log_N = np.log(particle_counts)
log_r = np.log(radii)

mask = np.isfinite(log_N) & np.isfinite(log_r)
log_N = log_N[mask]
log_r = log_r[mask]

slope, intercept, _, _, _ = linregress(log_N, log_r)
dimension = 1 / slope


plt.figure(figsize=(6,6))
plt.imshow(cluster, cmap='Greys', origin='lower')
plt.title("model DLA")
plt.axis('off')
plt.show()

plt.figure()
plt.loglog(particle_counts, radii, 'o-')
plt.loglog(particle_counts, np.exp(intercept) * np.array(particle_counts) ** slope,
           'r--', label=f'r ∼ N^{slope:.2f}')
plt.xlabel('liczba cząsteczek')
plt.ylabel('promień klastra')
plt.title('skalowanie')
plt.legend()
plt.grid(True)
plt.show()

print(f"(1/d): {slope:.3f}")
print(f"wymiar fraktalny d = {dimension:.3f}")
