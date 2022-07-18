from heapq import heappop, heappush
from sys import maxsize as inf


def read_pajek(filename: str) -> tuple[int, list[tuple[int, int, int]]]:
    """
    Read a pajek file and return it's data.

    Parameters
    ----------
    filename (str): pajek file's name.

    Returns
    -------
    int: number of nodes in the graph.
    list[tuple[int, int, int]]: directed arcs/undirected edges in the graph, from one node to another.
    """
    with open(filename, "r") as f:
        n_nodes = int(f.readline().split()[1])  # *Vertices N
        undirected = f.readline().strip().lower() == "*edges"  # *Arcs or *Edges
        arcs = [
            tuple(int(n) for n in data.split())
            for line in f.readlines()
            if (data := line.strip())
        ]

    if undirected:
        arcs.extend([(*reversed(arc[:2]), *arc[2:]) for arc in arcs])

    return n_nodes, arcs


class Graph:
    """Class for graph manipulation."""

    def __init__(self, N: int, arcs: list[tuple[int, int, int]]):
        """
        Generate a directional graph's adjacency matrix and each node's adjacency list off of a Pajek file's data.

        Parameters
        ----------
        N (int): The graph's number of nodes.
        arcs (list[tuple[int, int, int]]): Connections and distances between nodes.
        """
        if type(N) is not int or type(arcs) is not list:
            raise TypeError(
                "`N` must be an `int` and `arcs` must be a `list` of `tuples` containing two `int`."
            )

        M = [[inf for _ in range(N)] for _ in range(N)]
        neighbors: dict[int, set[int]] = {i: set([]) for i in range(N)}

        for edge in arcs:
            if (
                type(edge) is not tuple
                or len(edge) != 3
                or any([(type(v) is not int) for v in edge])
            ):
                raise TypeError(
                    "`arcs` must be a `list` of `tuples` containing three `int`."
                )

            i, j = [v - 1 for v in edge[:2]]

            if i >= N or j >= N:
                raise ValueError("`edges` contain invalid nodes.")

            # register arc with given distance
            M[i][j] = edge[2]
            neighbors[i].add(j)

        self.N = N
        self.matrix = M
        self.neighbors = neighbors

    def prim(self) -> int:
        """
        Determine the shortest distance between two nodes with Dijkstra's Shortest Path Algorithm.

        Parameters
        ----------
        root (int): the initial node's index.
        target (int): the target node's index.

        Returns
        -------
        int: shortesst distance between `root` and `target`.
        """
        to_analyze = [(0, 0)]  # paths enqued (cost, node)
        history = set([])  # nodes already analyzed
        acc_cost = 0

        while len(history) < self.N:
            cost, curr = heappop(to_analyze)

            if curr in history:
                continue
            else:
                acc_cost += cost
                history.add(curr)

            for neighbor in self.neighbors[curr]:
                if neighbor not in history:
                    heappush(
                        to_analyze,
                        (self.matrix[curr][neighbor], neighbor),
                    )

        # no path found
        return acc_cost


if __name__ == "__main__":
    pajek_filename = input().strip()
    n_nodes, arcs = read_pajek(pajek_filename)
    graph = Graph(n_nodes, arcs)
    print(graph.prim())
