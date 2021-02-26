import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

e_0 = 8.85e-12
R_1 = 180000
R_osc = 10**6

def C_tot(f, V_i, V_o):
        return 1/(2*3.14159*f*R_1)* (abs(V_i/V_o)**2 - (1 + R_1/R_osc)**2)**0.5

def opg1():
    f = 10800

    d = np.array([
        0.01, 0.009, 0.008, 0.007, 0.006, 0.005, 0.004, 0.003, 0.002, 0.001
    ])

    V_o = np.array([
        2.57, 2.56, 2.54, 2.52, 2.475, 2.42, 2.34, 2.25, 2.08, 1.72
    ])

    V_i = np.array([
        5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1
    ])


    plt.plot(1/d, C_tot(f, V_i, V_o))
    plt.show()

    model = LinearRegression().fit(np.array([[i] for i in 1/d]), C_tot(f, V_i, V_o))

    print('konstantledd:', model.intercept_)
    print('stigning:', model.coef_)
    print("Areal:", model.coef_ / e_0)

def opg2():

    f = np.array([
        10, 15, 20, 25, 30, 35, 40
    ])
    f *= 1000

    V_o = np.array([
        2.18, 1.59, 1.25, 1.03, 0.88, 0.77, 0.69
    ])

    V_i = np.array([
        5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1
    ])

    plt.plot(f, C_tot(f, V_i, V_o))
    plt.show()

def opg3():
    f = 6000
    V_p = 2.48
    V_i = 5.1
    V_luft_p = 3.1
    V_m = 2.88
    V_luft_m = 3.19

    C_p = C_tot(f, V_i, V_p) - 1.215*(10**(-10))
    C_lp = C_tot(f, V_i, V_luft_p) - 1.215*10**(-10)
    e_p = C_p / C_lp
    print("e_r (papir): ", e_p)

    C_m = C_tot(f, V_i, V_m) - 1.215*10**(-10)
    C_lm = C_tot(f, V_i, V_luft_m) - 1.215*10**(-10)
    e_m = C_m / C_lm
    print("e_r (musematte): ", e_m)

opg1()
opg2()
opg3()