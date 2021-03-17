from sympy import diff, symbols, sqrt
import numpy as np


#***************YOUR INPUT HERE*************#
eps = 1
sig = 1
x, y, z= symbols("x y z")
r = sqrt(x**2 + y**2 + z**2)
V = 4*eps*((sig/r)**12 - (sig/r)**6)
vdiff = [diff(-V, var) for var in [x,y,z]]

#**************END YOUR INPUT HERE***********#

#Here we input the coordinates of the atoms. You can have as many atoms as you want, 
#and change the coordinates to whatever you like

atoms = np.array([[0.,0.,0.], [0.,0.,1.], [0.,1.,0.], [1.,0.,0.], [1.,1.,0.], [1.,0.,1.], [0.,1.,1.], [1.,1.,1.], [0.5, 0.5, 0.5]])

#We write the output to a textfile


with open("output.txt", "w") as file:

    file.write('    Atom 1    ' + '    Atom2   ' + '    Force(x-dir)   Force(y-dir)   Force(z-dir) ' + '  Total Force(abs value) ' + '\n')


    for i in range(len(atoms)):
        for j in range(i):
            res = atoms[i] - atoms[j]
            Fxyz = [tv.subs([(x,res[0]), (y,res[1]),  (z,res[2])]) for tv in vdiff]
            print("Between", atoms[i], "and", atoms[j], "we have the forces", Fxyz)
            F = sqrt(Fxyz[0]**2 + Fxyz[1]**2 + Fxyz[2]**2)
            print("and the total force is", F)
            file.write(str(atoms[i]) + " " + str(atoms[j]))
            file.write( "%14.2f %14.2f %14.2f %14.2f" % (Fxyz[0], Fxyz[1], Fxyz[2], F) + '\n')

