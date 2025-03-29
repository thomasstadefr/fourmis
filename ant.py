import random
from typing import Self
from city_graph import Node, CityGraph

class Ant:
    def __init__(
        self,
        city_graph: CityGraph,
        pos_init: Node,
        metric #: callable[Self, float]
    ):
        self.__city_graph = city_graph
        self.__pos: Node = pos_init
        self.__path: list[Node] = [pos_init]
        self.__L_path: float = 0
        self.__metric = metric #: callable[Self, float]
        self.__score: float = self.__metric(self)

    def get_pos(self) -> Node:
        return self.__pos
    
    def get_path(self) -> list[Node]:
        return self.__path
    
    def get_L_path(self) -> float:
        return self.__L_path

    def get_score(self) -> float:
        return self.__score
    
    def update_score(self) -> None:
        self.__score: float = self.__metric(self)

    def next_city(self) -> Node:
        edges = CityGraph.find_edges_from_node(
            self.__city_graph,
            self.__pos
        )
        pheromones = [edge.get_pheromone() for edge in edges]
        next_edge = random.choices(edges, pheromones)[0]
        return next_edge.get_end()

    def move(self) -> None:
        start = self.__pos
        end = self.next_city()
        edge = self.__city_graph.find_edge(start, end)
        
        self.__path.append(end)
        self.__L_path += edge.get_distance()
        self.update_score()
        
    def trip(self) -> None:
        # Autant de pas à faire que nombre de villes : une étape corrspond à un trajet complet 
        N_steps = self.__city_graph.get_N_v()
        for _ in range(N_steps):
            self.move()
        
