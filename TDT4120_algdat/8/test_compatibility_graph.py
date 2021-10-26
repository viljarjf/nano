#!/usr/bin/python3
# coding=utf-8


def compatibility_graph(donors: list[str], recipients: list[str], k: int):
    # good luck, future Viljar. 
    # Bad task anyway imo, weird requirements for the output format
    return [[j for j, r in enumerate(recipients) if sum([r[a_ind] == d[a_ind] for a_ind in range(len(d))]) >= k] for d in donors]

tests = [
    (([], [], 0), []),
    (([["ab"]], [], 0), [[]]),
    (([], [["ab"]], 0), []),
    (([["ab"]], [["ab"]], 1), [[0]]),
    (([["ab"]], [["ac"]], 1), [[]]),
    (([["ab"]], [["ac"]], 0), [[0]]),
    (([["ab"]], [["ac"], ["ab"]], 1), [[1]]),
    (([["ab"], ["ac"]], [["ab"]], 1), [[0], []]),
    (([["ab"], ["ac"]], [["ac"], ["ab"]], 1), [[1], [0]]),
    (([["ab"], ["ac"]], [["ac"], ["ab"]], 0), [[0, 1], [0, 1]]),
    (([["ab", "ac"]], [["ac", "ab"]], 1), [[]]),
    (
        ([["ab", "12"], ["ac", "22"]], [["ab", "22"], ["ac", "22"]], 2),
        [[], [1]],
    ),
    (([], [[], []], 1), []),
    (
        (
            [],
            [
                ["IRk", "s", "S", "9zF"],
                ["V2xa", "JqZV", "PxbUl", "WbKZw"],
                ["V2xa", "s", "PxbUl", "7NoD"],
            ],
            2,
        ),
        [],
    ),
    (
        (
            [["dwfAa", "bt7c", "d1iP"], ["dwfAa", "bt7c", "d1iP"]],
            [
                ["dwfAa", "H", "vN82"],
                ["dwfAa", "bt7c", "vN82"],
                ["dwfAa", "H", "vN82"],
            ],
            4,
        ),
        [[], []],
    ),
    (
        ([["oLfIi", "wPAw"], ["gTnJf", "wPAw"], ["gTnJf", "LERhd"]], [], 1),
        [[], [], []],
    ),
    (
        ([["uw"], ["uw"], ["Lb"], ["uw"]], [["4r7lb"], ["Lb"]], 1),
        [[], [], [1], []],
    ),
    (([["wcaP", "zXgJ"]], [], 1), [[]]),
    (([], [], 1), []),
    (
        (
            [["w", "oA", "oIa"]],
            [["w", "oA", "oIa"], ["d", "oA", "vodI"], ["w", "oA", "5"]],
            1,
        ),
        [[0, 1, 2]],
    ),
    (([], [["x", "7HyQl", "Wr38", "Ww"], ["x", "7HyQl", "yq", "Ww"]], 9), []),
    (([["rX1", "z"], ["rX1", "ZY2w"]], [["qX1Ph", "7a0M"]], 1), [[], []]),
]


for test_case, answer in tests:
    donors, recipients, k = test_case
    student = compatibility_graph(donors, recipients, k)
    if len(student) != len(answer) or not all(
        [sorted(stu) == ans for stu, ans in zip(student, answer)]
    ):
        response = (
            "Koden feilet for følgende input: "
            + "(donors={:}, recipients={:}, ".format(donors, recipients)
            + "k={:}). ".format(k)
            + "Din output: {:}. Riktig output: {:}".format(student, answer)
        )
        print(response)
        break
