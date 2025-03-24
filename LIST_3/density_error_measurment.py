import numpy as np
import concurrent.futures

class GameOfLife:
    def __init__(self, L, p0=0.5, steps=1000):
        self.L = L
        self.p0 = p0
        self.steps = steps
        # dla pythoniarzy, zróbcie macierz numpy'ową bo jest OP
        self.table = np.random.choice([0, 1], size=(L, L), p=[1 - p0, p0])
    
    def update(self):
        # za pomocą rolla przesuwa sie macierz pionowo, no nie? i za pomocą tego można obliczyć sąsiadów
        neighbors = sum(np.roll(np.roll(self.table, dx, axis=0), dy, axis=1)
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                        if not (dx == 0 and dy == 0))
        new_table = ((self.table == 1) & ((neighbors == 2) | (neighbors == 3))) | \
                    ((self.table == 0) & (neighbors == 3))
        self.table = new_table.astype(int)
    
    def play(self):
        for _ in range(self.steps):
            self.update()
        return self.table.sum() / (self.L * self.L) # dens

def simulate(L, p0, steps):
    game = GameOfLife(L, p0, steps)
    return game.play()

if __name__ == '__main__':
    L_values = [10, 100, 200, 500, 1000]
    N = 100
    p0 = 0.5
    steps = 1000

    errors = []
    for L in L_values:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            densities = list(executor.map(simulate, [L] * N, [p0] * N, [steps] * N))
        std_error = np.std(densities) / np.sqrt(N)
        errors.append(std_error)
        print(f"L = {L}: Średnia gęstość = {np.mean(densities):.4f}, Błąd standardowy = {std_error:.4f}")

