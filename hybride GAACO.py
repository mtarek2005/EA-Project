import random
from typing import override
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from gen_graph import make_graph, rand_route
from ga import GA
from aco import ACO

import abc 

class HybridGAACO(abc.ABC):
    def __init__(self, cities:nx.DiGraph):
        self.cities = cities
        self.ga = GA(cities)
        self.aco = ACO(cities)
        self.pop_size=60
        self.population = [self.ga.create_individual() for _ in range(self.pop_size)]
    @override
    def create_solution(self, gens:int=1):
        bests=[]
        if len(self.ga.population)==0:
            self.ga.population=[self.ga.create_individual() for _ in range(self.ga.pop_size)]
        for gen in range(gens):
            ranked = self.ga.rank_routes(self.ga.population)
            selection = self.ga.selection(ranked)
            next_gen = []
            while len(next_gen) < self.ga.pop_size:
                parent1, parent2 = random.choices(selection, k=2)
                child = self.ga.crossover_experimental(self.ga.population[parent1], self.ga.population[parent2])
                next_gen.append(self.ga.mutate(child))
            self.ga.population = sorted(self.ga.population, key=lambda x: self.ga.route_distance(x))[:self.ga.pop_size//2] + sorted(next_gen, key=lambda x: self.ga.route_distance(x))[:self.ga.pop_size//2]
            bests.append(min([self.ga.route_distance(x) for x in self.ga.population]))
        print(f"{gens} best:")
        print(bests)
        ga_best = sorted(self.ga.population, key=lambda x: self.ga.route_distance(x))
        ga_best = ga_best[:10]
        return ga_best
    @override
    def construct_solution(self,iter:int=1,ga_best=None):
        best_route = ga_best
        for ga_route in ga_best:
            self.aco.update_pheromones(ga_route, self.aco.route_distance(ga_route),pherm_rate=5)
            
        best_distance = float('inf')
        for _ in range(iter):    
            for _ in range(self.aco.n_ants):
                routes= self.aco.ant_tour()
                for route in routes:
                    if not route:
                        continue  # Skip if no valid route found
                    distance = self.aco.route_distance(route)
                    if distance < best_distance:
                        best_route = route
                        best_distance = distance
                    self.aco.update_pheromones(route, distance)
        return best_route, best_distance
    def run(self, ga_generations=20, aco_iterations=10, cycles=5):
        BESTga=[]
        for i in range(cycles):
            print(f"Cycle {i+1}/{cycles}")
            BESTga.append(self.create_solution(ga_generations))
    # Flatten BESTga into a single list of routes
        flat_BESTga = [route for sublist in BESTga for route in sublist]
        ACO_best, aco_dist = self.construct_solution(aco_iterations, flat_BESTga)
        print("Best route from GA_ACO:", ACO_best)
        print("Best distance from GA_ACO:", aco_dist)
        return ACO_best, aco_dist
            
            
                
                





    # def run(self, ga_generations=20, aco_iterations=10, cycles=5):
    #     for cycle in range(cycles):
    #         ga_best=self.ga.create_solution(ga_generations)
    #         best_overall, best_distance = self.aco.construct_solution(aco_iterations)
    #         if ga_best[1] < best_distance:
    #             best_overall = ga_best[0]
    #             best_distance = ga_best[1]
    #         self.aco.update_pheromones(best_overall, best_distance)
    #         self.population = [best_overall] + random.sample(
    #             self.population, len(self.population)-1)

    #     return best_overall, best_distance

###the run with aco first and then ga second
    # def run_ga_aco(self, ga_generations=20, aco_iterations=10, cycles=5):
    #     best_overall = None
    #     best_distance = float('inf')
    #     next_gen = []
    #     for cycle in range(cycles):
    #         print(f"Cycle {cycle+1}/{cycles}")

    #         # ACO Phase
    #         for _ in range(aco_iterations):
    #             aco_best, aco_dist = self.aco.construct_solution()
    #             if aco_dist < best_distance:
    #                 best_overall = aco_best
    #                 best_distance = aco_dist
    #             self.aco.update_pheromones(aco_best, aco_dist)
    #             next_gen.append(aco_best)
    #         #transfer to ga
    #         self.population = next_gen + random.sample(
    #             self.population, len(self.population)-len(next_gen))
    #         #ga phase
    #         for _ in range(ga_generations):
    #             ranked = self.ga.rank_routes(self.population)
    #             selection = self.ga.selection(ranked)
    #             next_gen = []
    #             while len(next_gen) < self.ga.pop_size:
    #                 parent1, parent2 = random.choices(selection, k=2)
    #                 child = self.ga.crossover(self.population[parent1],
    #                                         self.population[parent2])
    #                 next_gen.append(self.ga.mutate(child))
    #             self.population = next_gen
    #         best_overall = max(self.population, key=lambda x: self.ga.route_distance(x))
    #         best_distance = self.ga.route_distance(best_overall)
    #     return best_overall, best_distance
    




        


























cities = make_graph(num_nodes=25,seed=656565)
HybridGAACO_TEST= HybridGAACO(cities)

BESTga,distance=HybridGAACO_TEST.run(ga_generations=20, aco_iterations=10, cycles=5)

positions = nx.get_node_attributes(cities,"pos")
edge_labels = nx.get_edge_attributes(cities, 'weight')
# Ensure BESTga is a flat list of nodes
if not isinstance(BESTga, list) or not all(isinstance(node, int) for node in BESTga):
    raise ValueError("BESTga must be a flat list of node identifiers.")

# Construct edges for the best route
route_edges = [(BESTga[i], BESTga[i+1]) for i in range(len(BESTga)-1)]

# Draw the graph
nx.draw_networkx(
    cities, 
    positions, 
    with_labels=True, 
    node_size=500, 
    node_color='lightblue', 
    arrows=True, 
    width=4
)

# Highlight the best route
nx.draw_networkx_edges(
    cities, 
    edgelist=route_edges, 
    pos=positions, 
    arrows=True, 
    width=1, 
    edge_color='red'
)

# Add edge labels
edge_labels = nx.get_edge_attributes(cities, 'weight')
nx.draw_networkx_edge_labels(
    cities, 
    positions, 
    edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()}
)

# Print and display the solution
print(f'GA_ACO Solution (Distance: {distance:.2f})')
plt.title(f'GA_ACO Solution (Distance: {distance:.2f})')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()
plt.show()