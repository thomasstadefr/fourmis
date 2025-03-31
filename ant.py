import random
#from typing import Self
from city_graph import Edge, Node, CityGraph

class Ant:
    q0:float = 0.5
    
    def __init__(
        self,
        city_graph: CityGraph,
        pos_init: Node,
        q: float,
        alpha: float,
        beta: float,
        metric #: callable[Self, float]
    ):
        self.__q = q 
        self.__alpha = alpha
        self.__beta = beta
        self.__city_graph = city_graph
        self.__path: list[Node] = [pos_init]
        self.__num_visited: int = 1
        self.__L_path: float = 0
        self.__metric = metric #: callable[Self, float]
        self.__score: float = self.__metric(self)

    def get_pos(self) -> Node:
        return self.__path[-1]
    
    def get_pos_init(self) -> Node:
        return self.__path[0]
    
    def get_path(self) -> list[Node]:
        return self.__path
    
    def get_L_path(self) -> float:
        return self.__L_path

    def get_score(self) -> float:
        return self.__score
    
    def update_score(self) -> None:
        self.__score: float = self.__metric(self)
        
    def score_choices(self) -> tuple[list[Edge], list[float], Edge]:
        r = self.get_pos()
        l_edges = self.__city_graph.find_edges_from_node(r)
        l_scores: list[float] = []
        max_score = 0
        for e in l_edges:
            tau = e.get_pheromone()
            eta = 1 / e.get_distance()
            score: float = tau ** self.__alpha * eta ** self.__beta
            l_scores.append(score)
            if score > max_score:
                max_score = score
                max_edge = e
        return l_edges, l_scores, max_edge

    def next_city(self) -> Node:
        l_edges, l_scores, max_edge = self.score_choices()
        if self.__q <= Ant.q0:
            next_edge = random.choices(l_edges, l_scores)[0]
        else:
            next_edge = max_edge
        return next_edge.get_end()

    def move(self) -> None:
        start = self.get_pos()
        end = self.next_city()
        edge = self.__city_graph.find_edge(start, end)
        
        if end not in self.__path:
            self.__num_visited += 1
        self.__path.append(end)
        self.__L_path += edge.get_distance()
        self.update_score()
        
    def trip(self) -> None:
        # Autant de pas à faire que nombre de villes : une étape corrspond à un trajet complet 
        N_v = self.__city_graph.get_N_v()
        N_steps_max = 2*N_v
        for _ in range(N_steps_max):
            self.move()
            if self.__num_visited == N_v and self.get_pos() == self.get_pos_init():  # Condition de complétude d'une tournée
                break
            
    def __str__(self):
        txt_path = "["
        for node in self.__path:
            txt_path += str(node.get_id())
            txt_path += ","
        txt_path += "]"
        return f"q : {self.__q}, alpha : {self.__alpha}, beta : {self.__beta}, path : {txt_path}, score : {self.__score}"
         
         
def random_population(city_graph: CityGraph, N_pop: int, metric) -> list[Ant]:
    ant_nodes = city_graph.random_nodes(N_pop)
    return [random_ant(city_graph, node, metric) for node in ant_nodes]
                
def random_ant(city_graph: CityGraph, node: Node, metric) -> Ant:
    q = random.random()
    alpha = random.random()
    beta = random.random()
    return Ant(city_graph, node, q, alpha, beta, metric)
