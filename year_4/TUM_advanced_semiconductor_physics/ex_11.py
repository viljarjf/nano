# Exercise 11 in Advanced Semiconductor Physics @ TUM

import numpy as np
from scipy import linalg
from matplotlib import pyplot as plt

Sx = 0.5 * np.array([[0, 1], [1, 0]], dtype=np.complex128)
Sy = 0.5 * np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Sz = 0.5 * np.array([[1, 0], [0, -1]], dtype=np.complex128)

I = np.eye(2)
Sx4 = linalg.kron(Sx, I)
Sy4 = linalg.kron(Sy, I)
Sz4 = linalg.kron(Sz, I)

Ix4 = linalg.kron(I, Sx)
Iy4 = linalg.kron(I, Sy)
Iz4 = linalg.kron(I, Sz)

muB = 9.2740100783e-24
g = 1.9985
h = 6.62607015e-34
A = 117.52e6 * h

H = lambda B: muB * g * B * Sz4 + A *(Sx4 @ Ix4 + Sy4 @ Iy4 + Sz4 @ Iz4)

B_range = np.linspace(0, 100e-3, 1000)
E = []
psi = []
for B in reversed(B_range):
    _E, _psi = linalg.eigh(H(B))
    E.append(_E)
    psi.append(_psi)
E.reverse()
psi.reverse()

uu = np.array([1, 0, 0, 0], dtype=np.complex128)
ud = np.array([0, 1, 0, 0], dtype=np.complex128)
du = np.array([0, 0, 1, 0], dtype=np.complex128)
dd = np.array([0, 0, 0, 1], dtype=np.complex128)

uu_str = r"\left|\uparrow\Uparrow\right>"
ud_str = r"\left|\uparrow\Downarrow\right>"
du_str = r"\left|\downarrow\Uparrow\right>"
dd_str = r"\left|\downarrow\Downarrow\right>"

print((Sz4 @ uu)[(Sz4 @ uu).nonzero()].real, (Iz4 @ uu)[(Iz4 @ uu).nonzero()].real)
print((Sz4 @ ud)[(Sz4 @ ud).nonzero()].real, (Iz4 @ ud)[(Iz4 @ ud).nonzero()].real)
print((Sz4 @ du)[(Sz4 @ du).nonzero()].real, (Iz4 @ du)[(Iz4 @ du).nonzero()].real)
print((Sz4 @ dd)[(Sz4 @ dd).nonzero()].real, (Iz4 @ dd)[(Iz4 @ dd).nonzero()].real)

a = ud
b = (du + uu) / 2**0.5
c = (du - uu) / 2**0.5
d = dd
start = np.array([a, b, c, d])
end = np.array([dd, du, uu, ud])
print(np.allclose(psi[0], start))
print(np.allclose(psi[-1], end, rtol=0.1))

plt.figure()
plt.plot(B_range, E)
plt.xlabel("B [T]")
plt.ylabel("E [J]")
plt.legend([
    f"${ud_str} \\rightarrow {dd_str}$",
    f"$\\frac{{1}}{{\sqrt{{2}}}}\\left({du_str} + {uu_str}\\right) \\rightarrow {du_str}$",
    f"$\\frac{{1}}{{\sqrt{{2}}}}\\left({du_str} + {uu_str}\\right) \\rightarrow {uu_str}$",
    f"${dd_str} \\rightarrow {ud_str}$",
])
plt.title("Legend might be wrong..")
plt.show()
