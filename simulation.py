from genetic import Genetic
from colony import Colony
from ant import Ant
from city_graph import Edge, City_graph

class Simulation(Genetic, Colony):
    def __init__(self, city_graph:City_graph, N_pop, metric, genetic_args, colony_args):
        Genetic.__init__(self, N_pop, genetic_args["mut_rate"], genetic_args["cross_rate"], genetic_args["repr_rate"], metric)
        Colony.__init__(self, city_graph, N_pop, colony_args["evap_rate"], colony_args["Q"])
        self.__steps = 0

    def get_steps(self):
        return self.__steps

    def step(self):
        # todo : étape de la simualation (utilisation des méthodes de génétique et de colonies de fourmis)
        self.__steps += 1
    
    def launch(self, num_steps):
        for _ in range(num_steps):
            self.step()




genetic_args = {
    "mut_rate" : 0.1,
    "cross_rate" : 0.1,
    "repr_rate" : 0.1
}

colony_args = {
    "evap_rate" : 0.1,
    "Q" : 5
}

edges = [
    Edge(0, 1, 4),
    Edge(1, 2, 3),
    Edge(1, 3, 5),
    Edge(2, 0, 1),
    Edge(3, 2, 8)
]

city_graph = City_graph(4, edges) 

#todo def metric(ant:Ant):
    