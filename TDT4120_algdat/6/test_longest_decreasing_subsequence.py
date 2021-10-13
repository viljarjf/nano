# !/usr/bin/python3
# coding=utf-8
class Element:

    def __init__(self, val: int, up: bool, left: bool):
        self.val = val
        self.up = up
        self.left = left
    
    def __iadd__(self, val):
        self.val += val
        return self
    
    def __bool__(self):
        return self.up and self.left
    
    def __str__(self):
        return str(self.val)
        if self.up and self.left:
            return "\\"
        elif self.up:
            return "^"
        elif self.left:
            return "<"

def longest_decreasing_subsequence(s):
    comp = sorted(set(s), reverse = True)
    ls = len(s)
    lc = len(comp)
    res = [[Element(0, False, False) for i in range(lc+1)] for j in range(ls+1)]
    for i in range(ls):
        for j in range(lc):
            res[i][j] +=  int(s[i] == comp[j])

            if s[i] == comp[j]:
                res[i][j].up = True
                res[i][j].left = True

            if res[i][j-1].val >= res[i-1][j].val:
                res[i][j] += res[i][j-1].val
                res[i][j].up = True
            else:
                res[i][j].left = True
                res[i][j] += res[i-1][j].val
            
    print(" ",*comp)
    for i, el in enumerate(res[:-1]):
        print(s[i], *el[:-1])
    return_list= []
    i = ls-1
    j = lc-1
    while i>= 0 and j >= 0:
        o = res[i][j]
        if o:
            return_list.append(s[i])
            i -= 1
            j -= 1
        elif o.up:
            i -= 1
        else:
            j -= 1
    seen = set()
    return_list.reverse()
    return [x for x in return_list if not (x in seen or seen.add(x))]



# Teste på formatet (følge, riktig lengde på svar)
tests = [
    #([1], 1),
    #([1, 2], 1),
    #([1, 2, 3], 1),
    #([2, 1], 2),
    #([3, 2, 1], 3),
    #([1, 3, 2], 2),
    #([3, 1, 2], 2),
    #([1, 1], 1),
    #([1, 2, 1], 2),
    ([8, 7, 3, 6, 2, 6], 4),
    ([10, 4, 2, 1, 7, 5, 3, 2, 1], 6),
    ([3, 7, 2, 10, 3, 3, 3, 9], 2),
]


def verify(sequence, subsequence, optimal_length):
    # Test if the subsequence is actually a subsequence
    index = 0
    for element in sequence:
        if element == subsequence[index]:
            index += 1
            if index == len(subsequence):
                break

    if index < len(subsequence):
        return False, "Svaret er ikke en delfølge av følgen."

    # Test if the subsequence is decreasing
    for index in range(1, len(subsequence)):
        if subsequence[index] >= subsequence[index - 1]:
            return False, "Den gitte delfølgen er ikke synkende."

    # Test if the solution is optimal
    if len(subsequence) != optimal_length:
        return (
            False,
            "Delfølgen har ikke riktig lengde. Riktig lengde er"
            + "{:}, mens delfølgen har lengde ".format(optimal_length)
            + "{:}".format(len(subsequence)),
        )

    return True, ""


failed = False

for test, optimal_length in tests:
    answer = longest_decreasing_subsequence(test[:])
    correct, error_message = verify(test, answer, optimal_length)

    if not correct:
        failed = True
        print(
            'Feilet med feilmeldingen "{:}" for testen '.format(error_message)
            + "{:}. Ditt svar var {:}.".format(test, answer)
        )

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
