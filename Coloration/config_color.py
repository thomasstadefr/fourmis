from ant_color import Ant

genetic_params: dict[str, float] = {
    "rand_rate" : 0.2, 
    "mutation_rate" : 0.2, 
    "crossover_rate" : 0.3
}

colony_params: dict[str, float] = {
    "Q" : 50.0, 
    "evap_rate" : 0.2, 
    "init_pheromone": 1.0
}

general_params: dict[str, int] = {
    "N_pop" : 100, 
    "num_genetic_steps" : 10, 
    "num_colony_steps": 10
}

def metric_color(ant: Ant) -> int:
    return ant.get_nb_colors()

canvas_colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "purple",
    "pink",
    "cyan",
    "magenta",
    "brown",
    "gray",
    "black",
    "white",
    "olive",
    "forestgreen",
    "navy",
    "skyblue",
    "turquoise",
    "coral",
    "gold"
]