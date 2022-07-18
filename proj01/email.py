def read_pajek_from_stdin() -> tuple[int, list[tuple[int, int]]]:
    """
    Read a pajek file-like input from STDIN and return it's data.

    Returns
    -------
    int: number of nodes in the graph.
    list[tuple[int, int, int]]: directed arcs/undirected edges in the graph, from one node to another.
    """
    n_nodes = int(input().strip().split()[1])  # *Vertices N
    undirected = input().strip().lower() == "*edges"  # *Arcs or *Edges
    arcs = []

    # here a little hack is needed because we don't know
    # for sure exacly how many edges there are, so we
    # need to keep reading stdin until no input is given
    while True:
        # if an input is received parse it and append it to the edges list
        try:
            data = input().strip()
            if data:
                arcs.append(tuple(int(n) for n in data.split()))
        # End Of File error'll be fired when no input is received
        except EOFError:
            break

    if undirected:
        arcs.extend([(*reversed(arc[:2]), *arc[2:]) for arc in arcs])

    return n_nodes, arcs


class Graph:
    """Class for graph manipulation."""

    def __init__(self, N: int, arcs: list[tuple[int, int]]):
        """
        Generate a graph's adjacency matrix and each node's adjacency list off of a Pajek file's data.

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


if __name__ == "__main__":
    n_nodes, arcs = read_pajek_from_stdin()
    graph = Graph(n_nodes, arcs)

    # nodes we want to label with the same colors (minus one)
    targets = set([3, 4, 5, 6, 7, 8, 9, 10])

    # loop through the targets searching for the one that is neighbor
    # of more than one of the nodes in the list. if it is removed, the
    # remaining nodes can all be assigned the same color
    for target in targets:
        # target - 1 and n + 1 because the graph's indexes start at 0
        neighbors = graph.neighbors[target - 1]
        if len([n for n in neighbors if n + 1 in targets]) > 1:
            print(target)
            break
