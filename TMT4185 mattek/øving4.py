import matplotlib.pyplot as plt

load = [0, 7330, 15100, 23100, 30400, 34400, 38400, 41300, 44800, 46200, 47300, 47500, 46100, 44800, 42600, 36400]
length = [50.8, 50.851, 50.902, 50.952, 51.003, 51.054,51.308, 51.816, 52.832, 53.848, 54.864, 55.880, 56.896, 57.658, 58.420, 59.182]

plt.plot([(x-50.8)/50.8 for x in length], [x / (4/3.1415 *(0.0128)**2) for x in load])
plt.show()