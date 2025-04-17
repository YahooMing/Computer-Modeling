import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry symulacji
dt = 0.0015       # krok czasowy
m = 1.0           # masa ciała
G = 1.0           # stała grawitacyjna
n_steps = 3000    # liczba kroków symulacji – można zwiększyć, aby lepiej zobaczyć trajektorię

W, H = 800, 800   # rozmiar "canvasu" dla rysowania
scale = 250       # czynnik skalujący pozycje (dopasowany do rozmiarów trajektorii)

class ThreeBodySimulation:
    def __init__(self, x0, y0, vx0, vy0, dt, m, G):
        self.N = len(x0)
        self.dt = dt
        self.m = m
        self.G = G
        self.step = 0
        self.x = np.array(x0, dtype=float)
        self.y = np.array(y0, dtype=float)
        self.vx = np.array(vx0, dtype=float)
        self.vy = np.array(vy0, dtype=float)
        # Zmienne pomocnicze dla metody Verlet
        self.xp1 = np.zeros(self.N)
        self.yp1 = np.zeros(self.N)
        self.xm1 = np.zeros(self.N)
        self.ym1 = np.zeros(self.N)
        
    def simulation_step(self):
        """Wykonuje jeden krok symulacji (pierwszy krok - metoda Eulera, potem Verlet)."""
        self.step += 1
        fx = np.zeros(self.N)
        fy = np.zeros(self.N)
        
        # Obliczanie sił między ciałami (prawo grawitacji Newtona)
        for i in range(self.N):
            for j in range(i + 1, self.N):
                dx = self.x[i] - self.x[j]
                dy = self.y[i] - self.y[j]
                d = np.sqrt(dx**2 + dy**2)
                if d != 0:
                    rx = dx / d
                    ry = dy / d
                    F = self.G * self.m * self.m / (d**2)
                    Fx = rx * F
                    Fy = ry * F
                    fx[i] -= Fx
                    fy[i] -= Fy
                    fx[j] += Fx
                    fy[j] += Fy

        # Pierwszy krok – metoda Eulera
        if self.step == 1:
            for b in range(self.N):
                self.vx[b] += (fx[b] / self.m) * self.dt
                self.vy[b] += (fy[b] / self.m) * self.dt
                self.xp1[b] = self.x[b] + self.vx[b] * self.dt
                self.yp1[b] = self.y[b] + self.vy[b] * self.dt
        else:
            # Kolejne kroki – metoda Verlet
            for b in range(self.N):
                self.xp1[b] = 2 * self.x[b] - self.xm1[b] + (self.dt**2 * fx[b] / self.m)
                self.yp1[b] = 2 * self.y[b] - self.ym1[b] + (self.dt**2 * fy[b] / self.m)
                
        # Aktualizacja pozycji i prędkości
        for b in range(self.N):
            self.xm1[b] = self.x[b]
            self.ym1[b] = self.y[b]
            self.x[b] = self.xp1[b]
            self.y[b] = self.yp1[b]
            self.vx[b] = (self.x[b] - self.xm1[b]) / (2 * self.dt)
            self.vy[b] = (self.y[b] - self.ym1[b]) / (2 * self.dt)
            
        return self.x.copy(), self.y.copy()  # zwracamy aktualne pozycje ciał

# Ustawienia początkowe zgodne z rozwiązaniem "ósemki" z [1]
# (Warunki dla równych mas, tak aby środek masy był w punkcie (0,0))
x0_fe = [0.97000436, -0.97000436, 0.0]
y0_fe = [-0.24308753, 0.24308753, 0.0]
vx0_fe = [0.466203685, 0.466203685, -0.93240737]
vy0_fe = [0.432365730, 0.432365730, -0.86473146]

sim = ThreeBodySimulation(x0_fe, y0_fe, vx0_fe, vy0_fe, dt, m, G)

# Przygotowanie list do zapisu trajektorii (dla rysowania linii przelotu)
traj_x = [ [] for _ in range(3) ]
traj_y = [ [] for _ in range(3) ]

# Przygotowanie figury i osi do animacji
fig, ax = plt.subplots()
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect('equal')
ax.set_title("Trajektoria '8' w problemie trzech ciał")

# Obiekt rysujący ciała – dla lepszej widoczności każdy punkt będzie miał swój kolor
points, = ax.plot([], [], 'o', markersize=8, color='black', label="Ciała")
# Obiekty rysujące trajektorie (każde ciało innym kolorem)
lines = []
colors = ['red', 'green', 'blue']
for c in colors:
    ln, = ax.plot([], [], '-', color=c, linewidth=1)
    lines.append(ln)

txt = ax.text(10, H - 30, "", fontsize=14, color='magenta')
ax.legend(loc="upper right")

def update(frame):
    # Wykonujemy kolejny krok symulacji
    x, y = sim.simulation_step()
    
    # Zapisujemy pozycje dla każdej trajektorii
    for i in range(3):
        traj_x[i].append(x[i])
        traj_y[i].append(y[i])
    
    # Skalujemy i przesuwamy pozycje do układu współrzędnych "canvasu"
    xs = [scale * xi + W/2 for xi in x]
    ys = [scale * yi + H/2 for yi in y]
    points.set_data(xs, ys)
    
    # Aktualizujemy linie trajektorii dla każdego ciała
    for i in range(3):
        tx = [scale * xi + W/2 for xi in traj_x[i]]
        ty = [scale * yi + H/2 for yi in traj_y[i]]
        lines[i].set_data(tx, ty)
    
    txt.set_text(f"Krok: {sim.step}")
    
    if frame == n_steps - 1:
        ani.event_source.stop()
    
    return [points, txt] + lines

ani = FuncAnimation(fig, update, frames=n_steps, interval=1, blit=True)

plt.show()
