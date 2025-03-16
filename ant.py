from city_graph import City_graph

class Ant:
    def __init__(self, city_graph : City_graph, pos_init, metric):
        self.__city_graph = city_graph
        self.__pos = pos_init
        self.__path = [pos_init]
        self.__L_path = 0
        self.__metric = metric
        self.__score = self.__metric(self)

    def get_pos(self):
        return self.__pos
    
    def get_path(self):
        return self.__path
    
    def get_L_path(self):
        return self.__L_path

    def get_score(self):
        return self.__score
    
    def update_score(self):
        self.__score = self.__metric(self)

    def next_city(self):
        # todo : choose next city to visit
        pass
    
    def moove(self):
        start = self.__pos
        end = self.next_city()
        e = self.__city_graph.find_edge(start, end)
        
        self.__path.append(end)
        self.__L_path += e.get_distance()
        self.update_score()
        
    def trip(self):
        # Autant de pas à faire que nombre de villes : une étape corrspond à un trajet complet 
        N_steps = self.__city_graph.get_N_v()
        for _ in range(N_steps):
            self.moove()
        
