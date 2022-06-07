def read_pajek(filename: str) -> tuple[int, list[tuple[int, int]]]:
    """
    Read a pajek file and return it's data.

    Parameters
    ----------
    filename (str): pajek file's name.

    Returns
    -------
    int: number of nodes in the graph.
    list[tuple[int, int]]: directed arcs in the graph, from one node to another.
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
        arcs.extend([tuple(reversed(arc)) for arc in arcs])

    return n_nodes, arcs


class Graph:
    """Class for graph manipulation."""

    def __init__(self, N: int, arcs: list[tuple[int, int]]):
        """
        Generate a directional graph's adjacency matrix and each node's adjacency list off of a Pajek file's data.

        Parameters
        ----------
        N (int): The graph's number of nodes.
        edges (list[tuple[int, int]]): Each of the graph's nodes' nodes.
        """
        if type(N) is not int or type(arcs) is not list:
            raise TypeError(
                "`N` must be an `int` and `edges` must be a `list` of `tuples` containing two `int`."
            )

        M = [[0 for _ in range(N)] for _ in range(N)]
        neighbors: dict[int, set[int]] = {i: set([]) for i in range(N)}

        for edge in arcs:
            if (
                type(edge) is not tuple
                or len(edge) != 2
                or any([(type(v) is not int) for v in edge])
            ):
                raise TypeError(
                    "`edges` must be a `list` of `tuples` containing two `int`."
                )

            i, j = [v - 1 for v in edge]

            if i >= N or j >= N:
                raise ValueError("`edges` contain invalid nodes.")

            # register arc
            M[i][j] = 1
            neighbors[i].add(j)

        self.N = N
        self.matrix = M
        self.neighbors = neighbors

    def dft(self, root: int) -> list[int]:
        """
        Perform a Depth First Traversal, returning the list of visited edges.

        Parameters
        ----------
        root (int): the initial node's index.

        Returns
        -------
        list[int]: list of all edges connected `root`.
        """
        # list of all nodes to be analyzed - works as stack
        to_analyze = [root]
        # list of all nodes already analyzed
        history = set([])

        # while to_analyze is not empty
        while to_analyze:
            # if the current node was already analyzed, skip it
            if (curr := to_analyze.pop()) in history:
                continue
            history.add(curr)

            # gets the current node's adjacency list
            adjacencies = [node for node in self.neighbors[curr] if node not in history]
            # pushs the neigbor nodes to the stack
            to_analyze.extend(adjacencies)

        return list(history)


if __name__ == "__main__":
    pajek_filename = input().strip()
    n_nodes, arcs = read_pajek(pajek_filename)

    graph = Graph(n_nodes, arcs)
    visited = set([])
    islands = []

    # count islands
    for node in range(n_nodes):
        if node in visited:
            continue

        connected = graph.dft(node)
        visited.update(connected)
        islands.append(len(connected))

    # print output
    print(len(islands))
    for n in sorted(islands, reverse=True):
        print(n)
