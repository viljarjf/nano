#!/usr/bin/python3
# coding=utf-8

def sort(stack1, stack2, stack3):
    # I tried implementing quicksort.
    # dont ask me how it works anymore, I wrote
    # this like two weeks ago and I have no idea anymore
    a = stack1.pop()
    b = stack1.pop()

    while not stack1.empty():
        if a > b:
            stack2.push(b)
            b = stack1.pop()
        else:
            stack2.push(a)
            a = stack1.pop()
    if b > a:
        a,b = b,a
    stack1.push(a)

    while not stack2.empty() or not stack3.empty():
        if not stack3.empty():
            stack2, stack3 = stack3, stack2
        a = stack2.pop()
        while not stack2.empty():
            if a > b:
                stack3.push(b)
                b = stack2.pop()
            else:
                stack3.push(a)
                a = stack2.pop()
        if b > a:
            a,b = b,a
        stack1.push(a)
    stack1.push(b)


def _sort(stack1, stack2, stack3):
    a = stack1.pop()
    b = stack1.pop()
    while True:
        while True:
            if a > b:
                a,b = b,a
            if stack3.empty():
                stack3.push(a)
                break
            if a < stack3.peek():
                stack1.push(b)
                b = stack3.pop()
            else:
                stack3.push(a)
                break
        if stack1.empty():
            break
        a = stack1.pop()
    stack1.push(b)
    while not stack3.empty():
        stack1.push(stack3.pop())
    
        
def _sort(stack1, stack2, stack3):
    
    def sort_single(s, g, l, size, reverse):
        if size is not None:
            string = f"Sorting {s.stack[-size:]}"
            if size <= 1:
                return s
            size -= 1
        p = s.pop()

        cur_size = 0
        g_size = 0
        l_size = 0

        def cond():
            if size is None:
                return not s.empty()
            return cur_size < size
        
        def comp(a,b):
            return reverse ^ (a < b)

        while cond():
            el = s.pop()
            if comp(el, p):
                l_size += 1
                l.push(el)
            else:
                g_size += 1
                g.push(el)
            cur_size += 1
        s.push(p)
        g = sort_single(g, s, l, g_size, not reverse)
        l = sort_single(l, g, s, l_size, not reverse)
        p = s.pop()
        cur_g_size = 0
        cur_l_size = 0
        while cur_g_size < g_size:
            cur_g_size += 1
            s.push(g.pop())
        s.push(p)
        while cur_l_size < l_size:
            cur_l_size += 1
            s.push(l.pop())
        if size is not None:
            pass
            #print(f"{string}\nFinal sort: {s.stack[-(size+1):]}\n")
        return s
    sort_single(stack1, stack2, stack3, None, False)

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def get_value(self):
        return self.value


class Stack:
    def __init__(self, operation_counter, element_counter, initial=None):
        self.stack = []
        if initial is not None:
            self.stack = initial

        self.element_counter = element_counter
        self.operation_counter = operation_counter

    def push(self, value):
        if self.element_counter.get_value() <= 0:
            raise RuntimeError(
                "Du kan ikke ta vare på flere elementer på "
                "stakkene enn det fantes originalt."
            )
        self.stack.append(value)
        self.element_counter.decrement()
        self.operation_counter.increment()

    def pop(self):
        if self.element_counter.get_value() >= 2:
            raise RuntimeError(
                "Du kan ikke ha mer enn 2 elementer i minnet " "av gangen."
            )
        self.element_counter.increment()
        self.operation_counter.increment()
        return self.stack.pop()

    def peek(self):
        self.operation_counter.increment()
        return self.stack[-1]

    def empty(self):
        return len(self.stack) == 0

import random
r = [i for i in range(110)]
random.shuffle(r)
# Tester, høyre side blir toppen av stakken
tests = (
    [4, 3, 2, 1],
    [1, 2, 3, 4],
    [4, 2, 1, 7],
    [1, 1, 1, 1],
    [7, 3, 9, 2, 0, 1, 3, 4],
    [7, 3, 0, 13, 48, 49, 233, 9, 2, 0, 1, 3, 4],
    [7, 97, 38, 21, 39, 12, 33, 12, 88, 46, 63, 82, 32, 37, 3, 0, 12, 13, 48]
    + [49, 233, 9, 2, 0, 1, 3, 4],
    r
)

failed = False

for test in tests:
    counter1 = Counter()
    counter2 = Counter()
    stack1 = Stack(counter1, counter2, initial=test[:])
    stack2, stack3 = Stack(counter1, counter2), Stack(counter1, counter2)

    sort(stack1, stack2, stack3)

    result = []
    counter2.value = float("-inf")
    while not stack1.empty():
        result.append(stack1.pop())

    if result != sorted(test):
        print(
            "Feilet for testen {:}, resulterte i listen".format(test)
            + "{:} i stedet for {:}.".format(result, sorted(test))
        )
        failed = True
    else:
        print(
            "Koden brukte {:}".format(counter1.get_value() - len(result))
            + " operasjoner på sortering av {:}".format(test)
        )

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
