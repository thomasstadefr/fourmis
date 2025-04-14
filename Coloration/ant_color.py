from random import uniform, choices
from city_graph_color import Edge, Node, CityGraph

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
        
        self.__pos = pos_init
        
        self.__nb_colors: int = 0
        self.__coloration: dict[int, int] = {}
        
        self.__metric = metric
        self.__score: float = self.__metric(self)
        

    def get_pos(self) -> Node:
        return self.__pos
    
    
    
    def get_coloration(self) -> dict[int, int]:
        return self.__coloration
    
    def set_color(self, r: Node, c: int) -> None:
        if self.is_new(c):
            self.__nb_colors += 1
        self.__coloration[r.get_id()] = c
        
    
    def get_nb_colors(self) -> int:
        return self.__nb_colors
    
    
    
    def get_q(self) -> float:
        return self.__q
    
    def get_alpha(self) -> float:
        return self.__alpha
    
    def get_beta(self) -> float:
        return self.__beta



    def get_score(self) -> float:
        return self.__score
    
    def update_score(self) -> None:
        self.__score: float = self.__metric(self)
        
        
        
    # détermine si une couleur n'est pas déjà utilisée dans la coloration en cours
    def is_new(self, color: int) -> bool:
        return not(color in self.__coloration.values())
    
       
    # détermination de la distribution de couleurs disponibles à la position actuelle 
    def score_choices(self, r: Node) -> tuple[list[int], list[float], int]:
        
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

    def next_color(self, r: Node) -> int:
        lst_available_colors, l_scores, max_color = self.score_choices(r)
        
        if self.__q <= Ant.q0:
            color = choices(lst_available_colors, l_scores)[0]
        else:
            color = max_color
        return color
    
        
        
    # Application de la meilleur coloration après une étape de colonie
    def apply_coloration(self) -> None:
        g = self.__city_graph
        for (id, color) in self.__coloration:
            n = g.find_node_from_id(id)
            n.change_color(color)
        
        
    def reset_trip(self):
        self.__coloration = {}
        self.__nb_colors = 0
        
        
        
    '''
    Trajet effectué selon un parocurs en largeur,
    avec comme heuristique de choisir le noeud adjacent le plus contraint
    (ayant le moins de couleurs restantes disponibles)
    '''  
        
    def is_visited(self, n: Node) -> bool:
        return n.get_id() in self.__coloration.keys()
    
    def neighbours_to_vist(self, r:Node) -> list[Node]:
        return self.__city_graph.get_neighbours(r)
        
    def trip(self):
        lst_to_vist = [self.get_pos()]
        
        while lst_to_vist != []:
            # traitement du noeud suivant
            r = lst_to_vist.pop(0)
            
            color = self.next_color(r)
            self.set_color(r, color)
            
            l_neighbours = self.neighbours_to_vist(r)
            # propagation de l'information aux voisins : ces derniers ne peuvent pas choisir la même couleur
            for n in l_neighbours:
                if not(self.is_visited(n)):
                    n.prevent_color(color)
                    if not(n in lst_to_vist):
                        lst_to_vist.append(n)
                        
                        
            
    def __str__(self):
        txt_coloration = str(self.__coloration)
        return f"q : {self.__q:.3f}, alpha : {self.__alpha:.3f}, beta : {self.__beta:.3f}, coloration : {txt_coloration}, score : {self.__score:.3f}"
         
    def str_dynamic_result(self) -> str:
        return f"q : {self.__q:.3f}, alpha : {self.__alpha:.3f}, beta : {self.__beta:.3f}"



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
    alpha = uniform(0, 1)
    beta = uniform(0.5, 1.5)
    return Ant(city_graph, node, q, alpha, beta, metric)

def new_ant_clonage_mutation(city_graph: CityGraph, best_ant: Ant, node: Node, metric) -> Ant:
    q_best = best_ant.get_q()
    alpha_best = best_ant.get_alpha()
    beta_best = best_ant.get_beta()
    
    q_new = q_best * uniform(0.9, 1.1)
    if q_new > 1:
        q_new = 1
    alpha_new = alpha_best ** uniform(0.9, 1.1)
    beta_new = beta_best * uniform(0.9, 1.1)
    
    return Ant(city_graph, node, q_new, alpha_new, beta_new, metric)

def new_ant_crossover(city_graph: CityGraph, best_ant: Ant, node: Node, metric) -> Ant:
    q_best = best_ant.get_q()
    alpha_best = best_ant.get_alpha()
    beta_best = best_ant.get_beta()
    
    q_new = (q_best + uniform(0, 1))/2
    alpha_new = (alpha_best + uniform(0, 1))/2
    beta_new = (beta_best + uniform(0.5, 1.5))/2
    return Ant(city_graph, node, q_new, alpha_new, beta_new, metric)

def elite_ant(city_graph: CityGraph, ant: Ant, node: Node, metric) -> Ant:
    q = ant.get_q()
    alpha = ant.get_alpha()
    beta = ant.get_beta()
    return Ant(city_graph, node, q, alpha, beta, metric)



'''
Relation d'ordre entre les fourmis --> renvoie True ssi ant1 <= ant2.
'''

def compare_ants(ant1: Ant, ant2: Ant) -> bool:
    ant1_score = ant1.get_score()
    ant2_score = ant2.get_score()
    
    return ant1_score <= ant2_score