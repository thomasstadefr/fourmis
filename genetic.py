from ant import Ant
from city_graph import City_graph
import random

def uniform(a, b):
    return a + (b-a)*random.random()

def exchange_ants(pop, i, j):
    tmp = pop[i]
    pop[i] = pop[j]
    pop[j] = tmp

def merge_sort_ants(pop):
    def merge(i, m, j):
        t = i
        r = m
        s = i
        while s<j:
            if r==j or (t<m and pop[t].get_score()<pop[r].get_score()):
                exchange_ants(pop, t, s)
                t += 1
            else:
                exchange_ants(pop, r, s)
                r += 1
            s += 1
        
    def aux(i, j):
        if j-i > 1:
            m = int((j-i)/2)
            aux(i, m)
            aux(m, j)
            merge(i, m, j)

    aux(0, len(pop))

class Genetic:
    def __init__(self, city_graph : City_graph, N_pop, mut_rate, cross_rate, repr_rate, metric):
        self.__mut_rate = mut_rate
        self.__cross_rate = cross_rate
        self.__repr_rate = repr_rate
        self.__metric = metric
        self.__N_pop = N_pop
        self.__population = [Ant(city_graph, 0, metric) for _ in range(N_pop)] # todo
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
        merge_sort_ants(self.__population)
        
    def step(self):
        pop = self.__population
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

        