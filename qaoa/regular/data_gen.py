import os

import networkx as nx


def gen_random_regular_graph(n_qubits, degree):
    G = nx.random_regular_graph(degree, n_qubits)
    return G


def main():
    import sys

    n_qubits = [10, 20, 40, 60, 80, 100]
    degree = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for n in n_qubits:
        for d in degree:
            if d >= n:
                continue
            os.makedirs(f"q{n}_regular{d}", exist_ok=True)
            for i in range(10):
                G = gen_random_regular_graph(n, d)
                with open(f"q{n}_regular{d}/i{i}.txt", "w") as f:
                    f.write(str(G.edges()))


if __name__ == "__main__":
    main()
