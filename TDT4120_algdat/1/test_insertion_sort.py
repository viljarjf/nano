#!/usr/bin/python3
# coding=utf-8


def insertion_sort(A):
    if not isinstance(A, list):
        return []
    if not len(A):
        return []
    
    sorted_list = []
    for i, el in enumerate(A):
        # do nothing with first element
        if not i:
            sorted_list.append(el)
        else:
            for j, sel in enumerate(sorted_list):
                if el < sel:
                    sorted_list.insert(j, el)
                    break
                # new greatest element
                elif j == i-1:
                    sorted_list.append(el)
    return sorted_list


if __name__ == "__main__":
    tests = [
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([3, 2, 1], [1, 2, 3]),
        ([9, 7, 3, 5, 2, 6], [2, 3, 5, 6, 7, 9]),
        ([-1, 1, -1, 2], [-1, -1, 1, 2]),
    ]

    for test, solution in tests:
        answer = insertion_sort(test)
        if answer != solution:
            print(
                "`insertion_sort` feilet for listen {:}. ".format(test)
                + "Svaret skulle vært {:}, men var {:}.".format(
                    solution, answer
                )
            )
