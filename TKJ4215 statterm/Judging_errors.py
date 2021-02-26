from math import factorial, log
import matplotlib.pyplot as plt

def stirling(n):
    return n*log(n) - n

def exact_sol(n):
    return log(factorial(n))

n = [8**x +10 for x in range(8)] #Fill in the values of n that you wish to test

file = open("Stirlings.txt", "w") # Creates the file Stirlings.txt to be written
file.write( "           n      " + "Exact solution      " + "       Stirling     " + "Absolute error     " + "Relative error" +'\n') #Sets up the file header and adjusts column width

for i in n:
    ex = exact_sol(i)
    st = stirling(i)
    file.write( "%12d      %14.4f       %14.4f     %14.4f     %14.4f \n" % (i, ex, st, ex - st, (1 - st/ex))) #Calculates n factorial, the approximation and corresponding errors.
