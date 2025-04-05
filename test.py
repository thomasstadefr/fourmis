import random
from ant import Ant
from city_graph import Node, Edge, CityGraph
from colony import Colony

"""Init"""

city_graph = CityGraph()

for _ in range(20):
    x, y = random.randrange(100), random.randrange(100)
    print(x, y)
    city_graph.add_node(Node(x, y))

nodes = city_graph.get_nodes()
for _ in range(100):
    start, end = random.sample(nodes, 2)
    city_graph.add_edge(start, end)

def metric(ant: Ant) -> float:
    length = ant.get_L_path
    number_of_cities = len(ant.get_path_nodes())
    return length / (number_of_cities ** 1.5)

colony = Colony(
    city_graph=city_graph,
    N_pop=10,
    evap_rate=0.2,
    Q=1,
    metric=metric
)

"""Steps"""