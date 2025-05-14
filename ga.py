import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from gen_graph import make_graph, rand_route


# Genetic Algorithm Components
class GA:
    def __init__(self, cities: nx.DiGraph, pop_size=50, mutation_rate=0.02, update_callback=lambda i,r,d,t:None, conc=False):
        self.cities = cities
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.population = [ ]
        self.update_callback = update_callback if not conc else None

    def create_individual(self):
        print("indu")
        #return random.sample(self.cities, len(self.cities))
        individual,_=rand_route(self.cities)
        return individual


    def rank_routes(self, population):
        fitness_results = {i: 1/((self.route_distance(p)**2)) for i, p in enumerate(population)}
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    def selection(self, ranked_pop):
    # Select elites (top 50%)
        elites = [i for i, _ in ranked_pop[:self.pop_size//2]]

    # Select remaining 50% from non-elites (to avoid duplicates)
        non_elites = [i for i, _ in ranked_pop[self.pop_size//2:]]
        non_elite_weights = [f for _, f in ranked_pop[self.pop_size//2:]]

        remaining = random.choices(
            non_elites,
            weights=non_elite_weights,
            k=self.pop_size//2
        )

        return elites + remaining

    def crossover(self, parent1, parent2, perc_random=0.3):
        #graph route random crossover by combining graphs
        parent1_edges=[(parent1[i],parent1[i+1]) for i in range(len(parent1)-1)]
        parent2_edges=[(parent2[i],parent2[i+1]) for i in range(len(parent2)-1)]
        parent_graph=nx.DiGraph(parent1_edges+parent2_edges)
        child,_=rand_route(parent_graph,perc_random)
        return child

    def crossover_experimental(self, parent1, parent2, perc_random=0.8):
        #graph route random crossover by combining graphs
        parent1_edges=[(parent1[i],parent1[i+1]) for i in range(len(parent1)-1)]
        parent2_edges=[(parent2[i],parent2[i+1]) for i in range(len(parent2)-1)]
        parent_graph=nx.DiGraph(parent1_edges+parent2_edges)
        G=parent_graph
        individual=[]
        cities_to_do=list(self.cities.nodes)
        start=random.choice([parent1[0],parent2[0]])
        next_city=start
        individual.append(next_city)
        if next_city in cities_to_do:
            cities_to_do.remove(next_city)
        tries=min(len(parent1),len(parent2))
        while len(cities_to_do)>len(G.nodes)*(1.0-perc_random) and tries>0:
            if not ((len(list(G.neighbors(individual[-1])))==0)):
                print("neighbors: ")
                print(len(list(G.neighbors(individual[-1]))))
                next_city=random.choice(list(set(G.neighbors(individual[-1]))-({individual[-2]} if len(individual)>=2
                                                                            and len(list(G.neighbors(individual[-1])))>1
                                                                            and not any((parent1[i]==individual[-2] and parent1[i+1]==individual[-1] and parent1[i+2]==individual[-2]) for i in range(len(parent1)-2))
                                                                            and not any((parent2[i]==individual[-2] and parent2[i+1]==individual[-1] and parent2[i+2]==individual[-2]) for i in range(len(parent2)-2))
                                                                            else set())))
                #print(next_city,end=", ")
                individual.append(next_city)
                if next_city in cities_to_do:
                    cities_to_do.remove(next_city)
            else:
                individual+=nx.shortest_path(self.cities,individual[-1],individual[-2],weight="weight")[1:]
            print(len(cities_to_do))
            tries-=1
        for city in cities_to_do:
            individual=individual[:-1]+(nx.shortest_path(G,individual[-1],city,weight="weight") if G.has_node(city) and G.has_node(individual[-1]) and nx.has_path(G,individual[-1],city) else nx.shortest_path(self.cities,individual[-1],city,weight="weight"))
        child=individual
        return child

    def mutate(self, individual):
        if len(individual)>3: #mutate?
            for _ in range(len(individual)): #for every node in route
                if random.random() < self.mutation_rate: #try to mutate
                    i=random.choice(list(range(len(individual)-2)))
                    neighbors=[e for e in self.cities.neighbors(individual[i]) if e != individual[i+1]] #neighbors to try to switch to
                    print(neighbors)
                    print(f'i={i}, i+2={i+2} in len={len(individual)} and range={list(range(len(individual)-2))[-1]}')
                    if len(neighbors)>1:
                        j = random.choice(neighbors) # choose random mutation
                        path=nx.shortest_path(self.cities,j,individual[i+2],weight="weight") # path from mutation choice to the next node
                        if len(path)<2:
                            print(f"path: {path} shorter than 2")
                        individual=individual[:i+1]+path[:-1]+individual[i+2:] # stitch mutation into individual
        return individual

    def route_distance(self, route):
        # print(route)
        # print(self.cities.edges)
        distance = 0
        for i in range(len(route)-1):
            # print("from "+str(route[i]))
            # print("to "+str(route[i+1]))
            distance += self.cities.edges[route[i],route[i+1]]["weight"]
        return distance
    def create_solution(self, gens:int=1):
        bests=[]
        avgs=[]
        if len(self.population)==0:
            self.population=[self.create_individual() for _ in range(self.pop_size)]
        for gen in range(gens):
            ranked = self.rank_routes(self.population)
            selection = self.selection(ranked)
            next_gen = []
            while len(next_gen) < self.pop_size:
                parent1, parent2 = random.choices(selection, k=2)
                child = self.crossover_experimental(self.population[parent1], self.population[parent2])
                next_gen.append(self.mutate(child))
            self.population = sorted(self.population, key=lambda x: self.route_distance(x))[:self.pop_size//2] + sorted(next_gen, key=lambda x: self.route_distance(x))[:self.pop_size//2]
            dists=[self.route_distance(x) for x in self.population]
            bests.append(min(dists))
            avgs.append(sum(dists)/len(dists))
            if(self.update_callback):
                self.update_callback(gen,self.population[0],bests[-2] if len(bests)>1 else bests[-1],gens)
        print(f"{gens} best:")
        print(bests)
        ga_best = sorted(self.population, key=lambda x: self.route_distance(x))
        ga_best = ga_best[:10]
        return ga_best,(bests,avgs)





# Example usage
if __name__ == "__main__":
    # Create 25 random cities
    cities = make_graph(num_nodes=25,seed=656565)
    
    GA_TEST= GA(cities)

    BESTga,_=GA_TEST.create_solution(40)[0]

    distance= GA_TEST.route_distance(BESTga)

    positions = nx.get_node_attributes(cities,"pos")
    edge_labels = nx.get_edge_attributes(cities, 'weight')
    route_edges=[(BESTga[i],BESTga[i+1]) for i in range(len(BESTga)-1)]
    nx.draw_networkx(cities, positions, with_labels=True, node_size=500, node_color='lightblue', arrows=True, width=4)
    nx.draw_networkx_edges(cities, edgelist=route_edges, pos=positions, arrows=True, width=1, edge_color='red')
    # nx.draw_networkx_edge_labels(cities, positions, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()})
    print(f'GA Solution (Distance: {distance:.2f})')
    plt.title(f'GA Solution (Distance: {distance:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()
    
    
