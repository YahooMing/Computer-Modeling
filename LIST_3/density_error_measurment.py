import random
import matplotlib.pyplot as plt
import numpy as np

class GameOfLife:
    def __init__(self, L, p0=0.5, steps=1000):
        self.width = self.height = L
        self.p0 = p0
        self.steps = steps
        self.table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.random_table()

    def random_table(self):
        for row in range(self.height):
            for col in range(self.width):
                self.table[row][col] = 1 if random.random() < self.p0 else 0

    def colide(self, x, y):
        shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        living_cells = 0
        for dx, dy in shifts:
            close_cell_x, close_cell_y = (x + dx) % self.height, (y + dy) % self.width
            living_cells += self.table[close_cell_x][close_cell_y]
        return living_cells

    def update(self):
        new_table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                mystate = self.table[row][col]
                neighbours = self.colide(row, col)
                if mystate == 1 and neighbours not in [2, 3]:
                    new_table[row][col] = 0
                elif mystate == 0 and neighbours == 3:
                    new_table[row][col] = 1
                else:
                    new_table[row][col] = mystate
        self.table = new_table

    def play(self):
        for _ in range(self.steps):
            self.update()
        return sum([sum(row) for row in self.table]) / (self.width * self.height)

L_values = [10, 100, 200]
N = 100
p0 = 0.5
steps = 1000

errors = []
for L in L_values:
    densities = [GameOfLife(L, p0, steps).play() for _ in range(N)]
    std_error = np.std(densities) / np.sqrt(N)
    errors.append(std_error)

plt.figure()
plt.plot(L_values, errors, marker='o')
plt.xscale("log")
plt.xlabel("Rozmiar układu (L)")
plt.ylabel("Błąd standardowy średniej")
plt.title("Błąd standardowy średniej gęstości w zależności od L")
plt.grid(True)
plt.show()
