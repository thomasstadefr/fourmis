from random import uniform, choices
from city_graph_color import Edge, Node, CityGraph, str_path

class Ant:
    q0:float = 0.5
    
    def __init__(
        self,
        city_graph: CityGraph,
        pos_init: Node,
        q: float,
        alpha: float,
        beta: float,
        metric
    ):
        self.__q = q 
        self.__alpha = alpha
        self.__beta = beta
        
        self.__city_graph = city_graph
        self.__path_nodes: list[Node] = [pos_init]
        self.__path_edges: list[Edge] = []
        
        self.__num_visited: int = 1
        
        self.__nb_colors: int = 0
        self.__coloration: list[int] = []
        
        self.__metric = metric
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
    
    
    def get_coloration(self):
        return self.__coloration
    
    def get_nb_colors(self) -> int:
        return self.__nb_colors
    
    
    
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
        
        
    # détermine si une couleur n'est pas déjà utilisée dans la coloration en cours
    def is_new(self, color) -> bool:
        return not(color in self.__coloration)
       
    # détermination de la distribution de couleurs disponibles à la position actuelle 
    def score_choices(self) -> tuple[list[int], list[float], int]:
        r = self.get_pos()
        
        lst_available_colors = r.get_available_colors()
        pheromones = r.get_pheromones()
        
        alpha = self.__alpha
        beta = self.__beta
        
        l_scores = []
        
        max_color = lst_available_colors[0]
        max_score = 0
        
        for color in lst_available_colors:
            tau = pheromones[color]
            
            score = (1 - alpha*int(self.is_new(color))) * tau**beta
            l_scores.append(score)
            
            if score > max_score:
                max_score = score
                max_color = color
        return lst_available_colors, l_scores, max_color

    def next_color(self) -> int:
        lst_available_colors, l_scores, max_color = self.score_choices()
        
        if self.__q <= Ant.q0:
            color = choices(lst_available_colors, l_scores)[0]
        else:
            color = max_color
        return color


    def go_to(self, r: Node) -> None:
        edge = self.__city_graph.find_edge(self.get_pos(), r)
        
        if r not in self.__path_nodes:
            self.__num_visited += 1
        self.__path_nodes.append(r)
        self.__path_edges.append(edge)
        
        color = self.next_color()
        
        self.__coloration[r.get_id()] = color
        self.update_score()
        
        
    def reset_trip(self):
        self.__coloration = []
        self.__nb_colors = 0
        
        self.__path_edges = []
        self.__num_visited = 1
        self.__finished = False
        
    def trip(self) -> bool:
        '''
        Trajet effectué selon un parocurs en largeur,
        avec comme heuristique de choisir le noeud adjacent le plus contraint
        (ayant le moins de couleurs restantes disponibles)
        '''
        
        N_v = self.__city_graph.get_N_v()
        N_steps_max = 2 * N_v
        for _ in range(N_steps_max):
            self.move()
            if self.__num_visited == N_v:  # Condition de complétude d'une tournée
                self.__finished = True
                break
            
    def __str__(self):
        txt_path = str_path(self.get_path_nodes())
        return f"q : {self.__q:.3f}, alpha : {self.__alpha:.3f}, beta : {self.__beta:.3f}, path : {txt_path}, score : {self.__score:.3f}, finished : {self.__finished}"
         
    def str_dynamic_result(self) -> str:
        return f"q : {self.__q:.3f}, alpha : {self.__alpha:.3f}, beta : {self.__beta:.3f}, finished : {self.__finished}"



'''
Fonctions utiles pour Genetic : 
- création d'une fourmie puis population de fourmis aléatoire
- création d'une fourmi par mutation
- création d'une fourmi par crossover
- création d'une fourmi comme maintien d'une fourmi élite
'''

def random_population(city_graph: CityGraph, N_pop: int, metric) -> list[Ant]:
    ant_nodes = city_graph.random_nodes(N_pop)
    return [new_random_ant(city_graph, node, metric) for node in ant_nodes]
                
def new_random_ant(city_graph: CityGraph, node: Node, metric) -> Ant:
    q = uniform(0, 1)
    alpha = uniform(0.5, 1.5)
    beta = uniform(0.5, 1.5)
    return Ant(city_graph, node, q, alpha, beta, metric)

def new_ant_clonage_mutation(city_graph: CityGraph, best_ant: Ant, node: Node, metric) -> Ant:
    q_best = best_ant.get_q()
    alpha_best = best_ant.get_alpha()
    beta_best = best_ant.get_beta()
    
    q_new = q_best * uniform(0.9, 1.1)
    if q_new > 1:
        q_new = 1
    alpha_new = alpha_best * uniform(0.9, 1.1)
    beta_new = beta_best * uniform(0.9, 1.1)
    
    return Ant(city_graph, node, q_new, alpha_new, beta_new, metric)

def new_ant_crossover(city_graph: CityGraph, best_ant: Ant, node: Node, metric) -> Ant:
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



'''
Relation d'ordre entre les fourmis --> renvoie True ssi ant1 <= ant2.

Premier critère : finitude du trajet (coloration complète pour coloration).
Deuxième critère : longueur du trajet.
'''

def compare_ants(ant1: Ant, ant2: Ant) -> bool:
    ant1_score = ant1.get_score()
    ant2_score = ant2.get_score()
    ant1_complete = ant1.is_finished()
    ant2_complete = ant2.is_finished()
    
    if ant1_complete:
        if not(ant2_complete) or ant1_score < ant2_score:
            return True
    if not(ant2_complete) and ant1_score < ant2_score:
        return True
    return False