import random
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import sys

class Spots:
    def __init__(self, base, mode=1, width=100, height=100):
        self.width = width
        self.height = height
        self.size_cell = 10
        self.base = base
        self.mode = mode

        self.density_data = []  # Dane do wykresu

        if self.mode == 1:
            self.background = tk.Canvas(base, width=width * self.size_cell, height=height * self.size_cell)
            self.background.pack()

        self.table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.random_table()
        self.draw() if self.mode == 1 else None
        self.play()

    def random_table(self):
        for row in range(self.height):
            for col in range(self.width):
                self.table[row][col] = random.choice([0, 1])

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                clr = "white" if self.table[i][j] == 1 else "black"
                self.background.create_rectangle(
                    j * self.size_cell, i * self.size_cell,
                    (j + 1) * self.size_cell, (i + 1) * self.size_cell,
                    fill=clr
                )

    def colide(self, x, y):
        shifts = [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        living_cells = 0
        for dx, dy in shifts:
            close_cell_x, close_cell_y = (x + dx) % self.height, (y + dy) % self.width
            living_cells += self.table[close_cell_x][close_cell_y]
        return living_cells

    def update(self):
        new_table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        changed_cells = []  # Lista zmienionych komórek

        for row in range(self.height):
            for col in range(self.width):
                neighbours = self.colide(row, col)
                if neighbours in [4, 6, 7, 8, 9]:
                    new_table[row][col] = 1
                else:
                    new_table[row][col] = 0
                
                # Śledzenie zmian
                if new_table[row][col] != self.table[row][col]:
                    changed_cells.append((row, col, new_table[row][col]))

        self.table = new_table
        return changed_cells  # Zwracamy listę zmienionych komórek

    def calculate_density(self):
        return sum(sum(row) for row in self.table) / (self.width * self.height)

    def play(self, iteration=0):
        self.update()
        density = self.calculate_density()
        self.density_data.append(density)

        if self.mode == 1:
            self.background.delete("all")
            self.draw()
            self.base.after(1, lambda: self.play(iteration + 1))
        else:
            if iteration % 200 == 0:
                plt.imshow(self.table, cmap='gray')
                plt.title(f"Iteracja {iteration}")
                plt.show(block=False)
                plt.pause(0.1)

            if iteration < 1000:  #limit iteracji dla rozkładu gęstości
                self.base.after(1, lambda: self.play(iteration + 1))
            else:
                plt.figure()
                plt.plot(self.density_data, label="Gęstość od czasu")
                plt.xlabel("Iteracje")
                plt.ylabel("Gęstość")
                plt.legend()
                plt.show()

if __name__ == "__main__":
    mode = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    base = tk.Tk() if mode == 1 else tk.Toplevel()
    game = Spots(base, mode)
    base.mainloop()