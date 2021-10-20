#!/usr/bin/python3
# coding=utf-8

class Node:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.character = None

    def __str__(self):
        return (
            f'{{ "left_child": {self.left_child}, "right_child": {self.right_child}, "character": '
            + (
                '"' + self.character + '"'
                if self.character is not None
                else "None"
            )
            + "}"
        )

    @classmethod
    def from_dict(cls, dic):
        node = Node()
        if dic["left_child"] is not None:
            node.left_child = Node.from_dict(dic["left_child"])
        if dic["right_child"] is not None:
            node.right_child = Node.from_dict(dic["right_child"])
        node.character = dic["character"]
        return node


def traverse(root: Node, path: str) -> Node:
    n = root
    for char in path:
        if char == "0":
            n = n.left_child
        elif char == "1":
            n = n.right_child
    return n

def encoding(root: Node):
    keys = [""]
    d = dict()
    while keys:
        key = keys.pop(0)
        n = traverse(root, key)
        if n.character is not None:
            d[n.character] = key
        else:
            keys.append(key + "0")
            keys.append(key + "1")
    return d
    


tests = [
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "n",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "a",
            },
            "character": None,
        },
        {"n": "0", "a": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "n",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "a",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "b",
                },
                "character": None,
            },
            "character": None,
        },
        {"n": "0", "a": "10", "b": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "c",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "a",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "b",
                },
                "character": None,
            },
            "character": None,
        },
        {"c": "0", "a": "10", "b": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "a",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "c",
            },
            "character": None,
        },
        {"a": "0", "c": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "a",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "b",
                },
                "right_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "c",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "d",
                    },
                    "character": None,
                },
                "character": None,
            },
            "character": None,
        },
        {"a": "0", "b": "10", "c": "110", "d": "111"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "a",
            },
            "right_child": {
                "left_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "b",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "d",
                    },
                    "character": None,
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "c",
                },
                "character": None,
            },
            "character": None,
        },
        {"a": "0", "b": "100", "d": "101", "c": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "a",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "b",
                    },
                    "character": None,
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "c",
                },
                "character": None,
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "d",
            },
            "character": None,
        },
        {"a": "000", "b": "001", "c": "01", "d": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "X",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "f",
            },
            "character": None,
        },
        {"X": "0", "f": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "X",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "B",
                },
                "character": None,
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "a",
            },
            "character": None,
        },
        {"X": "00", "B": "01", "a": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "K",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "B",
            },
            "character": None,
        },
        {"K": "0", "B": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "Y",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "F",
                },
                "character": None,
            },
            "right_child": {
                "left_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "O",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "M",
                    },
                    "character": None,
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "Q",
                },
                "character": None,
            },
            "character": None,
        },
        {"Y": "00", "F": "01", "O": "100", "M": "101", "Q": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "F",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "s",
            },
            "character": None,
        },
        {"F": "0", "s": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "S",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "z",
                },
                "right_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "b",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "O",
                    },
                    "character": None,
                },
                "character": None,
            },
            "character": None,
        },
        {"S": "0", "z": "10", "b": "110", "O": "111"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "R",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "e",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "T",
                },
                "character": None,
            },
            "character": None,
        },
        {"R": "0", "e": "10", "T": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "B",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "y",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "d",
                },
                "character": None,
            },
            "character": None,
        },
        {"B": "0", "y": "10", "d": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "u",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "q",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "z",
                },
                "character": None,
            },
            "character": None,
        },
        {"u": "0", "q": "10", "z": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "i",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "J",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "I",
                },
                "character": None,
            },
            "character": None,
        },
        {"i": "0", "J": "10", "I": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "T",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "K",
            },
            "character": None,
        },
        {"T": "0", "K": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "x",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "S",
                },
                "right_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "d",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "h",
                    },
                    "character": None,
                },
                "character": None,
            },
            "character": None,
        },
        {"x": "0", "S": "10", "d": "110", "h": "111"},
    ),
    (
        {
            "left_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "y",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "t",
                },
                "character": None,
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "d",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "L",
                },
                "character": None,
            },
            "character": None,
        },
        {"y": "00", "t": "01", "d": "10", "L": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "w",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "p",
                },
                "right_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "S",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "K",
                    },
                    "character": None,
                },
                "character": None,
            },
            "character": None,
        },
        {"w": "0", "p": "10", "S": "110", "K": "111"},
    ),
    (
        {
            "left_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "y",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "u",
                },
                "character": None,
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "U",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "a",
                },
                "character": None,
            },
            "character": None,
        },
        {"y": "00", "u": "01", "U": "10", "a": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "e",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "z",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "O",
                },
                "character": None,
            },
            "character": None,
        },
        {"e": "0", "z": "10", "O": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "s",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "S",
                },
                "right_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "l",
                },
                "character": None,
            },
            "character": None,
        },
        {"s": "0", "S": "10", "l": "11"},
    ),
    (
        {
            "left_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "g",
                },
                "right_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "E",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "i",
                    },
                    "character": None,
                },
                "character": None,
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "U",
            },
            "character": None,
        },
        {"g": "00", "E": "010", "i": "011", "U": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "G",
            },
            "right_child": {
                "left_child": None,
                "right_child": None,
                "character": "W",
            },
            "character": None,
        },
        {"G": "0", "W": "1"},
    ),
    (
        {
            "left_child": {
                "left_child": None,
                "right_child": None,
                "character": "A",
            },
            "right_child": {
                "left_child": {
                    "left_child": None,
                    "right_child": None,
                    "character": "E",
                },
                "right_child": {
                    "left_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "k",
                    },
                    "right_child": {
                        "left_child": None,
                        "right_child": None,
                        "character": "a",
                    },
                    "character": None,
                },
                "character": None,
            },
            "character": None,
        },
        {"A": "0", "E": "10", "k": "110", "a": "111"},
    ),
]


for test_case, answer in tests:
    node = Node.from_dict(test_case)
    student = encoding(node)
    if student != answer:
        response = "Koden feilet for følgende input: (data={:}). ".format(
            node
        ) + "Din output: {:}. Riktig output: {:}".format(student, answer)
        print(response)
        break
