import networkx as nx                                   # graph library 0
import random                                           # for random traffic levels 1
#from noise import pnoise2                               # Perlin noise 2
import matplotlib.pyplot as plt

def generate_city(
    num_nodes=50,
    connect_prob=0.08,
    traffic_range=(1, 10),
    perlin_scale=0.1,
    seed=None
):
    if seed is not None:
        random.seed(seed)
    G = nx.DiGraph()                                      # directed graph 3

    # 1. Create nodes and assign positions on a unit square
    for i in range(num_nodes):
        x, y = random.random(), random.random()           # uniform placement 4
        # altitude via Perlin noise, scaled to [0, 1]
        z = 0#(pnoise2(x / perlin_scale, y / perlin_scale) + 1) / 2
        G.add_node(i, pos=(x, y), altitude=z)             # node attrs: pos, altitude 5

    # 2. Add directed edges randomly
    for u in G.nodes():
        for v in G.nodes():
            if u != v and random.random() < connect_prob:
                # random traffic load
                traffic = random.uniform(*traffic_range)    # uniform traffic 6
                # optional cost incorporating slope
                dz = abs(G.nodes[u]['altitude'] - G.nodes[v]['altitude'])
                weight = traffic * (1 + dz)                # higher cost on steeper slopes 7
                G.add_edge(u, v, traffic=traffic, weight=weight)

    return G

# Example usage
if __name__ == "__main__":
    city = generate_city(num_nodes=100, connect_prob=0.05, seed=42)
    nx.draw_networkx(city,nx.get_node_attributes(city,"pos"))
    plt.show()
    # Access node attrs: city.nodes(data=True)
    # Access edge attrs: city.edges(data=True)
