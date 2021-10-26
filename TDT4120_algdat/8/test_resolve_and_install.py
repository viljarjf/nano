#!/usr/bin/python3
# coding=utf-8

import random
import string

class Package:
    def __init__(self, dependencies, is_installed_func):
        self.__is_installed_func = is_installed_func
        self.__dependencies = dependencies

    @property
    def dependencies(self):
        return self.__dependencies

    @property
    def is_installed(self):
        return self.__is_installed_func(self)

    def __str__(self):
        return str(
            {
                "is_installed": self.is_installed,
                "dependencies": self.dependencies,
            }
        )

    def __repr__(self):
        return str(self)


def resolve_and_install(package: Package):
    if package.is_installed:
        return 
    q = [package, *package.dependencies]
    while q:
        dep = q.pop()
        if not dep.is_installed:
            if all([d.is_installed for d in dep.dependencies]):
                install(dep)
            else:
                q += [dep, *dep.dependencies]
    
    """
    # recursion slow
    if package.is_installed:
        return 
    else:
        for dep in package.dependencies:
            if not dep.is_installed:
                resolve_and_install(dep)
        install(package)
    """
        

# Hvis du ønsker nye tester, så endre dette tallet.
random.seed(123)


def get_install_func(installed_packages):
    def install(package):
        if package.is_installed:
            raise ValueError(
                'Du kjører "install" på en pakke som allerede er installert.'
            )
        if not all([p.is_installed for p in package.dependencies]):
            raise ValueError(
                'Du kjører "install" på en pakke uten å ha installert alle pakkene den er avhengig av.'
            )
        installed_packages.add(package)

    return install


def generate_random_test(num_nodes, p):
    installed_packages = set()
    is_installed_func = lambda x: x in installed_packages
    packages = [None for i in range(num_nodes)]
    incoming_edges = [[] for i in range(num_nodes)]
    installed_limit = random.randint(0, num_nodes)
    for i in range(1, num_nodes):
        predecessors = random.sample(
            range(0, i), k=random.randint(1, min(i, max(1, int(2 * p * i))))
        )
        for pre in predecessors:
            incoming_edges[pre].append(i)
    for i in range(num_nodes - 1, -1, -1):
        dependencies = tuple([packages[j] for j in incoming_edges[i]])
        packages[i] = Package(dependencies, is_installed_func)
        if i >= installed_limit:
            installed_packages.add(packages[i])
    return (packages[0], get_install_func(installed_packages))


def generate_install_tests():
    # Some small random tests
    for i in range(100):
        yield generate_random_test(random.randint(1, 5), 0.5)


for package, install_func in generate_install_tests():
    global install
    install = install_func
    try:
        resolve_and_install(package)
    except ValueError as e:
        response = str(e) + " Input: {:}".format(package)
        print(response)
        break
    if not package.is_installed:
        response = "Pakken er ikke installert. Input: {:}".format(package)
        print(response)
        break
