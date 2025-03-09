from genetic import Genetic
from colony import Colony
from city_graph import City_graph

class Simulation(Genetic, Colony):
    def __init__(self, city_graph, N_pop, metric, genetic_args, colony_args):
        Genetic.__init__(self, N_pop, genetic_args[mut_rate], genetic_args[cross_rate], genetic_args[repre_rate], genetic_args[repr_rate], metric)
        Colony.__init__(self, city_graph, N_pop, colony_args[evaporation_rate], colony_args[Q], metric)
        self.__city = city_graph
        self.__steps = 0

    def step(self):
        # todo : étape de la simualation (utilisation des méthodes de génétique et de colonies de fourmis)
        pass
    
    def launch(self, num_steps):
        for _ in range(num_steps):
            self.step()
