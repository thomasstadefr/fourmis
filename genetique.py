from fourmi import Fourmi
import random

def uniform(a, b):
    return a + (b-a)*random.random()

class Genetique:
    def __init__(self, N_pop, mut_rate, cross_rate, repr_rate, metric):
        self.__mut_rate = mut_rate
        self.__cross_rate = cross_rate
        self.__repr_rate = repr_rate
        self.__metric = metric
        self.__N_pop = N_pop
        self.__population = [Fourmi(0, metric) for _ in range(N_pop)] # todo
        self.rank_pop()

    def mutation(self, ant): 
        # remplacement des individus les mois performants par des individus générés uniformément
        pass

    def crossover(self, ant):
        # petite mutation des individus relativement performants autour du meilleur individu 
        pass

    def reproduction(self, ant):
        # moyenne pondérée entre un individu et le meilleur individu
        pass 

    def rank_pop(self):
        n = self.__N_pop
        pop = self.__population
        # todo
        
    def step(self):
        pop = self.__population

        for ant in pop:
            ant.step()
        self.rank_pop()

        N_mut = int(self.__mut_rate * self.__N_pop)
        N_cross = int(self.__cross_rate * self.__N_pop)
        N_repr = int(self.__repr_rate * self.__N_pop)
        N_same = self.__N_pop - N_mut - N_cross - N_repr
        for i in range(N_same, N_same + N_cross):
            pop[i] = self.crossover(pop[i])
        for i in range(N_same + N_cross, N_same + N_cross + N_repr):
            pop[i] = self.reproduction(pop[i])
        for i in range(N_cross, N_same + N_cross + N_repr, N_cross, N_same + N_cross + N_repr + N_mut):
            pop[i] = self.mutation(pop[i])


#test criture