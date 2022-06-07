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

    def island_has_cycle(self, root: int) -> tuple[bool, list[int]]:
        """
        Determine if the island in which a node if located has a cycle - by performing a Depth First Traversal.

        Parameters
        ----------
        root (int): the initial node's index.

        Returns
        -------
        bool: if the island has a cycle.
        list[int]: list of visited edges.
        """
        # list of all paths to be analyzed (the next node to be
        # visited is the last one on each path) - works as stack
        to_analyze = [[root]]

        # list of all nodes already analyzed
        history = set([])

        # while to_analyze is not empty
        while to_analyze:
            # current path (LIFO)
            path = to_analyze.pop()
            # currently being analyzed node
            curr = path[-1]

            history.add(curr)

            # loop through each neighbor node, marking
            # a new path that ends in it to be analyzed
            for node in self.neighbors[curr]:
                if node in path:  # if a cycle was found
                    return True, list(history)
                to_analyze.append(path + [node])

        # if it got out of the loop, it means no cycle was found
        return False, list(history)

    def has_cycle(self) -> bool:
        """
        Determine if the graph has at least a cycle.

        Returns
        -------
        bool: if the graph has a cycle.
        """
        visited = set([])

        # look for cycles in each island
        for node in range(self.N):
            if node in visited:
                continue

            has_cycle, connected = self.island_has_cycle(node)

            if has_cycle:
                return True
            else:
                visited.update(connected)

        return False


if __name__ == "__main__":
    pajek_filename = input().strip()
    n_nodes, arcs = read_pajek(pajek_filename)
    graph = Graph(n_nodes, arcs)
    print("S" if graph.has_cycle() else "N")
