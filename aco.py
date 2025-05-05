import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from gen_graph import make_graph, rand_route

class ACO:
    def __init__(self, cities: nx.DiGraph, n_ants=20, alpha=1, beta=2, evaporation=0.5):
        self.cities = cities
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.node_list = list(cities.nodes())
        self.node_to_idx = {node: idx for idx, node in enumerate(self.node_list)}
        self.n_cities = len(self.node_list)
        self.pheromone = np.ones((self.n_cities, self.n_cities))

    def construct_solution(self,iter:int=1):
        best_route = None
        best_distance = float('inf')
        for _ in range(iter):
            for _ in range(self.n_ants):
                route = self.ant_tour()
                if not route:
                    continue  # Skip if no valid route found
                distance = self.route_distance(route)
                if distance < best_distance:
                    best_route = route
                    best_distance = distance
                self.update_pheromones(route, distance)
        return best_route, best_distance

    def ant_tour(self):
        unvisited = set(self.cities.nodes())
        if not unvisited:
            return []
        current = random.choice(list(unvisited))
        route = [current]
        unvisited.remove(current)
        while unvisited:
            neighbors = list(self.cities.neighbors(current))
            possible_next = [n for n in neighbors if n in unvisited]
            if not possible_next:
                possible_next = list(unvisited)
            probabilities = self.calculate_probabilities(current, possible_next)
            if not probabilities:
                next_city = random.choice(list(unvisited))
            else:
                next_city = random.choices(possible_next, weights=probabilities, k=1)[0]
            route.append(next_city)
            unvisited.remove(next_city)
            current = next_city
        return route

    def calculate_probabilities(self, current, possible_next):
        if not possible_next:
            return []
        current_idx = self.node_to_idx[current]
        total = 0.0
        pheromones = []
        for city in possible_next:
            city_idx = self.node_to_idx[city]
            pheromone = self.pheromone[current_idx][city_idx] ** self.alpha
            distance = self.route_distance([current,city])
            heuristic = (1.0 / distance) ** self.beta
            attraction = pheromone * heuristic
            pheromones.append(attraction)
            total += attraction
        if total == 0:
            return [1.0 / len(possible_next)] * len(possible_next)
        return [p / total for p in pheromones]

    def update_pheromones(self, route, distance,pherm_rate=1.0):
        if not route:
            return
        self.pheromone *= self.evaporation
        for i in range(len(route)):
            u = route[i]
            v = route[(i + 1) % len(route)]
            u_idx = self.node_to_idx[u]
            v_idx = self.node_to_idx[v]
            if self.cities.has_edge(u, v):
                self.pheromone[u_idx][v_idx] += pherm_rate / distance
    def route_distance(self, route):
        distance = 0.0
        for i in range(len(route)):
            u = route[i]
            v = route[(i + 1) % len(route)]
            if self.cities.has_edge(u, v):
                distance += self.cities[u][v].get('weight', 0.0)
            else:
                return float('inf')  # Path is invalid
        return distance
    
    def run_aco(self, iterations=10):
        best_route = None
        best_distance = float('inf')
        for _ in range(iterations):
            route, distance = self.construct_solution()
            if distance < best_distance:
                best_route = route
                best_distance = distance
        return best_route, best_distance
    
if __name__ == "__main__":
    # Example usage
    cities = make_graph(25, 0.7,3,5 )
    aco = ACO(cities, n_ants=25, alpha=1, beta=2, evaporation=0.5)
    best_route, best_distance = aco.run_aco(iterations=100)
    print("Best route:", best_route)
    print("Best distance:", best_distance)
    # Draw the graph
    positions = nx.get_node_attributes(cities, "pos")
    nx.draw(cities, pos=positions, with_labels=True, node_size=500, node_color='lightblue', font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(cities, 'weight')
    # Draw the best route
    route_edges = [(best_route[i], best_route[(i + 1) % len(best_route)]) for i in range(len(best_route)-1)]
    nx.draw_networkx_edges(cities, edgelist=route_edges, pos=positions, arrows=True, width=4, edge_color='red')
    plt.show()


    

