# !/usr/bin/python3
# coding=utf-8
class Institution:
    def __init__(self, name, parent = None):
        self.name = name
        self.p = parent

class HigherEdSolver:
    def initialize(self, institutions):
        self.institutions = {i: Institution(i) for i in institutions}


    def parent_institution(self, institution):
        i = self.institutions[institution]
        while i.p is not None:
            i = i.p
        return i.name


    def fuse(self, institution1, institution2, new_institution):
        i = Institution(new_institution)
        self.institutions[new_institution] = i
        self.institutions[institution1].p = i
        self.institutions[institution2].p = i


class HigherEdTestCase:
    def __init__(self, calls, print_case):
        self.calls = calls
        self.print_case = print_case

    def test(self, initialize, parent_institution, fuse):
        for index, call in enumerate(self.calls):
            if call[0] == "initialize":
                initialize(call[1])
            elif call[0] == "parent_institution":
                res = parent_institution(call[1])
                assert res == call[2], (
                    "Kall:\n"
                    + self.calls_to_str(index + 1)
                    + '\nSistnevte returnerte "{:}", men skulle '.format(res)
                    + 'returnere "{:}"'.format(call[2])
                    if self.print_case
                    else "parent_institution returnerte feil"
                )
            elif call[0] == "fuse":
                fuse(call[1], call[2], call[3])

    def calls_to_str(self, index=None):
        s = ""
        for call in self.calls[:index]:
            if call[0] == "initialize":
                s += 'initialize(["' + '", "'.join(call[1]) + '"])'
            elif call[0] == "parent_institution":
                s += 'parent_institution("{:}")'.format(call[1])
            elif call[0] == "fuse":
                s += 'fuse("{:}", "{:}", "{:}")'.format(call[1], call[2], call[3])
            s += "\n"
        return s


tests = [
    [
        ("initialize", ["UniK", "UniR", "UniW"]),
        ("parent_institution", "UniK", "UniK"),
        ("parent_institution", "UniR", "UniR"),
        ("fuse", "UniK", "UniW", "UniC"),
    ],
    [
        ("initialize", ["UniP", "UniB", "UniY", "UniJ", "UniK"]),
        ("fuse", "UniK", "UniB", "UniT"),
        ("fuse", "UniY", "UniT", "UniM"),
        ("fuse", "UniP", "UniM", "UniV"),
        ("parent_institution", "UniK", "UniV"),
    ],
    [
        ("initialize", ["UniL", "UniQ", "UniB", "UniY", "UniU"]),
        ("parent_institution", "UniL", "UniL"),
        ("fuse", "UniY", "UniB", "UniF"),
        ("parent_institution", "UniB", "UniF"),
        ("fuse", "UniQ", "UniF", "UniX"),
        ("parent_institution", "UniY", "UniX"),
    ],
    [
        ("initialize", ["UniG", "UniS", "UniC", "UniU"]),
        ("parent_institution", "UniG", "UniG"),
        ("fuse", "UniS", "UniC", "UniM"),
    ],
    [
        ("initialize", ["UniB", "UniA", "UniE", "UniO", "UniG"]),
        ("parent_institution", "UniE", "UniE"),
        ("fuse", "UniO", "UniA", "UniN"),
        ("fuse", "UniG", "UniE", "UniD"),
        ("fuse", "UniN", "UniD", "UniW"),
        ("parent_institution", "UniB", "UniB"),
    ],
    [
        ("initialize", ["UniZ", "UniR", "UniM", "UniC", "UniW"]),
        ("fuse", "UniC", "UniM", "UniK"),
        ("parent_institution", "UniC", "UniK"),
    ],
    [
        ("initialize", ["UniE", "UniR", "UniK", "UniQ", "UniD"]),
        ("fuse", "UniD", "UniK", "UniN"),
        ("parent_institution", "UniR", "UniR"),
        ("parent_institution", "UniE", "UniE"),
        ("parent_institution", "UniQ", "UniQ"),
    ],
    [
        ("initialize", ["UniN", "UniZ", "UniY", "UniA", "UniF"]),
        ("fuse", "UniZ", "UniF", "UniK"),
        ("fuse", "UniN", "UniK", "UniX"),
        ("parent_institution", "UniZ", "UniX"),
        ("fuse", "UniA", "UniY", "UniC"),
    ],
    [
        ("initialize", ["UniG", "UniK", "UniI", "UniM"]),
        ("parent_institution", "UniG", "UniG"),
        ("fuse", "UniM", "UniI", "UniY"),
        ("fuse", "UniY", "UniG", "UniS"),
    ],
    [
        ("initialize", ["UniT", "UniK", "UniC"]),
        ("parent_institution", "UniC", "UniC"),
        ("fuse", "UniK", "UniC", "UniZ"),
    ],
    [
        ("initialize", ["UniX", "UniM", "UniY", "UniA", "UniI"]),
        ("fuse", "UniA", "UniI", "UniK"),
        ("parent_institution", "UniM", "UniM"),
        ("fuse", "UniM", "UniY", "UniU"),
        ("parent_institution", "UniI", "UniK"),
        ("fuse", "UniU", "UniK", "UniW"),
    ],
    [
        ("initialize", ["UniK", "UniZ", "UniY"]),
        ("parent_institution", "UniK", "UniK"),
        ("parent_institution", "UniK", "UniK"),
        ("fuse", "UniY", "UniZ", "UniQ"),
        ("parent_institution", "UniK", "UniK"),
        ("parent_institution", "UniY", "UniQ"),
    ],
    [
        ("initialize", ["UniC", "UniJ", "UniD", "UniI", "UniQ"]),
        ("fuse", "UniQ", "UniI", "UniB"),
        ("fuse", "UniC", "UniJ", "UniS"),
        ("parent_institution", "UniD", "UniD"),
        ("parent_institution", "UniI", "UniB"),
    ],
    [
        ("initialize", ["UniU", "UniO", "UniI", "UniS"]),
        ("fuse", "UniO", "UniS", "UniW"),
        ("parent_institution", "UniI", "UniI"),
        ("parent_institution", "UniU", "UniU"),
    ],
]


for test_case in tests:
    test_case = HigherEdTestCase(test_case, True)
    higher_ed_solver = HigherEdSolver()
    try:
        test_case.test(
            higher_ed_solver.initialize,
            higher_ed_solver.parent_institution,
            higher_ed_solver.fuse,
        )
    except AssertionError as e:
        print(str(e))
        break
