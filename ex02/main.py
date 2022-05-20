def matrix_to_string(mat: list[list[int]]):
    """
    Convert a matrix to a string.

    Parameters
    ----------
    mat (list[list[int]]): the matrix to be converted.

    Returns
    -------
    str: the resulting string.
    """
    string = ""

    for row in mat:
        for i in range(len(row)):
            string += str(row[i])
            string += " " if i < len(row) - 1 else "\n"

    # remove trailing newline
    return string.rstrip()


class Graph:
    """Class for graph manipulation."""

    def __init__(self, N: int, edges: list[tuple[int, int]]):
        """
        Generate a non-directional graph's adjacency matrix and each node's adjacency list off of a Pajek file's data.

        Parameters
        ----------
        N (int): The graph's number of nodes.
        edges (list[tuple[int, int]]): Each of the graph's nodes' nodes.
        """
        if type(N) is not int or type(edges) is not list:
            raise TypeError(
                "`N` must be an `int` and `edges` must be a `list` of `tuples` containing two `int`."
            )

        M = [[0 for _ in range(N)] for _ in range(N)]
        neighbors = {i: set([]) for i in range(N)}

        for edge in edges:
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

            # register edge
            M[i][j] = M[j][i] = 1
            neighbors[i].add(j)
            neighbors[j].add(i)

        self.N = N
        self.matrix = M
        self.neighbors = neighbors

    def __str__(self) -> str:
        """
        Convert a graph into a string of it's adjacency matrix.

        Returns
        -------
        str: represents the graph's adjacency matrix.
        """
        return matrix_to_string(self.matrix)

    def bfs(self, root: int, target: int) -> list[int]:
        """
        Perform a Breadth First Search, returning the path that links the "root" node to the "target" node.

        Parameters
        ----------
            root (int): the initial node's index.
            target (int): the target node's index.

        Returns
        -------
            list[int]: path starting at "root" and ending at "target".
        """
        # list of all paths to be analyzed (the next node to be
        # visited is the last one on each path) - works as queue
        to_analyze = [[root]]

        # list of all nodes already analyzed
        history = set([])

        # while to_analyze is not empty
        while to_analyze:
            # current path (FIFO)
            path = to_analyze.pop(0)
            # currently being analyzed node
            curr = path[-1]

            # if the current node was already analyzed, skip it
            if curr in history:
                continue

            # gets the current node's adjacency list
            adjacencies = [node for node in self.neighbors[curr] if node not in history]

            # if the target is found
            if target in adjacencies:
                return path + [target]

            history.add(curr)

            # loops through each neighbor node, marking
            # a new path that ends in it to be analyzed
            to_analyze.extend([path + [node] for node in adjacencies])

        # if it got out of the loop, it means no path was found
        return []


if __name__ == "__main__":
    n_nodes = int(input().split()[1])  # *Vertices N
    input()  # *Edges
    edges = []

    # here a little hack is needed because we don't know
    # for sure exacly how many edges there are, so we
    # need to keep reading stdin until no input is given
    while True:
        # if an input is received parse it and append it to the edges list
        try:
            edges.append(tuple(int(n) for n in input().split()))  # V1 V2
        # End Of File error'll be fired when no input is received
        except EOFError:
            break

    graph = Graph(n_nodes, edges)

    # each element distancies[i][j] is the distance
    # between the graph's nodes of indexes i and j
    distancies = [[0 for _ in range(graph.N)] for _ in range(graph.N)]

    # calculate each distancy
    for i in range(graph.N):
        for j in range(i + 1, graph.N):
            distancies[i][j] = distancies[j][i] = len(graph.bfs(i, j)) - 1

    print(matrix_to_string(distancies))
