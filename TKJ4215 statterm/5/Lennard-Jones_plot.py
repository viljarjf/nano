from sympy import diff, latex, symbols, plot

r = symbols('r')

eps = 1
sig = 1

V = 4*eps*((sig/r)**12 - (sig/r)**6)

plot(V, (r, 0, 10), xlabel='Radial distance', ylabel='Potential', axis_center=(0,0), ylim=(-eps,4*eps))

# kraftig frastøting for lav r, noe tiltrekking for medium r, ingen interagering for stor r