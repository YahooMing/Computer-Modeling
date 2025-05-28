import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


n_krokow = 1000
n_spacerow = 10

#dwuwymiarowy
plt.figure(figsize=(8,8))
for _ in range(n_spacerow):
    x = np.cumsum(np.random.choice([-1,1], size=n_krokow)) #suma kumulatywna
    y = np.cumsum(np.random.choice([-1,1], size=n_krokow))
    plt.plot(x,y,alpha=0.5)
    plt.plot(x[0], y[0], 'go')  # początek
    plt.plot(x[-1], y[-1], 'rx')  # koniec

plt.title("2D")
plt.axis('equal')
plt.grid(True)
plt.show()

# adekwatnie dla trójwymiaru
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
for _ in range(n_spacerow):
    dx = np.random.choice([-1, 1], size=n_krokow)
    dy = np.random.choice([-1, 1], size=n_krokow)
    dz= np.random.choice([-1, 1], size=n_krokow)
    x = np.cumsum(dx)
    y = np.cumsum(dy)
    z = np.cumsum(dz)
    ax.plot(x,y,z, alpha=0.6)
    ax.scatter(x[0], y[0], z[0], c='green', marker='o')  # początek
    ax.scatter(x[-1], y[-1], z[-1], c='red', marker='x')  # koniec
ax.set_title('3D')
plt.show()
