import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from gen_graph import make_graph, rand_route

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return np.sqrt((self.x - city.x)**2 + (self.y - city.y)**2)

# Genetic Algorithm Components
class GA:
    def __init__(self, cities: nx.DiGraph, pop_size=50, mutation_rate=0.02):
        self.cities = cities
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.population = [ ]

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
        cities_to_do=list(set(parent1))
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
                                                                            and not any((parent1[i]==individual[-2] and parent1[i+1]==individual[-1] and parent1[i+2]==individual[-2]) for i in range(len(parent1)-2))
                                                                            and not any((parent2[i]==individual[-2] and parent2[i+1]==individual[-1] and parent2[i+2]==individual[-2]) for i in range(len(parent2)-2))
                                                                            and len(list(G.neighbors(individual[-1])))>1
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
            individual=individual[:-1]+(nx.shortest_path(G,individual[-1],city,weight="weight") if nx.has_path(G,individual[-1],city) else nx.shortest_path(self.cities,individual[-1],city,weight="weight"))
        child=individual
        return child

    def mutate(self, individual):
        if len(individual)>3: #mutate?
            for i in range(len(individual)-2): #for every node in route
                if random.random() < self.mutation_rate: #try to mutate
                    neighbors=[e for e in self.cities.neighbors(individual[i]) if e != individual[i+1]] #neighbors to try to switch to
                    print(neighbors)
                    if len(neighbors)>1:
                        j = random.choice(neighbors) # choose random mutation
                        path=nx.shortest_path(self.cities,j,individual[i+2],weight="weight") # pathe from mutation choice to the next node
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
            bests.append(min([self.route_distance(x) for x in self.population]))
        print(f"{gens} best:")
        print(bests)
        ga_best = sorted(self.population, key=lambda x: self.route_distance(x))
        ga_best = ga_best[0]
        return ga_best


# Ant Colony Optimization Components
"""class ACO:
    def __init__(self, cities, n_ants=20, alpha=1, beta=2, evaporation=0.5):
        self.cities = cities
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.pheromone = np.ones((len(cities), len(cities)))

    def construct_solution(self):
        best_route = None
        best_distance = float('inf')
        for _ in range(self.n_ants):
            route = self.ant_tour()
            distance = self.route_distance(route)
            if distance < best_distance:
                best_route = route
                best_distance = distance
            self.update_pheromones(route, distance)
        return best_route, best_distance

    def ant_tour(self):
        cities = self.cities.copy()
        route = []
        current = random.choice(cities)
        route.append(current)
        cities.remove(current)
        while cities:
            probabilities = self.calculate_probabilities(current, cities)
            next_city = random.choices(cities, weights=probabilities)[0]
            route.append(next_city)
            cities.remove(next_city)
            current = next_city
        return route

    def calculate_probabilities(self, current, cities):
        total = 0
        pheromones = []
        current_idx = self.cities.index(current)
        for city in cities:
            city_idx = self.cities.index(city)
            pheromone = self.pheromone[current_idx][city_idx] ** self.alpha
            heuristic = (1 / current.distance(city)) ** self.beta
            pheromones.append(pheromone * heuristic)
            total += pheromone * heuristic
        return [p/total for p in pheromones]

    def update_pheromones(self, route, distance):
        self.pheromone *= self.evaporation
        for i in range(len(route)):
            a = self.cities.index(route[i])
            b = self.cities.index(route[(i+1)%len(route)])
            self.pheromone[a][b] += 1/distance
            self.pheromone[b][a] += 1/distance

    def route_distance(self, route):
        distance = 0
        for i in range(len(route)):
            distance += route[i].distance(route[(i+1)%len(route)])
        return distance

# Hybrid GA-ACO System
class HybridGAACO:
    def __init__(self, cities):
        self.cities = cities
        self.ga = GA(cities)
        self.aco = ACO(cities)
        self.population = [self.ga.create_individual() for _ in range(50)]

    def run(self, ga_generations=20, aco_iterations=10, cycles=5):
        best_overall = None
        best_distance = float('inf')

        for cycle in range(cycles):
            print(f"Cycle {cycle+1}/{cycles}")

            # GA Phase
            for _ in range(ga_generations):
                ranked = self.ga.rank_routes(self.population)
                selection = self.ga.selection(ranked)
                next_gen = []
                while len(next_gen) < self.ga.pop_size:
                    parent1, parent2 = random.choices(selection, k=2)
                    child = self.ga.crossover(self.population[parent1],
                                            self.population[parent2])
                    next_gen.append(self.ga.mutate(child))
                self.population = next_gen

            # Transfer to ACO
            ga_best =sorted(self.population, key=lambda x: self.ga.route_distance(x),reverse=True)
            ga_best= ga_best[:10]
            self.aco.pheromone = np.ones((len(self.cities), len(self.cities)))

            for citys in ga_best:
                for city in citys:
                    idx = self.cities.index(city)
                    self.aco.pheromone[idx] += 10  # Boost pheromones from GA solution

            # ACO Phase
            aco_best, aco_dist = self.aco.construct_solution()
            if aco_dist < best_distance:
                best_overall = aco_best
                best_distance = aco_dist

            # Transfer to GA
            self.population = [aco_best] + random.sample(
                self.population, len(self.population)-1)

        return best_overall, best_distance

###the run with aco first and then ga second
    def run_ga_aco(self, ga_generations=20, aco_iterations=10, cycles=5):
        best_overall = None
        best_distance = float('inf')
        next_gen = []
        for cycle in range(cycles):
            print(f"Cycle {cycle+1}/{cycles}")

            # ACO Phase
            for _ in range(aco_iterations):
                aco_best, aco_dist = self.aco.construct_solution()
                if aco_dist < best_distance:
                    best_overall = aco_best
                    best_distance = aco_dist
                self.aco.update_pheromones(aco_best, aco_dist)
                next_gen.append(aco_best)
            #transfer to ga
            self.population = next_gen + random.sample(
                self.population, len(self.population)-len(next_gen))
            #ga phase
            for _ in range(ga_generations):
                ranked = self.ga.rank_routes(self.population)
                selection = self.ga.selection(ranked)
                next_gen = []
                while len(next_gen) < self.ga.pop_size:
                    parent1, parent2 = random.choices(selection, k=2)
                    child = self.ga.crossover(self.population[parent1],
                                            self.population[parent2])
                    next_gen.append(self.ga.mutate(child))
                self.population = next_gen
            best_overall = max(self.population, key=lambda x: self.ga.route_distance(x))
            best_distance = self.ga.route_distance(best_overall)
        return best_overall, best_distance


"""
# Example usage
if __name__ == "__main__":
    # Create 25 random cities
    cities = make_graph(num_nodes=25,seed=656565)
    """
    hybrid = HybridGAACO(cities)
    best_route, best_distance = hybrid.run()
    best_route2, best_distance2 = hybrid.run_ga_aco()

    # Plot results
    x = [city.x for city in best_route]
    y = [city.y for city in best_route]
    plt.figure(figsize=(10, 6))
    plt.plot(x + [x[0]], y + [y[0]], 'b--', alpha=0.5, label='Route')
    plt.scatter(x, y, c='red', label='Cities')
    plt.title(f'Hybrid GA-ACO Solution (Distance: {best_distance:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()
    x = [city.x for city in best_route2]
    y = [city.y for city in best_route2]
    plt.figure(figsize=(10, 6))
    plt.plot(x + [x[0]], y + [y[0]], 'b--', alpha=0.5, label='Route')
    plt.scatter(x, y, c='red', label='Cities')
    plt.title(f'Hybrid ACO-GA Solution (Distance: {best_distance2:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()
    """
    GA_TEST= GA(cities)

    BESTga=GA_TEST.create_solution(40)

    distance= GA_TEST.route_distance(BESTga)

    positions = nx.get_node_attributes(cities,"pos")
    edge_labels = nx.get_edge_attributes(cities, 'weight')
    route_edges=[(BESTga[i],BESTga[i+1]) for i in range(len(BESTga)-1)]
    nx.draw_networkx(cities, positions, with_labels=True, node_size=500, node_color='lightblue', arrows=True, width=4)
    nx.draw_networkx_edges(cities, edgelist=route_edges, pos=positions, arrows=True, width=1, edge_color='red')
    nx.draw_networkx_edge_labels(cities, positions, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()})
    print(f'GA Solution (Distance: {distance:.2f})')
    plt.title(f'GA Solution (Distance: {distance:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()
    """
    ACO_TEST= ACO(cities)

    BESTACO,ACO_distance=ACO_TEST.construct_solution()






    x= [city.x for city in BESTACO]
    y= [city.y for city in BESTACO]
    plt.figure(figsize=(10, 6))
    plt.plot(x + [x[0]], y + [y[0]], 'b--', alpha=0.5, label='Route')
    plt.scatter(x, y, c='red', label='Cities')
    plt.title(f'ACO Solution (Distance: {ACO_distance:.2f})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()"""
