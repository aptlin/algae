import numpy as np


# Adapted from
# https://github.com/keon/algorithms/blob/master/algorithms/graph/minimum_spanning_tree.py


class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointUnionSet:
    # The disjoint union set is represented as a list <n> of integers where
    # <n[i]> is the parent of the node at position <i>.
    # If <n[i]> = <i>, then <i> is the root, or head, of a set
    def __init__(self, nVertices):
        # Args:
        #   nVertices (int): The number of vertices in the graph

        # Map out parents of each node in the graph
        self.parent = np.arange(nVertices)

        # Map out the size of each disjoint set
        self.size = np.ones(nVertices)

    def mergeSet(self, a, b):
        # Args:
        #   a, b (int): Indices of two disjoint sets to merge

        # First, fetch the disjoint sets of nodes labelled <a> and <b>
        # If <a> and <b> correspond to root vertices,
        # the algorithm will work in O(1)

        a = self.findSet(a)
        b = self.findSet(b)

        # Join the shortest chain of nodes to the longest,
        # minimizing the tree size for a faster search
        if self.size[a] < self.size[b]:
            # Merge set(a) and set(b)
            self.parent[a] = b
            # Adjust the size of the disjoint set you get
            self.size[b] += self.size[a]
        else:
            # Merge set(b) and set(a)
            self.parent[b] = a
            # Add the size of old set(b) to set(a)
            self.size[a] += self.size[b]

    def findSet(self, a):
        if self.parent[a] != a:
            # Memoize the result of the recursion  to optimize future
            # calls, making the operation constant on average
            self.parent[a] = self.findSet(self.parent[a])

        # Return the head of the disjoint set
        return self.parent[a]

    def labelling(self):
        return list(map(self.findSet, self.parent))


def agglomerativeClustering(nNodes, edges, nClusters):
    # Args:
    #   nNodes (int): The number of vertices in the graph
    #   edges (list of Edge): The edges of the graph
    #   nClusters (int): The number of clusters
    #
    # Returns:
    #   labels: a list of clustering labels for each vertex
    #
    # The algorithm is a generalisation of Kruskal's MST algorithm.
    #
    # Procedure:
    #   Sort the edges by weight
    #   Start building an MST, just like in Kruskal's algorithm,
    #   which automatically sorts your vertices into clusters
    #   Stop when you have the number of clusters you need

    clusters = DisjointUnionSet(nNodes)

    edges.sort(key=lambda edge: edge.weight)

    connectedCentres = 0  # the number of clusters obtained
    for edge in edges:
        set_u = clusters.findSet(edge.u)  # Set of the node <u>
        set_v = clusters.findSet(edge.v)  # Set of the node <v>
        if set_u != set_v:
            clusters.mergeSet(set_u, set_v)
            connectedCentres += 1
            if connectedCentres == min(nNodes - nClusters, nNodes - 1):
                break

    return clusters.labelling()


def kMeansClustering(nNodes, edges, nClusters, seed=2):
    # Args:
    #   nNodes (int): The number of vertices in the graph
    #   edges (list of Edge): The edges of the graph
    #   nClusters (int): The number of clusters
    #
    # Returns:
    #   labels: a list of clustering labels for each vertex
    #
    # Procedure:
    #  Pick <nClusters> cluster centroids at random
    #  Assign labels to each vertex based on the closest centre

    clusters = DisjointUnionSet(nNodes)

    # Pick centres
    np.random.seed(seed)
    indices = np.random.permutation(nNodes)[:nClusters]
    centroids = set(clusters.parent[indices])

    # Save distances from the nodes on the periphery to the centroids
    distances = np.array(
        [[float("inf") for rowIdx in range(nNodes)] for colIdx in range(nNodes)]
    )
    for edge in edges:
        if edge.v in centroids:
            distances[edge.u][edge.v] = edge.weight

    periphery = set(range(nNodes)) - centroids

    # cluster periphery vertices and the nearest centroids together
    for node in periphery:
        clusters.mergeSet(
            clusters.findSet(node), clusters.findSet(np.argmin(distances[node]))
        )

    return clusters.labelling()

