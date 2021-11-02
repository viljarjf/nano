# !/usr/bin/python3
# coding=utf-8


class Node:
    def __init__(self, ind):
        self.i = ind
        self.p = None
        self.r = 0

    def find_root(self):
        i = self
        while i.p is not None:
            i = i.p
        return i

    @staticmethod
    def union(node_1, node_2):
        if node_1.r > node_2.r:
            node_2.p = node_1
        else:
            node_1.p = node_2
            if node_1.r == node_2.r:
                node_2.r += 1

    def __eq__(self, other):
        if other is None:
            return False
        return self.i == other.i
    def __hash__(self):
        return hash(self.i)
    def __repr__(self):
        return self.i


def hamming_distance(s1, s2):
    return sum([i != j for i, j in zip(s1, s2)])


def find_clusters(E, n, k):
    """
    Finner k klynger ved hjelp av kantene i E. Kantenen i E er på
    formatet (i, j, avstand), hvor i og j er indeksen til noden (dyret)
    kanten knytter sammen og avstand er Hamming-avstanden mellom
    gensekvensen til dyrene. Funksjonen returnerer en liste av k
    lister. Hvor de indre listene representerer en klynge og består av
    indeksene til nodene (dyrene). F.eks. har vi tre dyr som skal
    i to klynger, hvor dyr 0 og 2 ender i samme klynge returnerer
    funksjonen [[0, 2], [1]].

    :param E: Kanter i grafen på formatet (i, j, avstand). i og j er
              indeksen til dyrene kanten går mellom.
    :param n: Antall noder
    :param k: Antall klynger som ønskes
    :return: En liste av k liste .
    """

    # MST_KRUSKAL
    nodes = [Node(i) for i in range(n)]
    edges = []
    E.sort(key = lambda i: i[-1])
    for i, j, _ in E:
        if nodes[i].find_root() != nodes[j].find_root():
            Node.union(nodes[i], nodes[j])
            edges.append((i, j))

    roots = set([nodes[i] if nodes[i].p is None else nodes[j]])
    ind = -1
    while len(roots) < k:
        i, j = edges[ind]
        ind -= 1
        if nodes[i].p == nodes[j]:
            nodes[i].p = None
        else:
            nodes[j].p = None
        roots.add(nodes[i]) if nodes[i].p is None else _
        roots.add(nodes[j]) if nodes[j].p is None else _

    roots = list(roots)

    res = [[] for _ in range(k)]
    for node in nodes:
        res[roots.index(node.find_root())].append(node.i)
    return res


def find_animal_groups(animals, k):
    # Lager kanter basert på Hamming-avstand
    E = []
    for i in range(len(animals)):
        for j in range(i + 1, len(animals)):
            E.append((i, j, hamming_distance(animals[i][1], animals[j][1])))

    # Finner klynger
    clusters = find_clusters(E, len(animals), k)

    # Gjøre om fra klynger basert på indekser til klynger basert på dyrenavn
    animal_clusters = [
        [animals[i][0] for i in cluster] for cluster in clusters
    ]
    return animal_clusters


tests = [
    ([("Ugle", "AGTC"), ("Ørn", "AGTA")], 2, 1),
    ([("Ugle", "CGGCACGT"), ("Elg", "ATTTGACA"), ("Hjort", "AATAGGCC")], 2, 8),
    (
        [("Ugle", "ATACTCAT"), ("Hauk", "AGTCTCAT"), ("Hjort", "CATGGCCG")],
        2,
        6,
    ),
    (
        [
            ("Ugle", "CGAAGTTA"),
            ("Hauk", "CGATGTTA"),
            ("Hamster", "AAAATCAC"),
            ("Mus", "AAAATGAC"),
        ],
        2,
        6,
    ),
    (
        [
            ("Ugle", "CAAACGAT"),
            ("Spurv", "CAGTCTAA"),
            ("Mus", "TCTGGACG"),
            ("Hauk", "CGAACTAT"),
        ],
        2,
        8,
    ),
    (
        [
            ("Ugle", "ATAACTCC"),
            ("Hauk", "TTACCTCC"),
            ("Hjort", "AGTGAACC"),
            ("Mus", "GTAGGACC"),
            ("Spurv", "ATGTCCCA"),
        ],
        3,
        4,
    ),
    (
        [
            ("Hauk", "CCTACTGATGACGCGC"),
            ("Ugle", "CCTAGTGATGAAGCAC"),
            ("Hjort", "ACTTTAACATCGCGGG"),
            ("Spurv", "ACGACTGATGAAGCAC"),
            ("Mus", "GTTAGACAATGGAGTG"),
            ("Rotte", "GTCGTACAATTGAGTG"),
        ],
        3,
        9,
    ),
    (
        [
            ("Ugle", "GGAGACCGGCTTCCTA"),
            ("Marsvin", "GCTACCTTGCTCACGT"),
            ("Hauk", "CGAGACCAGCTGCTGG"),
            ("Hjort", "GACATCTCTGTTCGGC"),
            ("Spurv", "GGAGACCGGCTTCCTG"),
            ("Rotte", "ACTACCTTGCGCACGA"),
            ("Mus", "TCTACCTTGCCCACGA"),
        ],
        3,
        10,
    ),
    (
        [
            ("Spurv", "TAGCAGTTCCTGAGAA"),
            ("Hjort", "ATGCATATCAGACGAT"),
            ("Ugle", "TAGCGATTTCAGAATT"),
            ("Rotte", "GACGGATTATTCCCCA"),
            ("Marsvin", "GAGGAATGGTAATCGC"),
            ("Hauk", "GATCGGTATCAGAACT"),
            ("Elg", "ATTCGTATAACCAAAG"),
            ("Mus", "GAGGGATGCTCCTCCC"),
        ],
        3,
        9,
    ),
    (
        [
            ("Katt", "CCGTGGTATCAAATAA"),
            ("Hjort", "TTACAGGCGGGCGTTC"),
            ("Hauk", "GGGAAATGAGCTTTCT"),
            ("Rotte", "ATCCTATAATGACCCT"),
            ("Elg", "TTGCATGCGGGCGATT"),
            ("Marsvin", "TTCGGCGGAGGTTCTA"),
            ("Mus", "ATCGGAGGAGGATCTC"),
            ("Ugle", "GGCTAGTGCGCTTTTT"),
            ("Spurv", "TGCCAGTCCGCTTTAT"),
        ],
        4,
        9,
    ),
    (
        [
            ("Hjort", "GATTACCCATGCTGGA"),
            ("Leopard", "TTTTCCTACCTAGTTA"),
            ("Ugle", "TCCCGGGAAGGGGATG"),
            ("Hauk", "TCCCAGCAAGGGGCTG"),
            ("Rotte", "CGCAGGACCGGAGGCA"),
            ("Spurv", "TCACGTGACGGGGGTG"),
            ("Katt", "TTTTCCTAACGGGTTA"),
            ("Mus", "CGCCGGAGCGAAACTA"),
            ("Elg", "GTATAGCTGTGCAGGA"),
            ("Marsvin", "AGCTGGGGCGTCAAGA"),
        ],
        4,
        9,
    ),
    (
        [
            ("Spurv", "AATCCCTGTAACGCGT"),
            ("Rotte", "CACCAGTCCGAGGAAC"),
            ("Leopard", "CACCCTATATCAAAGG"),
            ("Hauk", "AAATTGTCTCACGGGG"),
            ("Mus", "CACCACTCCTAGGAAC"),
            ("Elg", "ATGAGAGAGAGCTCCT"),
            ("Hjort", "ATGCTAGTGGGCCGCT"),
            ("Elefant", "TTTGAACAGTTTTAAT"),
            ("Marsvin", "AAGCCCTCAGAGCAAC"),
            ("Nesehorn", "TTTGACCAGTATTAAC"),
            ("Ugle", "AAAATGTCTAACGAGG"),
            ("Katt", "CACCCTATACCAAAGG"),
        ],
        5,
        9,
    ),
]

failed = False
import itertools

for animals, k, optimal in tests:
    clusters = find_animal_groups(animals[:], k)

    test = "(animals={:}, k={:})".format(animals, k)
    if type(clusters) != list:
        print(
            "find_animal_groups skal returnere en liste av klynger. For testen "
            + "{:} gjorde ikke implementasjonen din dette. Den ".format(test)
            + "returnerte heller {:}.".format(clusters)
        )
        failed = True
        break

    if len(clusters) != k:
        print(
            "Implementasjonen din lage ikke riktig antall klynger for testen "
            + "{:}. Du lagde {:} klynger.".format(test, len(clusters))
        )
        failed = True
        break

    cluster_animals = [animal for cluster in clusters for animal in cluster]
    if len(cluster_animals) > len(animals):
        print(
            "Klyngene dine inneholder flere elementer enn det som finnes. "
            + "Du returnerte {:} for testen {:}.".format(clusters, test)
        )
        failed = True
        break

    if len(cluster_animals) > len(set(cluster_animals)):
        print(
            "Klyngene dine inneholder duplikater. Du returnerte "
            + "{:} for testen {:}.".format(clusters, test)
        )
        failed = True
        break

    if set(name for name, _ in animals) != set(cluster_animals):
        print(
            "Klyngene dine inneholder ikke alle dyrene eller inneholder også "
            + " andre dyr. Du returnerte "
            + "{:} for testen {:}.".format(clusters, test)
        )
        failed = True
        break

    lookup = {
        animal: index
        for index, cluster in enumerate(clusters)
        for animal in cluster
    }
    t = lambda x: x[0] != x[1]
    sep_dist = min(
        sum(map(t, zip(a1[1], a2[1])))
        for a1, a2 in itertools.combinations(animals, 2)
        if lookup[a1[0]] != lookup[a2[0]]
    )
    if sep_dist < optimal:
        print(
            "Klyngene har ikke maksimal separasjonsavstand. Den maksimale "
            + "seperasjonsavstanden er {:}, men koden ".format(optimal)
            + "resulterte i en seperasjonsavstand på {:} ".format(sep_dist)
            + "for testen {:}".format(test)
        )
        print(clusters)
        failed = True
        break

if not failed:
    print("Koden fungerte for alle eksempeltestene.")
