from ant import Ant, new_ant_mutation, new_ant_crossover, new_ant_reproduction, elite_ant
from city_graph import CityGraph
from random import uniform

def exchange_ants(pop: list[Ant], i: int, j: int) -> None:
    tmp = pop[i]
    pop[i] = pop[j]
    pop[j] = tmp

def merge_sort_ants(pop: list[Ant]) -> None:
    def merge(i: int, m: int, j: int) -> None:
        t, s = i, i
        r = m
        while s < j:
            if r == j or (
                t < m and
                pop[t].get_score() < pop[r].get_score()
            ):
                exchange_ants(pop, t, s)
                t += 1
            else:
                exchange_ants(pop, r, s)
                r += 1
            s += 1
        
    def aux(i: int, j: int) -> None:
        if j - i > 1:
            m = i + int((j - i) / 2)
            aux(i, m)
            aux(m, j)
            merge(i, m, j)

    aux(0, len(pop))

class Genetic:
    def __init__(
        self,
        city_graph : CityGraph,
        population: list[Ant],
        N_pop: int,
        mut_rate: float,
        cross_rate: float,
        repr_rate: float,
        metric #: callable[Ant, float]
    ):
        self.__mut_rate: float = mut_rate
        self.__cross_rate: float = cross_rate
        self.__repr_rate: float = repr_rate
        self.__metric = metric #: callable[Ant, float]
        self.__N_pop: int = N_pop
        self.__city_graph = city_graph
        self.__population: list[Ant] = population
        self.rank_pop()
        
    def rank_pop(self) -> None:
        merge_sort_ants(self.__population)
        
    def get_best_ant(self):
        return self.__population[0]
    
    def keep_elite(self, ant :Ant):
        g = self.__city_graph
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        
        same_ant = elite_ant(g, ant, new_node, self.__metric)
        del(ant)
        return same_ant

    def mutation(self, ant: Ant) -> Ant: 
        # On supprime la fourmi de la population avant d'en recréer une nouvelle
        del(ant)
        
        g = self.__city_graph
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        return new_ant_mutation(g, new_node, self.__metric)

    def crossover(self, ant: Ant) -> Ant:
        # On supprime la fourmi de la population avant d'en recréer une nouvelle
        del(ant)
        
        # TODO: petite mutation des individus relativement performants autour du meilleur individu 
        g = self.__city_graph
        best_ant = self.get_best_ant()
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        return new_ant_crossover(g, best_ant, new_node, self.__metric)

    def reproduction(self, ant: Ant) -> Ant:
        # On supprime la fourmi de la population avant d'en recréer une nouvelle
        del(ant)
        
        # TODO: moyenne pondérée entre un individu et le meilleur individu
        g = self.__city_graph
        best_ant = self.get_best_ant()
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        return new_ant_reproduction(g, best_ant, new_node, self.__metric)
        
    def genetic_step(self) -> None:
        pop = self.__population
        self.rank_pop()

        N_mut = int(self.__mut_rate * self.__N_pop)
        N_cross = int(self.__cross_rate * self.__N_pop)
        N_repr = int(self.__repr_rate * self.__N_pop)
        N_same = self.__N_pop - N_mut - N_cross - N_repr
        
        for i in range(0, N_same):
            pop[i] = self.keep_elite(pop[i])
            
        for i in range(N_same, N_same + N_cross):
            pop[i] = self.crossover(pop[i])
            
        for i in range(N_same + N_cross, N_same + N_cross + N_repr):
            pop[i] = self.reproduction(pop[i])
            
        for i in range(N_same + N_cross + N_repr, N_same + N_cross + N_repr + N_mut):
            pop[i] = self.mutation(pop[i])
