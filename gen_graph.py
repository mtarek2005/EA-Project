import networkx as nx
import matplotlib.pyplot as plt
import random
import math

# Parameters
num_nodes = 4
edge_probability = 0.3  # Probability of edge creation between nodes
min_traffic = 1.0       # Minimum traffic factor
max_traffic = 2.0       # Maximum traffic factor

# Create a directed graph
G = nx.DiGraph()

# Assign random coordinates to each node
for i in range(num_nodes):
    x = random.uniform(0, 100)
    y = random.uniform(0, 100)
    G.add_node(i, pos=(x, y))

positions = nx.get_node_attributes(G,"pos")
# Add edges with weights based on distance and traffic
for i in G.nodes:
    for j in G.nodes:
        if i != j and random.random() < edge_probability:
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            distance = math.hypot(x2 - x1, y2 - y1)
            traffic_factor = random.uniform(min_traffic, max_traffic)
            weight = distance * traffic_factor
            G.add_edge(i, j, weight=weight, distance=distance, traffic_factor=traffic_factor)
print(G.nodes)
print(G.edges)
# Draw the graph
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, positions, with_labels=True, node_size=500, node_color='lightblue', arrows=True)
nx.draw_networkx_edge_labels(G, positions, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()})
plt.title("Random Directed Graph with Traffic-Adjusted Weights")
plt.show()
