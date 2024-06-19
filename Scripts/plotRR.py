import matplotlib.pyplot as plt
import TakePositions
from typing import List

def plotRR(name: str, granularity: str, pair: str, open: List, close: List, high: List, low: List, show_graphs: bool) -> float:
    # Plot the gain versus rr per different rr
    # Plot from 0.4 - 3 in 0.2 increment
    graph = [None for _ in range(29)]
    iterator = 0.1
    index = 0
    while iterator <= 3:
        graph[index] = TakePositions.takePositions(name, iterator, pair, open, close, high, low)

        iterator += 0.1
        index += 1
    
    # Find the best RR
    bestGain = -1
    rr = -1
    for i in range(len(graph)):
        if graph[i] > bestGain:
            bestGain = graph[i]
            rr = i
    print("Granularity: "+granularity+"; Most Gain at: "+(str)(rr * 0.1 + 0.1)+" with gain of "+(str)(bestGain))
    if show_graphs:
        plt.plot(graph, label = "Gain")
        plt.xlabel("RR")
        plt.ylabel("Gain")
        plt.title(granularity)
        plt.grid(True)
        plt.legend()
        plt.show()

    return rr

def testOneRR(name):
    rr = 0.1
    TakePositions.takePositions(name, rr)
    
# pair = 'EURUSD'
# granularity = 'M1'
# name = f'{pair}_{granularity}_candles.csv'
# count = 500
# connectToOANDA.download_data(pair, granularity, count)

# plotRR(name, granularity)
# #testOneRR('AUDUSD_2023-2024.csv')