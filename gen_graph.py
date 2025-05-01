import networkx as nx
import matplotlib.pyplot as plt
import random
import math

# Parameters
num_nodes = 25
edge_probability = 0.05  # Probability of edge creation between nodes
min_traffic = 1.0       # Minimum traffic factor
max_traffic = 2.0       # Maximum traffic factor
def make_graph(num_nodes:int = 25, edge_probability:float = 0.05, min_traffic:float = 1.0, max_traffic:float = 2.0, seed=None) -> nx.DiGraph:
    random.seed(seed)
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
    for i in G.nodes:
        if(G.in_degree(i)==0 or (G.in_degree(i)==1 and list(G.in_edges(i))[0][0]==i)):
            j=random.choice(list(G.nodes))
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            distance = math.hypot(x2 - x1, y2 - y1)
            traffic_factor = random.uniform(min_traffic, max_traffic)
            weight = distance * traffic_factor
            G.add_edge(j, i, weight=weight, distance=distance, traffic_factor=traffic_factor)
        if(G.out_degree(i)==0 or (G.out_degree(i)==1 and list(G.out_edges(i))[0][1]==i)):
            j=random.choice(list(G.nodes))
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            distance = math.hypot(x2 - x1, y2 - y1)
            traffic_factor = random.uniform(min_traffic, max_traffic)
            weight = distance * traffic_factor
            G.add_edge(i, j, weight=weight, distance=distance, traffic_factor=traffic_factor)
    return G
def rand_route(G:nx.DiGraph):
    individual=[]
    cities_to_do=list(G.nodes)
    start=random.choice(cities_to_do)
    next_city=start
    individual.append(next_city)
    cities_to_do.remove(next_city)
    while len(cities_to_do)>0 or next_city!=start:
        next_city=random.choice(list(G.neighbors(individual[-1])))
        if len(cities_to_do)==0 and start in list(G.neighbors(individual[-1])):
            next_city=start
        individual.append(next_city)
        if next_city in cities_to_do:
            cities_to_do.remove(next_city)
    #print(individual)
    route_edges=[(individual[i],individual[(i+1)%len(individual)]) for i in range(len(individual)-1)]
    return individual,route_edges
if __name__ == "__main__":
    G=make_graph(seed=508)
    print(G.nodes)
    print(G.edges)
    _, route_edges=rand_route(G)
    print(route_edges)
    # Draw the graph
    positions = nx.get_node_attributes(G,"pos")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, positions, with_labels=True, node_size=500, node_color='lightblue', arrows=True, width=4)
    nx.draw_networkx_edges(G, edgelist=route_edges, pos=positions, arrows=True, width=1, edge_color='red')
    nx.draw_networkx_edge_labels(G, positions, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()})
    plt.title("Random Directed Graph with Traffic-Adjusted Weights")
    plt.show()
