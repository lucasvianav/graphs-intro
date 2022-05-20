from random import random


class Graph:
    """Class for graphs manipulation, primarily working with it's adjacency matrix."""

    def __init__(self, N: int, p: float):
        """
        Generate an Erdös-Renyi non-directional graph's adjacency matrix.

        Parameters
        ----------
            N (int): The graph's number of vertices.
            p (float): The Erdös-Renyi parameter.
        """
        if type(N) is not int or type(p) is not float:
            raise TypeError("`N` must be an `int` and `p` must be a `float`.")

        if not (0 <= p <= 1):
            raise ValueError("The `p` value is invalid - it must be in [0, 1].")

        M = [[0 for _ in range(N)] for _ in range(N)]

        for i in range(N):
            for j in range(N):
                M[i][j] = M[j][i] = int(random() > p) if i > j else M[i][j]

        self.N = N
        self.p = p
        self.matrix = M

    def __str__(self) -> str:
        """
        Convert a graph into a string of it's adjacency matrix.

        Returns
        -------
            str: represents the graph's adjacency matrix.
        """
        string = ""

        for i in range(self.N):
            string += "[  "
            for j in range(self.N):
                string += str(self.matrix[i][j]) + "  "
            string += "]\n"

        return string


if __name__ == "__main__":
    N_prompt = "N (must be an int): "
    p_prompt = "p (must be a float betweeen 0 and 1): "

    def is_float(s: str):
        return s.replace(".", "").isdigit()

    while not (N := input(N_prompt)).isdigit():
        pass
    while not (is_float(p := input(p_prompt)) and 0 <= float(p) <= 1):
        pass

    graph = Graph(int(N), float(p))
    print("\nThe generated Erdös-Renyi non-directional graph is:", graph, sep="\n")
