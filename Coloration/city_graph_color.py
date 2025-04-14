from typing import Self
import random

class Node:
    id: int = 0
    def __init__(
        self,
        x: int,
        y: int
    ):
        self.__x = x
        self.__y = y
        
        '''
        On doit attendre de connaître le nombre de sommets (= nombre de couleurs max) avant de créer les tableaux associant
        une donnée à chaque couleur
        '''
        self.__available_colors: list[int] = []
        self.__nb_available_colors: int = 0
        
        self.__color: int = None  # couleur du noeud déterminé après une étape de colonie : selon la coloration du meilleur individu
        
        self.__pheromones: list[float] = []
        
        self.__id: int = Node.id
        Node.id += 1
        
    def get_id(self) -> int:
        return self.__id
        
    def get_x(self) -> int:
        return self.__x
    
    def get_y(self) -> int:
        return self.__y
        
    
    # Remise à zéro de la coloration du graphe au début de chque étape de colonie pour chaque fourmi
    def reset_available_colors(self, N_v: int) -> None:
        self.__available_colors = [i for i in range(0, N_v)]
        self.__nb_available_colors = N_v
        
    def get_available_colors(self) -> list[int]:
        return self.__available_colors    
    
    def prevent_color(self, c: int) -> None:
        if c in self.__available_colors:
            self.__available_colors.remove(c)
    
    
    
    def get_pheromones(self) -> list[float]:
        return self.__pheromones
            
    def get_color(self) -> int:
        return self.__color
    
    def change_color(self, new_color) -> None:
        self.__color = new_color
        
        
        
    # Gestion du taux de pheromone de chaque couleur
    
    # dépôt de phéromone initial à la réation du graphe
    def init_pheromone(self, ph0: float, N_V: int) -> None:
        self.__pheromones = [ph0 for _ in range(N_V)]
        
    # évaporation de la phéromone (pour toutes les couleurs)
    def evaporation_pheromone(self, evap_rate: float) -> None:
        ph = self.__pheromones
        nb_colors = len(ph)
        for color in range(nb_colors):
            ph[color] = (1-evap_rate)*ph[color]
            
    # augmentation de la phéromone (pour une couleur en particulier)
    def augmentation_pheromone(self, delta: float, color: int) -> None:
        self.__pheromones[color] += delta
        
        
    
    def __eq__(self, n: Self) -> bool:
        return self.__id == n.get_id()
    
    def __str__(self) -> str:
        return f"id : {self.__id}, coords = ({self.__x}, {self.__y})"



class Edge:
    def __init__(
        self,
        start: Node,
        end: Node
    ):
        assert start != end, f"Boucle sur le noeud {start} !"
        self.__start: Node = start
        self.__end: Node = end

    def get_start(self) -> Node:
        return self.__start
    
    def get_end(self) -> Node:
        return self.__end
        
    def __eq__(self, edge: Self) -> bool:
        return self.__start == edge.get_start() and self.__end == edge.get_end()
    
    def __str__(self) -> str:
        return f"({self.get_start().get_id()}, {self.get_end().get_id()})"
    
    
        
class CityGraph:
    def __init__(self):
        self.__N_v: int = 0
        self.__N_e: int = 0
        self.__edges: list[Edge] = []
        self.__nodes: list[Node] = []
        
    def get_N_v(self) -> int:
        return self.__N_v
    
    def get_N_e(self) -> int:
        return self.__N_e
        
    def get_edges(self) -> list[Edge]:
        return self.__edges
    
    def get_nodes(self) -> list[Node]:
        return self.__nodes
    
    def find_node_from_id(self, id: int) -> Node:
        l_nodes = self.__nodes
        for n in l_nodes:
            if n.get_id() == id:
                return Node
        
    def add_node(self, n: Node) -> None:
        self.__nodes.append(n)
        self.__N_v += 1
        
    def remove_node(self, n: Node) -> None:
        self.__nodes.remove(n)
        edges_from_n = self.find_edges_from_node(n)
        edges_to_n = self.find_edges_to_node(n)
        for e in edges_from_n:
            self.remove_edge(e)
        for e in edges_to_n:
            self.remove_edge(e)
        del(n)
        self.__N_v -= 1
        
    def random_nodes(self, k_nodes) -> list[Node]:
        return random.choices(self.__nodes, k=k_nodes)
    
    
    
    def find_edge(self, start: Node, end: Node) -> Edge | None:
        for e in self.__edges:
            if e.get_start() == start and e.get_end() == end:
                return e
        return None
        
    def find_edges_from_node(self, start: Node) -> list[Edge]:
        L: list[Edge] = []
        edges = self.__edges
        for e in edges:
            if e.get_start() == start:
                L.append(e)
        return L
    
    def find_edges_to_node(self, end: Node) -> list[Edge]:
        L: list[Edge] = []
        edges = self.__edges
        for e in edges:
            if e.get_end() == end:
                L.append(e)
        return L
    
    
    
    def add_edge(self, start: Node, end: Node) -> None:
        self.__edges.append(Edge(start, end))
        self.__N_e += 1
        
    def remove_edge(self, e: Edge) -> None:
        self.__edges.remove(e)
        del(e)
        self.__N_e -= 1
    
    
    
    
    # Obtention du voisinnage d'un noeud
    def get_neighbours(self, n:Node) -> list[Node]:
        l_edges = self.find_edges_from_node(n)
        l_neighbours = []
        
        for e in l_edges:
            l_neighbours.append(e.get_end())
    
        return l_neighbours
    
    
    # Réinitialisation des couleurs disponible avant le trajet d'une fourmi
    def reset_available_colors(self) -> None:
        for n in self.__nodes:
            n.reset_available_colors(self.__N_v)
    
    
    def evaporate(self, evap_rate: float) -> None:
        for n in self.__nodes:
            n.evaporation_pheromone(evap_rate)
            
            
            
        
    def str_edges(self) -> str:
        txt_edges = "Edges : "
        for e in self.__edges:
            txt_edges += str(e)
            txt_edges += " | "
        return txt_edges
    
    def str_nodes(self):
        txt_nodes: str = "Nodes : "
        for n in self.__nodes:
            txt_nodes += str(n) 
            txt_nodes += " | "
        return txt_nodes
        
    def __str__(self) -> str:
        return "\n" + self.str_nodes() + "\n" + self.str_edges() + "\n"
