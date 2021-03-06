#!/usr/bin/python

import random
from graphtheory.structures.edges import Edge


class PlanarGraphFactory:
    """The class for planar graph generators."""

    def __init__(self, graph_class):
        """Get a graph class."""
        self.cls = graph_class

    def make_cyclic(self, n=1, directed=False):
        """Create a weighted cyclic topological graph."""
        graph = self.cls(n, directed)
        graph.edge_next = dict()
        graph.edge_prev = dict()
        weights = range(1, 1 + n)   # different weights
        random.shuffle(weights)
        for node in xrange(n):
            graph.add_node(node)
        L = []            # list of edges
        for i in xrange(n):
            edge1 = Edge(i, (i+1) % n, weights.pop())
            graph.add_edge(edge1)
            L.append(edge1)
        for i in xrange(n):
            # At the node i.
            edge1 = L[i]
            edge2 = L[(i+n-1) % n]
            graph.edge_next[edge1] = ~edge2
            graph.edge_next[~edge2] = edge1
            graph.edge_prev[edge1] = ~edge2
            graph.edge_prev[~edge2] = edge1
        return graph

# 1-------2
# |\     /|
# | \   / |
# |  \ /  |  wheel graph W_7
# 6---0---3  planar Halin graph
# |  / \  |
# | /   \ |
# |/     \|
# 5-------4

    def make_wheel(self, n=4, directed=False):
        """Create a weighted wheel topological graph."""
        if n < 4:
            raise ValueError("number of vertices must be greater than 3")
        graph = self.cls(n, directed)
        graph.edge_next = dict()
        graph.edge_prev = dict()
        weights = range(1, 1 + 2 * n - 2)
        random.shuffle(weights)
        for node in xrange(n):
            graph.add_node(node)
        hub = 0
        # L[0] and M[0] are empty for convenience.
        L = [None]            # list of edges, to the center
        M = [None]            # list of edges, circle
        for i in xrange(1, n):
            edge1 = Edge(i, hub, weights.pop())
            edge3 = Edge(i, i+1 if (i < n-1) else 1, weights.pop())
            graph.add_edge(edge1)
            graph.add_edge(edge3)
            L.append(edge1)
            M.append(edge3)
        for i in xrange(1, n):
            edge1 = L[i]
            edge2 = L[i+1 if (i < n-1) else 1]
            edge3 = M[i]
            edge4 = M[i-1 if i > 1 else n-1]
            # At the hub.
            graph.edge_next[~edge2] = ~edge1
            graph.edge_prev[~edge1] = ~edge2
            # At the node i.
            graph.edge_next[edge1] = edge3
            graph.edge_next[edge3] = ~edge4
            graph.edge_next[~edge4] = edge1
            graph.edge_prev[edge1] = ~edge4
            graph.edge_prev[~edge4] = edge3
            graph.edge_prev[edge3] = edge1
        return graph

# EOF
