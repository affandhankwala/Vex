import matplotlib.pyplot as plt
import TakePositions
def plotRR(name):
    # Plot the gain versus rr per different rr
    # Plot from 0.4 - 3 in 0.2 increment
    graph = [None for _ in range(29)]
    iterator = 0.1
    index = 0
    while iterator <= 3:
        graph[index] = TakePositions.takePositions(name, iterator)
        iterator += 0.1
        index += 1
    
    # Find the best RR
    bestGain = -1
    rr = -1
    for i in range(len(graph)):
        if graph[i] > bestGain:
            bestGain = graph[i]
            rr = i
    print("Most Gain at: "+(str)(rr * 0.1 + 0.1)+" with gain of "+(str)(bestGain))

    plt.plot(graph, label = "Gain")
    plt.xlabel("RR")
    plt.ylabel("Gain")
    plt.grid(True)
    plt.legend()
    plt.show()

def testOneRR(name):
    rr = 0.1
    TakePositions.takePositions(name, rr)
    
#plotRR('AUDUSD_2023-2024.csv')
testOneRR('AUDUSD_2023-2024.csv')