import random
from ant import Ant
from city_graph import CityGraph

class Colony:
    def __init__(
        self,
        city_graph: CityGraph,
        population: list[Ant],
        N_pop: int,
        evap_rate: float,
        Q: float,
        metric #: callable[Ant, float]
    ):
        self.__city_graph: CityGraph = city_graph
        self.__N_pop: int = N_pop
        self.__evap_rate: float = evap_rate
        self.__Q: float = Q

        self.__population: list[Ant] = population


    def evaporation(self) -> None:
        edges = self.__city_graph.get_edges()
        for e in edges:
            e.set_pheromone(
                (1 - self.__evap_rate) * e.get_pheromone()
            )


    def created_pheromone(self) -> None:                
        for ant in self.__population:
            path = ant.get_path()
            delta = self.__Q / ant.get_L_path()
            
            for i in range(len(path) - 1):                    
                start = path[i]
                end = path[i + 1]
                e = self.__city_graph.find_edge(start, end)
                e.set_pheromone(e.get_pheromone() + delta)


    def step(self) -> None:
        for ant in self.__population:
            ant.trip()
        self.evaporation()
        self.created_pheromone()
