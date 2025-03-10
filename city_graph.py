class Edge:
    def __init__(self, start, end, L): 
        self.__pheromone = 0
        self.__distance = L 
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
        
class City_graph:
    def __init__(self, N_v, edges):
        self.__N_v = N_v
        self.__N_e = len(edges)
        self.__edges = edges
        
    def get_N_v(self):
        return self.__N_v
        
    def get_edges(self):
        return self.__edges
        
    def find_edge(self, start, end) -> Edge:
        for e in self.__edges:
            if e.get_start() == start and e.get_end() == end:
                return e
        
    def add_edge(self, L, start, end):
        self.__edges.append(Edge(L, start, end))
        self.__N_e += 1
        
    def remove_edge(self, start, end):
        e = self.find_edge(start, end)
        self.__edges.remove(e)
        del(e)
        self.__N_e -= 1
        
    