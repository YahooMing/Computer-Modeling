import numpy as np
# stąd biore wzór: https://youtu.be/7DRheelN7Hg?si=zT2AfL48uPKOIUaA&t=1184

def dyf(n, n_sym, kierunki):
    srd_kwrd= []
    for _ in range(n_sym):
        pos = np.array([0,0])
        for _ in range(n):
            pos += kierunki[np.random.randint(len(kierunki))]
        r2 = np.sum(pos**2)
        srd_kwrd.append(r2)
    ret = np.mean(srd_kwrd)
    d = ret/(4*n)
    return d

n = 1000
n_sym = 1000

kierunki1 = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]
d1 = dyf(n, n_sym, kierunki1)

kierunki2 = kierunki1 +[np.array([1, 1]), np.array([-1, -1]), np.array([-1, 1]), np.array([1, -1])]
d2 = dyf(n, n_sym, kierunki2)

print(f'Dyfuzja 4 kierunki: {d1}')
print(f'Dyfuzja 8 kierunków: {d2}')