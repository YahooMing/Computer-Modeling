import numpy as np

def oned(n):
    x = np.cumsum(np.random.choice([-1,1], size=n))
    return np.any(x == 0)

def twod(n):
    x = np.cumsum(np.random.choice([-1,1], size=n))
    y = np.cumsum(np.random.choice([-1,1], size=n))
    return np.any((x == 0) & (y == 0))

def threed(n):
    x = np.cumsum(np.random.choice([-1,1], size=n))
    y = np.cumsum(np.random.choice([-1,1], size=n))
    z = np.cumsum(np.random.choice([-1,1], size=n))
    return np.any((x == 0) & (y == 0) & (z==0))

n_spacerow = 1000
n_krokow = 1000

one_d = (sum(oned(n_krokow) for _ in range(n_spacerow)))/ n_spacerow
two_d = (sum(twod(n_krokow) for _ in range(n_spacerow)))/ n_spacerow
three_d = (sum(threed(n_krokow) for _ in range(n_spacerow)))/ n_spacerow

print(f'Prawdopodobieństwo d=1: {one_d:.3f}')
print(f'Prawdopodobieństwo d=2: {two_d:.3f}')
print(f'Prawdopodobieństwo d=3: {three_d:.3f}')