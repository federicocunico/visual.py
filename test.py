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

    plt.pause(5)


def example3():
    plt = PyPlot("My Title")

    plt.figure()

    max_t = 100
    t = np.linspace(0, 10, max_t)
    x = np.sin(t)
    y = np.cos(t)
    y = y + 1  # move up a bit
    z = t

    _t = 0
    while True:
        print("\rt:", _t, end="")
        plt.clear()

        if _t >= max_t:
            _t = 0
        plt.plot(xs=x, ys=y, zs=z, color="blue")

        _x = x[_t]
        _y = y[_t]
        _z = z[_t]

        plt.scatter(xs=[_x], ys=[_y], zs=[_z], size=0.5, color="red")

        plt.show()
        _t += 1

        plt.pause(1/60)  # 60 fps

    plt.pause(1)
    plt.clear()
    plt.close()


# example1()
# example2()
example3()
