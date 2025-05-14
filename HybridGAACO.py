import random
from typing import override
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import concurrent.futures
from gen_graph import make_graph, rand_route
from ga import GA
from aco import ACO

class HybridGAACO:
    def __init__(self, cities:nx.DiGraph, concurrency=True, pop_size=50, mutation_rate=0.02, n_ants=20, alpha=1, beta=2, evaporation=0.5, update_callback=lambda i,r,d,t:None):
        self.cities = cities
        self.ga = GA(cities,pop_size,mutation_rate)
        self.aco = ACO(cities,n_ants,alpha,beta,evaporation)
        self.concurrency = concurrency
        self.update_callback = update_callback

    def create_solution(self, gens:int=1,pop=None):
        if pop:
            self.ga.population=pop
        return self.ga.create_solution(gens)

    def construct_solution(self,gens:int=1,ga_best=None):
        return self.aco.construct_solution(gens,ga_best)

    def run_ga_plus_aco(self, ga_generations=20, aco_iterations=10, cycles=5):
        BESTga=[]
        if self.concurrency:
            # self.ga.update_callback=self.update_callback
            with concurrent.futures.ProcessPoolExecutor() as ex:
                BESTga=list(ex.map(GA(self.ga.cities,self.ga.pop_size,self.ga.mutation_rate,None,True).create_solution,[ga_generations]*cycles))
        else:
            for ic in range(cycles):
                print(f"Cycle {ic+1}/{cycles}")
                self.ga.update_callback=lambda i,r,d,t:self.update_callback(i+(ga_generations*ic),r,d,t)
                BESTga.append(self.create_solution(ga_generations))
        # Flatten BESTga into a single list of routes
        flat_BESTga = sorted([route for sublist in BESTga for route in sublist[0]], key=lambda x: self.ga.route_distance(x))
        self.aco.update_callback=lambda i,r,d,t:self.update_callback(i+(ga_generations*cycles),r,d,t+(ga_generations*cycles))
        ACO_best, aco_dist, aco_history = self.construct_solution(aco_iterations, flat_BESTga)
        print("Best route from GA_ACO:", ACO_best[0])
        print("Best distance from GA_ACO:", aco_dist[0])
        return ACO_best[0], aco_dist[0], tuple(x for x in aco_history+tuple(x[1] for x in BESTga))

    def run_aco_plus_ga(self, ga_generations=20, aco_iterations=10, cycles=5):
        BESTaco=[]
        if self.concurrency:
            # self.aco.update_callback=self.update_callback
            with concurrent.futures.ProcessPoolExecutor() as ex:
                BESTaco=list(e[0] for e in ex.map(ACO(self.aco.cities,self.aco.n_ants,self.aco.alpha,self.aco.beta,self.aco.evaporation,None,True).construct_solution,[aco_iterations]*cycles))
        else:
            for ic in range(cycles):
                print(f"Cycle {ic+1}/{cycles}")
                self.aco.update_callback=lambda i,r,d,t:self.update_callback(i+(aco_iterations*ic),r,d,t)
                BESTaco.append(self.construct_solution(aco_iterations))
        # Flatten BESTaco into a single list of routes
        flat_BESTaco = sorted([route for sublist in BESTaco for route in sublist[0]], key=lambda x: self.aco.route_distance(x))
        self.ga.update_callback=lambda i,r,d,t:self.update_callback(i+(aco_iterations*cycles),r,d,t+(aco_iterations*cycles))
        GA_best,ga_history = self.create_solution(ga_generations, flat_BESTaco)
        ga_dist=self.ga.route_distance(GA_best[0])
        print("Best route from GA_ACO:", GA_best[0])
        print("Best distance from GA_ACO:", ga_dist)
        return GA_best[0], ga_dist, tuple(x for x in ga_history+tuple(x[2] for x in BESTaco))


if __name__ == "__main__":
    cities = make_graph(num_nodes=25,seed=656565)
    HybridGAACO_TEST= HybridGAACO(cities)

    BESTga,distance=HybridGAACO_TEST.run_ga_plus_aco(ga_generations=20, aco_iterations=10, cycles=5)

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
