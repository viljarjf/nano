import random

l = []
for n in range(1000000):
    a = []
    for i in range(1, 8):
        b = random.randint(1, 6)
        if b not in a:
            a.append(b)
        else:
            l.append(i)
            break

res = [l.count(n) for n in range(1, 8)]
print(res)
prob = [n/len(l) for n in res]
print(prob)