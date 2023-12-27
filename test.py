from src.pyplot import PyPlot

plt = PyPlot("My Title")

plt.figure()

plt.scatter(xs=[0.1, 0.2, 0.3], ys=[0.1, 0.2, 0.3], zs=[0.1, 0.2, 0.3])

plt.plot(xs=[1, 2, 3], ys=[1, 2, 3], zs=[1, 2, 3], color="red")

plt.show()
