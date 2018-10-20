from clustering import agglomerativeClustering, kMeansClustering, Edge
from collections import defaultdict
from pathlib import Path
from scipy.spatial import distance
import time

metrics = {
    "Euclidean": distance.euclidean,
    "City-block": distance.cityblock,
    "Correlation": distance.correlation,
}

clusteringMethods = {
    "Agglomerative": agglomerativeClustering,
    "k-Means": kMeansClustering,
}


class Timer:
    def __init__(self, start=time.time()):
        self.start = start

    def now(self):
        return time.time() - self.start


def test(
    filename,
    clusteringMethod,
    metric,
    nClusters=5,
    frequencyLowerBound=2,
    frequencyUpperBound=10,
):
    info = "Clustering method: {}\nNumber of clusters: {}\nData source: {}\n".format(
        clusteringMethod, nClusters, filename
    )
    info += "Metric: {}\n".format(metric)
    distance = metrics[metric]
    cluster = clusteringMethods[clusteringMethod]
    stopwatch = Timer()

    with open(filename) as f:
        nTexts = int(f.readline())
        nUniqueWords = int(f.readline())
        nLines = int(f.readline())

        wordFrequencyCount = [0] * nUniqueWords

        texts = [[] for _ in range(nTexts)]

        for _ in range(nLines):
            textID, wordID, wordFrequency = map(int, f.readline().split())
            wordFrequencyCount[wordID - 1] += wordFrequency
            if wordFrequency <= frequencyUpperBound:
                texts[textID - 1].append([wordID - 1, wordFrequency])

    def sieve(text):
        filteredText = []
        for token in text:
            wordID = token[0]
            if frequencyLowerBound <= wordFrequencyCount[wordID] <= frequencyUpperBound:
                filteredText.append(token)
        return filteredText

    texts = list(map(sieve, texts))
    info += "Analysing {} texts...\n".format(len(texts))

    def vectorise(text):
        representation = [0] * nUniqueWords
        for token in text:
            wordID, wordFrequency = token
            representation[wordID] += wordFrequency
        return representation

    edges = [
        Edge(i, j, distance(vectorise(texts[i]), vectorise(texts[j])))
        for i in range(len(texts) - 1)
        for j in range(i + 1, len(texts))
    ]

    info += "Built {} edges...\n".format(len(edges))

    label = cluster(len(texts), edges, nClusters)

    clusters = defaultdict(list)
    for textID in range(len(label)):
        clusters[label[textID]].append(textID + 1)

    info += "Clusters:\n"
    info += "cluster id,cluster size,cluster texts\n"
    for clusterID in clusters:
        info += "{},{},{}\n".format(
            clusterID, len(clusters[clusterID]), clusters[clusterID]
        )

    info += "\nRunning time: {0:.2f}s".format(stopwatch.now())
    return info


def run():
    dirpath = Path("results/")
    dirpath.mkdir(parents=True, exist_ok=True)
    for filename in Path().glob("data/test*"):
        for clusteringMethod in clusteringMethods:
            for metric in metrics:
                filepath = dirpath / "{}-{}-{}.txt".format(
                    filename.stem, clusteringMethod, metric
                )
                with filepath.open("w", encoding="utf-8") as f:
                    f.write(test(filename, clusteringMethod, metric))


if __name__ == "__main__":
    run()
