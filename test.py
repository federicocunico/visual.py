import numpy as np
from src.pyplot import PyPlot

def example1():
    plt = PyPlot("My Title")

    plt.figure()

    plt.scatter(xs=[0.1, 0.2, 0.3], ys=[0.1, 0.2, 0.3], zs=[0.1, 0.2, 0.3])

    plt.plot(xs=[1, 2, 3], ys=[1, 2, 3], zs=[1, 2, 3], color="red")

    plt.show()

    plt.pause(5)

    plt.clear()


def example2():
    plt = PyPlot("My Title")

    plt.figure()

    t = np.linspace(0, 10, 100)
    x = np.sin(t)
    y = np.cos(t)
    z = t

    y = y + 1  # move up a bit

    plt.plot(xs=x, ys=y, zs=z, color="red")

    plt.show()
