#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

using Size = std::size_t;
using Weight = std::size_t;
using Vertex = std::size_t;
using AdjacencyList = std::vector<std::vector<Weight>>;
using Filter = std::vector<bool>;

template <typename TailEnd, typename TailLength>
std::pair<TailEnd, TailLength> measureColourlessTail(const AdjacencyList &adj, const Vertex &v, const Filter &covered)
{
    TailEnd end = 0;
    TailLength length = 0;

    for (const auto &neighbour : adj[v])
    {
        if (!covered[neighbour])
        {
            ++length;
            end = neighbour;
        }
    }

    return {end, length};
}

int main()
{
    Size nVertices;
    std::cin >> nVertices;

    AdjacencyList adj(nVertices);

    for (auto idx = 0; idx != nVertices; ++idx)
    {
        Size neighbourhoodSize;
        std::cin >> neighbourhoodSize;
        adj[idx].resize(neighbourhoodSize);

        for (auto neighbourIdx = 0; neighbourIdx != neighbourhoodSize; ++neighbourIdx)
        {
            std::cin >> adj[idx][neighbourIdx];
        }
    }

    Size coveringSize = 0;
    Filter covered(nVertices);

    while (std::count(covered.begin(), covered.end(), true) != nVertices)
    {
        for (auto idx = 0; idx != nVertices; ++idx)
        {
            if (!covered[idx])
            {
                Size tailEnd, tailLength;
                std::tie(tailEnd, tailLength) = measureColourlessTail<Vertex, Size>(adj, idx, covered);

                if (tailLength == 1)
                {
                    covered[idx] = true;
                    covered[tailEnd] = true;
                    ++coveringSize;
                }
                else if (tailLength == 0)
                {
                    covered[idx] = true;
                }
            }
        }
    }

    std::cout << coveringSize << std::endl;
}