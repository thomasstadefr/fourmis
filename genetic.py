from ant import Ant
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
        self.__population: list[Ant] = [Ant(city_graph, 0, metric) for _ in range(N_pop)] # TODO
        self.rank_pop()

    def mutation(self, ant: Ant) -> Ant: 
        # TODO: remplacement des individus les mois performants par des individus générés uniformément
        # utiliser uniform(a, b)
        pass

    def crossover(self, ant: Ant) -> Ant:
        # TODO: petite mutation des individus relativement performants autour du meilleur individu 
        pass

    def reproduction(self, ant: Ant) -> Ant:
        # TODO: moyenne pondérée entre un individu et le meilleur individu
        pass

    def rank_pop(self) -> None:
        merge_sort_ants(self.__population)
        
    def step(self) -> None:
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
