import random
#import matplotlib as mp
import tkinter as tk

class GameOfLife:
    def __init__(self,base, mode=1):
        self.width = 100
        self.height = 100
        self.mode = mode

        # TEMP
        self.size_cell = 10
        self.background = tk.Canvas(base, width=self.width * self.size_cell, height=self.height * self.size_cell)
        self.background.pack()
        self.base = base


        self.table = [ [0 for _ in range(self.width)] for _ in range(self.height)]
        self.random_table()

        self.draw() #temp
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
        shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
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
                mystate = self.table[row][col]
                neighbours = self.colide(row, col)
                if mystate == 1 and neighbours not in [2, 3]:  # Śmierć
                    new_table[row][col] = 0
                elif mystate == 0 and neighbours == 3:  # Urodziny
                    new_table[row][col] = 1
                else:  
                    new_table[row][col] = mystate  # Stan się nie zmienia
                
                # Śledzenie zmian
                if new_table[row][col] != self.table[row][col]:
                    changed_cells.append((row, col, new_table[row][col]))

        self.table = new_table
        return changed_cells  # Zwracamy listę zmienionych komórek
    
    def play(self):
        self.update()
        self.background.delete("all")
        self.draw()
        self.base.after(10, lambda: self.play())

if __name__ == "__main__":
    base = tk.Tk()
    game = GameOfLife(base)
    base.mainloop()