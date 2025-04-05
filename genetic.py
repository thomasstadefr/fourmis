from ant import Ant, compare_ants, new_random_ant, new_ant_clonage_mutation, new_ant_crossover, elite_ant
from city_graph import CityGraph

def merge_sort_ants(pop: list[Ant]) -> None:
    def merge(i: int, m: int, j: int) -> None:
        t = i
        r = m
        s = i
        new_tab = []
        
        while s < j:
            if r == j or (t < m and compare_ants(pop[t], pop[r])):
                new_tab.append(pop[t])
                t += 1
            else:
                new_tab.append(pop[r])
                r += 1
            s += 1
            
        for k in range(i, j):
            pop[k] = new_tab[k-i]
        del(new_tab)
        
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
        rand_rate: float,
        mutation_rate: float,
        repr_rate: float,
        metric #: callable[Ant, float]
    ):
        self.__rand_rate: float = rand_rate
        self.__mutation_rate: float = mutation_rate
        self.__crossover_rate: float = repr_rate
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
        new_node = g.random_nodes(1)[0] # TODO: faut-il mettre les fourmis sur le même noeud ou en changer ???
        
        same_ant = elite_ant(g, ant, new_node, self.__metric)
        del(ant)
        return same_ant

    def randomization(self, ant: Ant) -> Ant: 
        # On supprime la fourmi de la population avant d'en recréer une nouvelle
        del(ant)
        
        g = self.__city_graph
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        return new_random_ant(g, new_node, self.__metric)

    def clonage_mutation(self, ant: Ant) -> Ant:
        # On supprime la fourmi de la population avant d'en recréer une nouvelle
        del(ant)
        
        # TODO: petite mutation des individus relativement performants autour du meilleur individu 
        g = self.__city_graph
        best_ant = self.get_best_ant()
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        return new_ant_clonage_mutation(g, best_ant, new_node, self.__metric)

    def crossover(self, ant: Ant) -> Ant:
        # On supprime la fourmi de la population avant d'en recréer une nouvelle
        del(ant)
        
        # TODO: moyenne pondérée entre un individu et le meilleur individu
        g = self.__city_graph
        best_ant = self.get_best_ant()
        new_node = g.random_nodes(1)[0] # faut-il mettre les fourmis sur le même noeud ou en changer ???
        return new_ant_crossover(g, best_ant, new_node, self.__metric)
        
    def genetic_step(self) -> None:
        pop = self.__population
        self.rank_pop()

        N_rand = int(self.__rand_rate * self.__N_pop)
        N_mutation = int(self.__mutation_rate * self.__N_pop)
        N_crossover = int(self.__crossover_rate * self.__N_pop)
        N_same = self.__N_pop - N_rand - N_mutation - N_crossover
        
        for i in range(0, N_same):
            pop[i] = self.keep_elite(pop[i])
            
        for i in range(N_same, N_same + N_mutation):
            pop[i] = self.clonage_mutation(pop[i])
            
        for i in range(N_same + N_mutation, N_same + N_mutation + N_crossover):
            pop[i] = self.crossover(pop[i])
            
        for i in range(N_same + N_mutation + N_crossover, N_same + N_mutation + N_crossover + N_rand):
            pop[i] = self.randomization(pop[i])
