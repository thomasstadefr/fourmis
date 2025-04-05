#import random
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
        init_pheromone: float,
        metric #: callable[Ant, float]
    ):
        self.__city_graph: CityGraph = city_graph
        for edge in city_graph.get_edges():
            edge.set_pheromone(init_pheromone)
        self.__N_pop: int = N_pop
        self.__evap_rate: float = evap_rate
        self.__Q: float = Q
        self.__population: list[Ant] = population

    def evaporation(self) -> None:
        self.__city_graph.evaporate(self.__evap_rate)

    def created_pheromone(self) -> None:                
        for ant in self.__population:
            if ant.is_finished():
                path_edges = ant.get_path_edges()
                delta = self.__Q / ant.get_L_path()
                for e in path_edges:
                    e.increase(delta)

    def colony_step(self) -> None:
        for ant in self.__population:
            ant.reset_trip()
            ant.trip()
        self.evaporation()
        self.created_pheromone()
        
