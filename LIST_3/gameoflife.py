import random
import matplotlib.pyplot as plt
import numpy as np

class GameOfLife:
    def __init__(self, mode=1, p0=0.5, steps=1000):
        self.width = 100
        self.height = 100
        self.mode = mode
        self.p0 = p0
        self.steps = steps

        self.table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.random_table()

        if self.mode == 1:
            self.fig, self.ax = plt.subplots()
            self.im = self.ax.imshow(self.table, cmap="binary", interpolation="nearest")
            self.fig.canvas.mpl_connect('close_event', self.on_close)

        self.running = True

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
                if mystate == 1 and neighbours not in [2, 3]:  # Śmierć
                    new_table[row][col] = 0
                elif mystate == 0 and neighbours == 3:  # Urodziny
                    new_table[row][col] = 1
                else:
                    new_table[row][col] = mystate  # Stan się nie zmienia
        self.table = new_table

    def play(self):
        if self.mode == 1:
            plt.show(block=False)
            while self.running:
                self.update()
                self.im.set_data(self.table)
                plt.draw()
                plt.pause(0.01)
        elif self.mode == 2:
            density = []
            for _ in range(self.steps):
                density.append(sum(sum(row) for row in self.table) / (self.width * self.height))
                self.update()
            plt.figure()
            plt.plot(density)
            plt.xlabel("Kroki")
            plt.ylabel("Gęstość żywych komórek")
            plt.title(f"p0={self.p0}")
            plt.show()
            return density

    def on_close(self, event):
        self.running = False

if __name__ == "__main__":
    game = GameOfLife(mode=1, steps=1000)
    game.play()
