import connectToOANDA
import matplotlib.pyplot as plt
import TakePositions

def plot_best_granularity():
    granularities = ['S30',
                     'M1', 'M2', 'M4', 'M5', 'M10', 'M15', 'M30',
                     'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D']
    pair = 'EURUSD'
    count = 500
    all_graphs = []
    best_granularity = ''
    best_gain = -1
    best_rr = 0
    for g in granularities:
        name = f'{pair}_{g}_candles.csv'
        connectToOANDA.download_data(pair, g, count)
        graph = []
        iterator = 0.1
        index = 0
        while iterator <= 5:
            graph.append(TakePositions.takePositions(name, iterator))
            iterator += 0.1

        for i in range(len(graph)):
            if graph[i] > best_gain:
                best_gain = graph[i]
                best_granularity = g
                best_rr = i
        # Add granularity to graph
        graph.append(g)
        # Add graph to total graphs
        all_graphs.append(graph)
    # Plot
    for graph in all_graphs:
        plt.plot(graph[:len(graph) - 1], label = graph[len(graph) - 1])
    print("Best gain at %i with a gain of %f in %s for %s" % (best_rr, round(best_gain, 2), best_granularity, pair))
    plt.xlabel("RR")
    plt.ylabel("Gain")
    plt.grid(True)
    plt.legend()
    plt.show()
    



plot_best_granularity()