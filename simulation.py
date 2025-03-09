from genetic import Genetic
from colony import Colony
from city_graph import City_graph

class Simulation(Genetique, Colonie):
    def __init__(self, city_graph, N_pop, metric, genetique_args, colonie_args):
        Genetique.__init__(self, N_pop, genetique_args[mut_rate], genetique_args[cross_rate], genetique_args[repre_rate], genetique_args[repr_rate], metric)
        Colonie.__init__(self, N_pop, metric)

    def step(self):
        # todo
        pass
