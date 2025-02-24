from genetique import Genetique
from colonie import Colonie

class Edge:
    def __init__(self, L, start, end):
        self.__pheromone = 0
        self.__distance = L
        self.__start = start
        self.__end = end

    def get_distance(self):
        return self.__distance
    
    def get_pheromone(self):
        return self.__pheromone
    
    def set_pheromone(self, phermone):
        self.__pheromone = phermone

class Simulation(Genetique, Colonie):
    def __init__(self):
        super.__init__(Genetique, self)
        super.__init__(Colonie, self)

    def step(self):
        pass