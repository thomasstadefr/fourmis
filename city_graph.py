class Node:
    id = 0
    def __init__(self, x, y):
        self.__id = Node.id
        Node.id += 1
        self.__x = x
        self.__y = y
        
    def get_id(self):
        return self.__id 
        
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y 
    
    def __eq__(self, n):
        return self.__id == n.get_id()
    
    def __str__(self):
        return f"id : {self.__id}, coords = ({self.__x}, {self.__y})"



class Edge:
    def __init__(self, start : Node, end : Node): 
        self.__pheromone = 0
        self.__distance = ((start.get_x()-end.get_x())**2 + (start.get_y()-end.get_y())**2)**0.5
        self.__start = start
        self.__end = end

    def get_start(self):
        return self.__start
    
    def get_end(self):
        return self.__end

    def get_distance(self):
        return self.__distance
    
    def get_pheromone(self):
        return self.__pheromone
    
    def set_pheromone(self, pheromone):
        self.__pheromone = pheromone
        
    def __eq__(self, e):
        return self.__start == e.get_start() and self.__end == e.get_end()
    
    def __str__(self):
        return f"({self.get_start().get_id()}, {self.get_end().get_id()})"
    
    
        
class City_graph:
    def __init__(self):
        self.__N_v = 0
        self.__N_e = 0
        self.__edges = []
        self.__nodes = []
        
    def get_N_v(self):
        return self.__N_v
    
    def get_N_e(self):
        return self.__N_e
        
    def get_edges(self):
        return self.__edges
    
    def get_nodes(self):
        return self.__nodes
        
    def add_node(self, n : Node):
        self.__nodes.append(n)
        self.__N_v += 1
        
    def remove_node(self, n : Node):
        self.__nodes.remove(n)
        edges_from_n = self.find_edges_from_node(n)
        edges_to_n = self.find_edges_to_node(n)
        for e in edges_from_n:
            self.remove_edge(e)
        for e in edges_to_n:
            self.remove_edge(e)
        del(n)
        self.__N_v -= 1
    
    def find_edge(self, start : Node, end : Node) -> Edge:
        for e in self.__edges:
            if e.get_start() == start and e.get_end() == end:
                return e
        return None
        
    def find_edges_from_node(self, start : Node):
        L = []
        edges = self.__edges
        for e in edges:
            if e.get_start() == start:
                L.append(e)
        return L
    
    def find_edges_to_node(self, end : Node):
        L = []
        edges = self.__edges
        for e in edges:
            if e.get_end() == end:
                L.append(e)
        return L
    
    def add_edge(self, start : Node, end : Node):
        self.__edges.append(Edge(start, end))
        self.__N_e += 1
        
    def remove_edge(self, e : Edge):
        self.__edges.remove(e)
        del(e)
        self.__N_e -= 1
        
    def __str__(self):
        txt_nodes = "Nodes : "
        for n in self.__nodes:
            txt_nodes += str(n) 
            txt_nodes += " | "
        txt_edges = "Edges : "
        for e in self.__edges:
            txt_edges += str(e)
            txt_edges += " | "
        return "\n" + txt_nodes + "\n" + txt_edges + "\n"
        
    