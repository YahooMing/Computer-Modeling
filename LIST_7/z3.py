import numpy as np
import matplotlib.pyplot as plt

size = 101
steps = 60
center = size // 2

neighbors = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]

def evolve(rule):
    grid = np.zeros((size, size), dtype=int)
    grid[center, center] = 1
    grid[center - 1, center] = 1
    grid[center, center + 1] = 1
    grids = [grid.copy()]

    for _ in range(steps):
        new_grid = grid.copy()
        for x in range(1, size - 1):
            for y in range(1, size - 1):
                if grid[x, y] == 1:
                    continue
                count = 0
                for dx, dy in neighbors:
                    if grid[x + dx, y + dy] == 1:
                        count += 1
                if rule(count):
                    new_grid[x, y] = 1
        grid = new_grid
        grids.append(grid.copy())
    return grids

rules = {
    "1 sąsiad": lambda c: c == 1,
    "2 sąsiadów": lambda c: c == 2,
    ">=1 sąsiad": lambda c: c >= 1,
    ">=2 sąsiadów (moje własne)": lambda c: c >= 2
}
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for ax, (title, rule) in zip(axes, rules.items()):
    final = evolve(rule)[-1]
    ax.imshow(final, cmap="Blues", origin="lower")
    ax.set_title(title)
    ax.axis("off")
plt.suptitle("wyjkresik")
plt.tight_layout()
plt.show()
