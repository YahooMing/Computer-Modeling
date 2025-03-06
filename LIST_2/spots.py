import random
import tkinter as tk

class Spots:
    def __init__(self, base , width=100, height=100):
        self.width = width
        self.height = height
        self.size_cell = 10
        self.base = base
        self.background = tk.Canvas(base, width = width*self.size_cell, height = height*self.size_cell)
        self.background.pack() # żeby użyć widżetu podczas wyświetlania
        self.table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.random_table()
        self.draw()
        self.play()

    def random_table(self):
        for row in range(self.height):
            for col in range(self.width):
                self.table[row][col] = random.choice([0,1])

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                clr = "white" if self.table[i][j]==1 else "black"
                self.background.create_rectangle(
                    j * self.size_cell, i * self.size_cell,
                    (j+1) * self.size_cell, (i+1) * self.size_cell,
                    fill = clr
                )

    def colide(self,x,y):
        shifts = [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1),(0, 1),(1, -1), (1, 0), (1, 1)] # przesunięcia względem x y danej komórki żeby sprawdzić sąsiadujące ze sobą
        living_cells = 0
        for dx, dy in shifts: #i,j to sa w tym przypadku przesunięcia
            close_cell_x , close_cell_y = (x+dx) % self.height, (y+dy)%self.width #modulo żeby sprawdzić warunek brzegowy
            living_cells += self.table[close_cell_x][close_cell_y]
        return living_cells

    def update(self):
        new_table = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                neighbours = self.colide(row, col)
                if neighbours in [ 4, 6, 7, 8, 9]:
                    new_table[row][col] = 1
                else:
                    new_table[row][col] = 0
        self.table = new_table

    def play(self):
        self.update()
        self.background.delete("all")
        self.draw()
        self.base.after(5,self.play)

if __name__ == "__main__":
    base = tk.Tk()
    game = Spots(base)
    base.mainloop()
