from XRD import parse, convert, utilities

from matplotlib import pyplot as plt
from scipy import integrate

def main():
    Si, unknown = parse.get_data()
    plt.plot(Si[:, 0], Si[:, 1])
    plt.plot(unknown[:, 0], unknown[:, 1])
    plt.legend(["Si", "Unknkown"])
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
 