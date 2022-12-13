import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d


def f(x, y):
    return 9 - 2 * x + 4 * y - x ** 2 - 4 * y ** 2


x = np.linspace(-1, 1, 50)
y = np.linspace(-1, 1, 50)

X, Y = np.meshgrid(x, y)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, f(X, Y))
plt.show()
