from typing import Self
import random

class Node:
    id: int = 0
    def __init__(
        self,
        x: int,
        y: int
    ):
        self.__x: int = x
        self.__y: int = y
        self.__id: int = Node.id
        Node.id += 1
        
    def get_id(self) -> int:
        return self.__id
        
    def get_x(self) -> int:
        return self.__x
    
    def get_y(self) -> int:
        return self.__y
    
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
        self.__pheromone: float = 0
        self.__distance: float = (
            (start.get_x() - end.get_x()) ** 2
            + (start.get_y() - end.get_y()) ** 2
        ) ** .5
        self.__start: Node = start
        self.__end: Node = end

    def get_start(self) -> Node:
        return self.__start
    
    def get_end(self) -> Node:
        return self.__end

    def get_distance(self) -> float:
        return self.__distance
    
    def get_pheromone(self) -> float:
        return self.__pheromone
    
    def set_pheromone(self, pheromone: float) -> None:
        self.__pheromone = pheromone
    
    def evaporate(self, evap_rate: float) -> None:
        self.__pheromone *= 1 - evap_rate
        
    def __eq__(self, edge: Self) -> bool:
        return self.__start == edge.get_start() and self.__end == edge.get_end()
    
    def __str__(self) -> str:
        return f"({self.get_start().get_id()}, {self.get_end().get_id()}), ph = {self.get_pheromone():.3f}"
    
    
        
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
        
    def random_nodes(self, k_nodes):
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
    
    def evaporate(self, evap_rate: float) -> None:
        for e in self.__edges:
            e.evaporate(evap_rate)
        
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
