from ant_color import Ant
from city_graph_color import CityGraph

class Colony:
    def __init__(
        self,
        city_graph: CityGraph,
        population: list[Ant],
        N_pop: int,
        evap_rate: float,
        Q: float,
        init_pheromone: float
    ):
        self.__city_graph: CityGraph = city_graph
        
        N_v = self.__city_graph.get_N_v()
        for node in city_graph.get_nodes():
            node.init_pheromone(init_pheromone, N_v)
            
        self.__N_pop: int = N_pop
        self.__evap_rate: float = evap_rate
        self.__Q: float = Q
        self.__population: list[Ant] = population



    def evaporation(self) -> None:
        self.__city_graph.evaporate(self.__evap_rate)

    def augmentation(self) -> None:      
        l_nodes = self.__city_graph.get_nodes()
                  
        for ant in self.__population:
            coloration = ant.get_coloration()
            delta = self.__Q / ant.get_nb_colors()
            
            for n in l_nodes:
                for color in coloration.keys():
                    n.augmentation_pheromone(delta, color)



    def colony_step(self) -> None:
        g = self.__city_graph
        
        for ant in self.__population:
            ant.reset_trip()
            g.reset_available_colors()
            ant.trip()
        self.evaporation()
        self.augmentation()
        
