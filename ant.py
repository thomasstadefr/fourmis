from random import uniform, choices
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
        gamma: float, # pour pondérer les choix de prochaine ville par la mémoire
        metric #: callable[Self, float]
    ):
        self.__q = q 
        self.__alpha = alpha
        self.__beta = beta
        self.__gamma = gamma
        self.__city_graph = city_graph
        self.__path_nodes: list[Node] = [pos_init]
        self.__path_edges: list[Edge] = []
        self.__num_visited: int = 1
        self.__L_path: float = 0
        self.__metric = metric #: callable[Self, float]
        self.__score: float = self.__metric(self)
        self.__finished: bool = False
        
    def is_finished(self) -> bool:
        return self.__finished

    def get_pos(self) -> Node:
        return self.__path_nodes[-1]
    
    def get_pos_init(self) -> Node:
        return self.__path_nodes[0]
    
    def get_path_nodes(self) -> list[Node]:
        return self.__path_nodes
    
    def get_path_edges(self) -> list[Edge]:
        return self.__path_edges
    
    def get_L_path(self) -> float:
        return self.__L_path
    
    def get_q(self) -> float:
        return self.__q
    
    def get_alpha(self) -> float:
        return self.__alpha
    
    def get_beta(self) -> float:
        return self.__beta
    
    def get_gamma(self) -> float:
        return self.__gamma

    def get_score(self) -> float:
        return self.__score
    
    def update_score(self) -> None:
        self.__score: float = self.__metric(self)
        
    def score_choices(self) -> tuple[list[Edge], list[float], Edge]:
        r = self.get_pos()
        l_edges = self.__city_graph.find_edges_from_node(r)
        l_scores: list[float] = []
        assert len(l_edges) > 0, "Graphe non fortement connexe"
        
        max_edge = l_edges[0]
        max_score = 0
        for e in l_edges:
            tau = e.get_pheromone()
            eta = 1 / e.get_distance()
            end = e.get_end()
            score: float = tau ** self.__alpha * eta ** self.__beta
            try:
                last_time = self.__path_nodes[::-1].index(end) # nombre d'étapes deppuis la dernière visite
            except ValueError: # noeud end jamais visité
                last_time = float("inf")        
            score *= 1 - (1 - self.__gamma) ** last_time # pondération par un premier ordre
            l_scores.append(score)
            if score > max_score:
                max_score = score
                max_edge = e
        return l_edges, l_scores, max_edge

    def next_city(self) -> Node:
        l_edges, l_scores, max_edge = self.score_choices()
        if self.__q <= Ant.q0:
            next_edge = choices(l_edges, l_scores)[0]
        else:
            next_edge = max_edge
        return next_edge.get_end()

    def move(self) -> None:
        start = self.get_pos()
        end = self.next_city()
        edge = self.__city_graph.find_edge(start, end)
        
        if end not in self.__path_nodes:
            self.__num_visited += 1
        self.__path_nodes.append(end)
        self.__path_edges.append(edge)
        self.__L_path += edge.get_distance()
        self.update_score()
        
    def reset_trip(self):
        self.__path_nodes = [self.get_pos_init()]
        self.__path_edges = []
        self.__L_path = 0
        self.__num_visited = 1
        self.__finished = False
        
    def trip(self) -> bool:
        # Renvoie si la fourmi a réussi
        # Autant de pas à faire que nombre de villes : une étape corrspond à un trajet complet 
        N_v = self.__city_graph.get_N_v()
        N_steps_max = 2 * N_v
        for _ in range(N_steps_max):
            self.move()
            if self.__num_visited == N_v and self.get_pos() == self.get_pos_init():  # Condition de complétude d'une tournée
                self.__finished = True
                break
            
    def __str__(self):
        txt_path = "["
        for node in self.__path_nodes:
            txt_path += str(node.get_id())
            txt_path += ","
        txt_path += "]"
        return f"q : {self.__q:.3f}, alpha : {self.__alpha:.3f}, beta : {self.__beta:.3f}, gamma : {self.__gamma:.3f}, path : {txt_path}, score : {self.__score:.3f}"
         
         
         
def random_population(city_graph: CityGraph, N_pop: int, metric) -> list[Ant]:
    ant_nodes = city_graph.random_nodes(N_pop)
    return [new_random_ant(city_graph, node, metric) for node in ant_nodes]
                
def new_random_ant(city_graph: CityGraph, node: Node, metric) -> Ant:
    q = uniform(0, 1)
    alpha = uniform(0.5, 1.5)
    beta = uniform(0.5, 1.5)
    gamma = uniform(0, 0.5)
    return Ant(city_graph, node, q, alpha, beta, gamma, metric)

def new_ant_clonage_mutation(city_graph: CityGraph, best_ant: Ant, node: Node, metric) -> Ant:
    q_best = best_ant.get_q()
    alpha_best = best_ant.get_alpha()
    beta_best = best_ant.get_beta()
    gamma_best = best_ant.get_gamma()
    
    q_new = q_best * uniform(0.9, 1.1)
    if q_new > 1:
        q_new = 1
    alpha_new = alpha_best * uniform(0.9, 1.1)
    beta_new = beta_best * uniform(0.9, 1.1)
    gamma_new = gamma_best * uniform(0.9, 1.1)
    if gamma_new > 1:
        gamma_new = 1
    return Ant(city_graph, node, q_new, alpha_new, beta_new, gamma_new, metric)

def new_ant_crossover(city_graph: CityGraph, best_ant: Ant, node: Node, metric) -> Ant:
    # TODO: faire un VRAI crossover, en faisant la moyenne avec une VRAIE ant
    q_best = best_ant.get_q()
    alpha_best = best_ant.get_alpha()
    beta_best = best_ant.get_beta()
    gamma_best = best_ant.get_gamma()
    
    q_new = (q_best + uniform(0, 1))/2
    alpha_new = (alpha_best + uniform(0.5, 1.5))/2
    beta_new = (beta_best + uniform(0.5, 1.5))/2
    gamma_new = (gamma_best + uniform(0, 0.5))/2
    return Ant(city_graph, node, q_new, alpha_new, beta_new, gamma_new, metric)

def elite_ant(city_graph: CityGraph, ant: Ant, node: Node, metric) -> Ant:
    q = ant.get_q()
    alpha = ant.get_alpha()
    beta = ant.get_beta()
    gamma = ant.get_gamma()
    return Ant(city_graph, node, q, alpha, beta, gamma, metric)