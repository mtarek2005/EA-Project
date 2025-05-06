import random
from typing import override
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from gen_graph import make_graph, rand_route
from ga import GA
from aco import ACO

class HybridGAACO:
    def __init__(self, cities:nx.DiGraph):
        self.cities = cities
        self.ga = GA(cities)
        self.aco = ACO(cities)

    def create_solution(self, gens:int=1):
        return self.ga.create_solution(gens)

    def construct_solution(self,iter:int=1,ga_best=None):
        return self.aco.construct_solution(iter,ga_best)

    def run(self, ga_generations=20, aco_iterations=10, cycles=5):
        BESTga=[]
        for i in range(cycles):
            print(f"Cycle {i+1}/{cycles}")
            BESTga.append(self.create_solution(ga_generations))
    # Flatten BESTga into a single list of routes
        flat_BESTga = sorted([route for sublist in BESTga for route in sublist], key=lambda x: self.ga.route_distance(x))
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
    




        

























if __name__ == "__main__":
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
