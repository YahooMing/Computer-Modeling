import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dt = 0.0015       
m = 1.0           
G = 1.0          
n_steps = 2000   
N = 3            

W, H = 800, 800  

def avg_distance(x, y):
    """Oblicza średnią odległość między trzema ciałami."""
    d01 = np.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2)
    d02 = np.sqrt((x[0] - x[2])**2 + (y[0] - y[2])**2)
    d12 = np.sqrt((x[1] - x[2])**2 + (y[1] - y[2])**2)
    return (d01 + d02 + d12) / 3.0

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
        # Inicjalizacja zmiennych pomocniczych dla metody Verlet
        self.xp1 = np.zeros(self.N)
        self.yp1 = np.zeros(self.N)
        self.xm1 = np.zeros(self.N)
        self.ym1 = np.zeros(self.N)
        
    def simulation_step(self):
        """pierwszy krok metodą Eulera, potem Verlet"""
        self.step += 1
        fx = np.zeros(self.N)
        fy = np.zeros(self.N)
        
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

        if self.step == 1:
            for b in range(self.N):
                self.vx[b] += (fx[b] / self.m) * self.dt
                self.vy[b] += (fy[b] / self.m) * self.dt
                self.xp1[b] = self.x[b] + self.vx[b] * self.dt
                self.yp1[b] = self.y[b] + self.vy[b] * self.dt
        else:
            #verlet
            for b in range(self.N):
                self.xp1[b] = 2 * self.x[b] - self.xm1[b] + (self.dt**2 * fx[b] / self.m)
                self.yp1[b] = 2 * self.y[b] - self.ym1[b] + (self.dt**2 * fy[b] / self.m)
        
        for b in range(self.N):
            self.xm1[b] = self.x[b]
            self.ym1[b] = self.y[b]
            self.x[b] = self.xp1[b]
            self.y[b] = self.yp1[b]
            self.vx[b] = (self.x[b] - self.xm1[b]) / (2 * self.dt)
            self.vy[b] = (self.y[b] - self.ym1[b]) / (2 * self.dt)
            
        return avg_distance(self.x, self.y)

x0_base = [0.5 - 0.2, 0.5 + 0.2, 0.5]
y0_base = [0.5 - 0.2, 0.5 - 0.2, 0.5 + 0.2]
vx0_base = [0.93240737 / 2.0, 0.93240737 / 2.0, -0.93240737]
vy0_base = [0.86473146 / 2.0, 0.86473146 / 2.0, -0.86473146]

perturbation = 0.001

sim1 = ThreeBodySimulation(x0_base, y0_base, vx0_base, vy0_base, dt, m, G)

x0_2 = x0_base.copy()
y0_2 = y0_base.copy()
x0_2[0] += perturbation
sim2 = ThreeBodySimulation(x0_2, y0_2, vx0_base, vy0_base, dt, m, G)

x0_3 = x0_base.copy()
y0_3 = y0_base.copy()
y0_3[1] += perturbation
sim3 = ThreeBodySimulation(x0_3, y0_3, vx0_base, vy0_base, dt, m, G)

avg_dist_sim1 = []
avg_dist_sim2 = []
avg_dist_sim3 = []
steps = []

fig, ax = plt.subplots()
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect('equal')
ax.set_title("Symulacja problemu trzech ciał")
points1, = ax.plot([], [], 'o', markersize=6, color='black', label="Sim 1")
points2, = ax.plot([], [], 'o', markersize=6, color='red',   label="Sim 2")
points3, = ax.plot([], [], 'o', markersize=6, color='green', label="Sim 3")
txt = ax.text(10, H - 40, "", fontsize=16, color='blue')
ax.legend(loc="upper right")

def update(frame):
    steps.append(frame)
    d1 = sim1.simulation_step()
    d2 = sim2.simulation_step()
    d3 = sim3.simulation_step()
    avg_dist_sim1.append(d1)
    avg_dist_sim2.append(d2)
    avg_dist_sim3.append(d3)
    
    xs1 = 98 * sim1.x + W / 2
    ys1 = 98 * sim1.y + H / 2
    xs2 = 98 * sim2.x + W / 2
    ys2 = 98 * sim2.y + H / 2
    xs3 = 98 * sim3.x + W / 2
    ys3 = 98 * sim3.y + H / 2
    
    points1.set_data(xs1, ys1)
    points2.set_data(xs2, ys2)
    points3.set_data(xs3, ys3)
    
    txt.set_text(f"Krok: {sim1.step}")
    if frame == n_steps - 1:
        ani.event_source.stop()
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(steps, avg_dist_sim1, label="Symulacja 1 (warunki bazowe)")
        ax2.plot(steps, avg_dist_sim2, label="Symulacja 2 (perturbacja ciała 0)")
        ax2.plot(steps, avg_dist_sim3, label="Symulacja 3 (perturbacja ciała 1)")
        ax2.set_xlabel("Krok symulacji")
        ax2.set_ylabel("Średnia odległość między ciałami")
        ax2.set_title("Efekt motyla: Porównanie zachowania chaotycznego")
        ax2.legend()
        ax2.grid(True)
        plt.show()
    
    return points1, points2, points3, txt

ani = FuncAnimation(fig, update, frames=n_steps, interval=1, blit=True)

plt.show()