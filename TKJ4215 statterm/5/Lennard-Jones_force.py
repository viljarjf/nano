from sympy import diff, symbols, solve, plot

eps, sig, r = symbols('eps sig r')


eps = 1
sig = 1 

V = 4*eps*((sig/r)**12 - (sig/r)**6)

Fr = diff(-V, r)

print("Fr is: ", Fr.subs(r, 4))

print("Fr = 0:", solve(Fr, r)[1])
print("V = 0:", solve(V, r)[1])

plot(Fr, (r, 0, 10), xlabel='Radial distance', ylabel='Force', axis_center=(0,0), ylim=(-eps,4*eps))