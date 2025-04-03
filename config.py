from ant import Ant

genetic_params: dict[str, float] = {
    "mut_rate" : 0.2, 
    "cross_rate" : 0.2, 
    "repr_rate" : 0.3
}

colony_params: dict[str, float] = {
    "Q" : 1.0, 
    "evap_rate" : 0.2, 
    "init_pheromone": 1.0
}

general_params: dict[str, int] = {
    "N_pop" : 100, 
    "num_genetic_steps" : 10, 
    "num_colony_steps": 10
}

def metric(ant: Ant) -> float:
    return ant.get_L_path()