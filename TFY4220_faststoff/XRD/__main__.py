from XRD import parse, convert, utilities, simulate

from matplotlib import pyplot as plt
from scipy import integrate
import numpy as np

def main():
    KCl_angles, KCl_data = simulate.get_lattice_data("KCl")
    NaCl_angles, NaCl_data = simulate.get_lattice_data("NaCl")
    Si, unknown = parse.get_data()

    plt.figure()
    plt.plot(Si[:, 0], Si[:, 1])
    plt.plot(unknown[:, 0], unknown[:, 1])
    plt.plot("Si and unknown sample")
    plt.legend(["Si", "Unknkown"])
    plt.xlabel("$2\\theta$")
    plt.show(block = False)

    # normalisation factor for KCl is different
    KCl_factor = np.max(unknown[:, 1][unknown[:, 0] < 14]) / np.max(unknown[:, 1])
    plt.figure()
    plt.plot(KCl_angles, KCl_data / np.max(KCl_data)*KCl_factor)
    plt.plot(NaCl_angles, NaCl_data / np.max(NaCl_data))
    plt.plot(unknown[:, 0], unknown[:, 1] / np.max(unknown[:, 1]))
    plt.legend(["KCl", "NaCl", "Unknown"])
    plt.title("Simulated KCl and NaCl")
    plt.xlabel("$2\\theta$")
    plt.show(block = False)

    print("Enter peak values for group 1")
    twothetas1 = utilities.get_input_floats(3)

    print("Enter peak values for group 2")
    twothetas2 = utilities.get_input_floats(3)

    print("Corresponding d-spacing: ")
    for t1, t2 in zip(twothetas1, twothetas2):
        print(f"1: {convert.two_theta_to_d(t1):.2f}, 2: {convert.two_theta_to_d(t2):.2f}")

    for _ in range(6):
        print("Enter left and right boundary to integrate")
        l, r = utilities.get_input_floats(2)
        mask = (unknown[:, 0] >= l) & (unknown[:, 0] <= r)
        i = integrate.simpson(unknown[mask, 1], unknown[mask, 0])
        print(f"Integral evaluates to {i :.3f}")


if __name__ == "__main__":
    main()
 