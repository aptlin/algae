# Algae: Algorithmic Tidbits

## Graph

### Exact Minimum Cover of a Forest ([C++](/graph/forest/exact-minimum-vertex-cover/mvc.cpp))

- **Input**: a forest _G_, represented as an adjacency list

- **Output**: the exact size of the minimum vertex cover
- **Formatting**

  - **Input**:
    - **n**: the number of vertices
    - Line **idx**: indices of the vertices in the neighbourhood of the vertex **idx**
  - **Output**:
    - size of the minimum vertex cover
  - **Example**:

    - _Input_:
      ```
      4
      3 1 2 3
      1 0
      1 0
      1 0
      ```
    - _Output_:
      ```
      1
      ```

* **Algorithm**:
  - Colour each vertex black or white with regards to its _coloured tail_ (the number of vertices in the neighbourhood which have not been yet coloured, together with the last uncoloured vertex).
  - If the coloured tail is of length 1, colour the parent (original vertex) and child (the tip of the tail) nodes in black, increasing the counter for the size of the minimum vertex cover.
  - If the vertex does not have a tail, just colour it in black.

### Clustering ([Python](/graph/clustering/))

- [Agglomerative Algorithm](/graph/clustering/clustering.py)

  - Description:

  1. Sort the edges by weight
  2. Start building an MST, just like in Kruskal's algorithm, which automatically sorts your vertices into clusters
  3. Stop when you have the number of clusters you need

- [k-Means Algorithm](/graph/clustering/clustering.py)
  - [Description](https://jakevdp.github.io/PythonDataScienceHandbook/05.11-k-means.html)

## Further Resources

- [Awesome Algorithms](https://github.com/tayllan/awesome-algorithms#readme)
