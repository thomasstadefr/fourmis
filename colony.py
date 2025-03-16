from ant import Ant
from city_graph import City_graph

class Colony:
    def __init__(self, city_graph : City_graph, N_pop, evap_rate, Q, metric):
        self.__city_graph = city_graph
        self.__N_pop = N_pop
        self.__evap_rate = evap_rate
        self.__Q = Q
        self.__population = [Ant(city_graph, 0, metric) for _ in range(N_pop)] # todo

    def evaporation(self):
        edges = self.__city_graph.get_edges()
        for e in edges:
            e.set_pheromone((1-self.__evap_rate)*e.get_pheromone())
            e.set

    def created_pheromone(self):
        pop = self.__population
        g = self.__city_graph
                
        for ant in pop:
            path = ant.get_path()
            delta = self.__Q / ant.get_L_path()
            
            for i in range(len(path)-1):                    
                start = path[i]
                end = path[i+1]
                e = g.find_edge(start, end)
                e.set_pheromone(e.get_pheromone() + delta)
            
    def step(self):
        pop = self.__population
        for ant in pop:
            ant.trip()
            
        self.evaporation()
        self.created_pheromone()