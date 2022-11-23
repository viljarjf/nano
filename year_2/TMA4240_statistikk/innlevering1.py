import random
from statistics_TMA4240 import *
def opg1a():
    l = [1] + [0]*99
    random.shuffle(l)
    print(l)
    found = 0
    amount = 1000000
    for x in range(amount):
        l[l.index(1)] = 0
        l[random.randint(0, len(l)-1)] = 1
        s = l[96:]
        if 1 in s:
            if s.count(1) > 1:
                print("wat")
            found += 1
    print(found, found / amount)
def opg1b():
    print(1/100 + 1/9900 + 1/(99*98*100) + 1/(100*99*98*97)) 
    
opg1a()
