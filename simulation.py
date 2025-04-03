import tkinter as tk
from tkinter import font
from genetic import Genetic
from colony import Colony
from ant import random_population
from city_graph import CityGraph, Node
from config import genetic_params, general_params, colony_params, metric

class Visualisation:
    def __init__(self, city_graph: CityGraph, genetic_params, colony_params, general_params):
        self.__root = tk.Tk()
        self.__root.geometry("700x600")
        self.__root.title("TSP simulation by ant colony and genetic algorithm")
        
        self.__canvas_frame = tk.Frame(self.__root)
        self.__canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__canvas = tk.Canvas(self.__canvas_frame, width=700, height=400)
        self.__canvas.pack(fill=tk.BOTH, expand=True)
        
        self.__drawn_nodes: dict[
            tuple[int, int],
            int
        ] = {}
        self.__drawn_edges: dict[
            tuple[int, int, int, int],
            int
        ] = {}
        self.__written_ids: dict[
            tuple[int, int],
            any
        ] = {}
        self.__mode = "create"
        self.__canvas.bind("<Button-1>", self.select_node)
        self.__node_curently_selected = None
        
        self.__city_graph: CityGraph = city_graph
        self.__begin: bool = False
        
        self.__bottom_frame = tk.Frame(self.__root, bg="pink")
        self.__bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.__settings_frame = tk.Frame(self.__bottom_frame, bg="brown")
        self.__settings_frame.pack(side=tk.LEFT, fill=tk.X)
        
        self.__begin_button = tk.Button(self.__settings_frame, text = 'Begin', command = self.begin)
        self.__begin_button.pack()
        
        self.__create_mode_button = tk.Button(self.__settings_frame, text = 'Create mode', command = self.set_mode_create, bg="green")
        self.__create_mode_button.pack()
        self.__delete_edge_mode_button = tk.Button(self.__settings_frame, text = 'Delete edge mode', command = self.set_mode_delete_edge, bg="grey")
        self.__delete_edge_mode_button.pack()
        self.__delete_node_mode_button = tk.Button(self.__settings_frame, text = 'Delete node mode', command = self.set_mode_delete_node, bg="grey")
        self.__delete_node_mode_button.pack()
        
        self.__step_label = tk.Label(self.__settings_frame, text="Etape : -")
        self.__step_label.pack()
        
        self.__genetic_params_frame = tk.Frame(self.__bottom_frame, bg="brown", highlightbackground="blue", highlightcolor="blue", highlightthickness=3)
        self.__genetic_params_frame.pack(side=tk.RIGHT, fill=tk.X)
        
        self.__genetic_params: dict[str, float] = genetic_params
        
        self.__rand_rate_label = tk.Label(self.__genetic_params_frame, text="Randomization rate :")
        self.__rand_rate_label.pack()
        self.__rand_rate_entry = tk.Entry(self.__genetic_params_frame, justify="center")
        self.__rand_rate_entry.pack()
        self.__rand_rate_entry.insert(0, self.__genetic_params["rand_rate"])
        
        self.__mutation_rate_label = tk.Label(self.__genetic_params_frame, text="Mutation rate :")
        self.__mutation_rate_label.pack()
        self.__mutation_rate_entry = tk.Entry(self.__genetic_params_frame, justify="center")
        self.__mutation_rate_entry.pack()
        self.__mutation_rate_entry.insert(0, self.__genetic_params["mutation_rate"])
        
        self.__crossover_rate_label = tk.Label(self.__genetic_params_frame, text="Crossover rate :")
        self.__crossover_rate_label.pack()
        self.__crossover_rate_entry = tk.Entry(self.__genetic_params_frame, justify="center")
        self.__crossover_rate_entry.pack()
        self.__crossover_rate_entry.insert(0, self.__genetic_params["crossover_rate"])
        
        self.__colony_params_frame = tk.Frame(self.__bottom_frame, bg="brown", highlightbackground="blue", highlightcolor="blue", highlightthickness=3)
        self.__colony_params_frame.pack(side=tk.RIGHT, fill=tk.X)
        
        self.__colony_params: dict[str, float] = colony_params
        
        self.__Q_label = tk.Label(self.__colony_params_frame, text="Q :")
        self.__Q_label.pack()
        self.__Q_entry = tk.Entry(self.__colony_params_frame, justify="center")
        self.__Q_entry.pack()
        self.__Q_entry.insert(0, self.__colony_params["Q"])
        
        self.__evap_rate_label = tk.Label(self.__colony_params_frame, text="Evaporation rate :")
        self.__evap_rate_label.pack()
        self.__evap_rate_entry = tk.Entry(self.__colony_params_frame, justify="center")
        self.__evap_rate_entry.pack()
        self.__evap_rate_entry.insert(0, self.__colony_params["evap_rate"])

        self.__init_pheromone_label = tk.Label(self.__colony_params_frame, text="Initial pheromone :")
        self.__init_pheromone_label.pack()
        self.__init_pheromone_entry = tk.Entry(self.__colony_params_frame, justify="center")
        self.__init_pheromone_entry.pack()
        self.__init_pheromone_entry.insert(0, self.__colony_params["init_pheromone"])
        
        self.__general_params_frame = tk.Frame(self.__bottom_frame, bg="brown", highlightbackground="blue", highlightcolor="blue", highlightthickness=3)
        self.__general_params_frame.pack(side=tk.RIGHT, fill=tk.X)
        
        self.__general_params: dict[str, int] = general_params
        
        self.__N_pop_label = tk.Label(self.__general_params_frame, text="Population size :")
        self.__N_pop_label.pack()
        self.__N_pop_entry = tk.Entry(self.__general_params_frame, justify="center")
        self.__N_pop_entry.pack()
        self.__N_pop_entry.insert(0, self.__general_params["N_pop"])
        
        self.__num_genetic_steps_label = tk.Label(self.__general_params_frame, text="Number of genetic steps :")
        self.__num_genetic_steps_label.pack()
        self.__num_genetic_steps_entry = tk.Entry(self.__general_params_frame, justify="center")
        self.__num_genetic_steps_entry.pack()
        self.__num_genetic_steps_entry.insert(0, self.__general_params["num_genetic_steps"])

        self.__num_colony_steps_label = tk.Label(self.__general_params_frame, text="Number of colony steps each generation :")
        self.__num_colony_steps_label.pack()
        self.__num_colony_steps_entry = tk.Entry(self.__general_params_frame, justify="center")
        self.__num_colony_steps_entry.pack()
        self.__num_colony_steps_entry.insert(0, self.__general_params["num_colony_steps"])
        
        self.__root.mainloop()
        
    def raise_error_value(self, error_msg: str) -> None:
        error_window = tk.Tk()
        error_window.geometry("600x100")
        error_window.title("Value error")
        error_label = tk.Label(error_window, text="Value error ! Values must respect :", font=font.Font(size=4))
        error_label.pack(side=tk.TOP, expand=True)
        msg_label = tk.Label(error_window, text=error_msg, fg="red", font=font.Font(size=6))
        msg_label.pack(side=tk.BOTTOM, expand=True)
        error_window.mainloop()
        
    def check_entries(self) -> bool:
        try:
            rand_rate = float(self.__rand_rate_entry.get())
            mutation_rate = float(self.__mutation_rate_entry.get())
            crossover_rate = float(self.__crossover_rate_entry.get())
            if rand_rate + mutation_rate + crossover_rate > 1:
                self.raise_error_value("mutation_rate + reproduction_rate + crossover_rate <= 1")
                return False
            if rand_rate < 0 or crossover_rate < 0 or mutation_rate < 0:
                self.raise_error_value("Values must be positives")
                return False
            
            Q = float(self.__Q_entry.get())
            evap_rate = float(self.__evap_rate_entry.get())
            init_pheromone = float(self.__init_pheromone_entry.get())
            if Q < 0:
                self.raise_error_value("Value of Q must be positive")
                return False
            if evap_rate <= 0 or evap_rate >= 1:
                self.raise_error_value("0 < evaporation_rate < 1")
                return False
            if init_pheromone < 0:
                self.raise_error_value("Value of tau_0 (initial pheromone) must be positive")
                return False
            
            N_pop = int(self.__N_pop_entry.get())
            num_genetic_steps = int(self.__num_genetic_steps_entry.get())
            num_colony_steps = int(self.__num_colony_steps_entry.get())
            if N_pop < 0 or num_genetic_steps < 0 or num_colony_steps < 0:
                self.raise_error_value("Values must be positives")
                return False
            
            return True
        except Exception:
            self.raise_error_value("Values must be int or float")
            return False
        
    def begin(self) -> None:
        if self.check_entries():
            self.__begin = True
            
            self.__create_mode_button.config(bg="grey")
            self.__create_mode_button.config(state = tk.DISABLED)
            self.__delete_node_mode_button.config(bg="grey")
            self.__delete_node_mode_button.config(state = tk.DISABLED)
            self.__delete_edge_mode_button.config(bg="grey")
            self.__delete_edge_mode_button.config(state = tk.DISABLED)
            self.__begin_button.config(bg="green")
            self.__begin_button.config(text="Started")
            self.__begin_button.config(state=tk.DISABLED)
            
            genetic_params = self.__genetic_params
            genetic_params["rand_rate"] = float(self.__rand_rate_entry.get())
            self.__rand_rate_entry.delete(0, tk.END)
            self.__rand_rate_entry.insert(0, genetic_params["rand_rate"])
            self.__rand_rate_entry.config(state="readonly")
            genetic_params["mutation_rate"] = float(self.__mutation_rate_entry.get())
            self.__mutation_rate_entry.delete(0, tk.END)
            self.__mutation_rate_entry.insert(0, genetic_params["mutation_rate"])
            self.__mutation_rate_entry.config(state="readonly")
            genetic_params["crossover_rate"] = float(self.__crossover_rate_entry.get())
            self.__crossover_rate_entry.delete(0, tk.END)
            self.__crossover_rate_entry.insert(0, genetic_params["crossover_rate"])
            self.__crossover_rate_entry.config(state="readonly")
            
            colony_params = self.__colony_params
            colony_params["Q"] = float(self.__Q_entry.get())
            self.__Q_entry.delete(0, tk.END)
            self.__Q_entry.insert(0, colony_params["Q"])
            self.__Q_entry.config(state="readonly")
            colony_params["evap_rate"] = float(self.__evap_rate_entry.get())
            self.__evap_rate_entry.delete(0, tk.END)
            self.__evap_rate_entry.insert(0, colony_params["evap_rate"])
            self.__evap_rate_entry.config(state="readonly")
            colony_params["init_pheromone"] = float(self.__init_pheromone_entry.get())
            self.__init_pheromone_entry.delete(0, tk.END)
            self.__init_pheromone_entry.insert(0, colony_params["init_pheromone"])
            self.__init_pheromone_entry.config(state="readonly")
            
            general_params = self.__general_params
            general_params["N_pop"] = int(self.__N_pop_entry.get())
            self.__N_pop_entry.delete(0, tk.END)
            self.__N_pop_entry.insert(0, general_params["N_pop"])
            self.__N_pop_entry.config(state="readonly")
            general_params["num_genetic_steps"] = int(self.__num_genetic_steps_entry.get())
            general_params["num_colony_steps"] = int(self.__num_colony_steps_entry.get())
            self.__num_genetic_steps_entry.delete(0, tk.END)
            self.__num_genetic_steps_entry.insert(0, general_params["num_genetic_steps"])
            self.__num_genetic_steps_entry.config(state="readonly")
            self.__num_colony_steps_entry.delete(0, tk.END)
            self.__num_colony_steps_entry.insert(0, general_params["num_colony_steps"])
            self.__num_colony_steps_entry.config(state="readonly")
        
    def get_begin(self) -> bool:
        return self.__begin
    
    def get_genetic_params(self) -> dict[str, float]:
        return self.__genetic_params
    
    def get_colony_params(self) -> dict[str, float]:
        return self.__colony_params
    
    def get_general_params(self) -> dict[str, int]:
        return self.__general_params
    
    def update_step(self, i: int) -> None:
        self.__step_label.config(text=f"Etape : {i}")
        
    def set_mode_create(self) -> None:
        self.__mode = "create"
        self.__create_mode_button.config(bg="green")
        self.__delete_edge_mode_button.config(bg="grey")
        self.__delete_node_mode_button.config(bg="grey")
        n_cur = self.__node_curently_selected
        if n_cur:
            self.change_color_node(n_cur, "blue")
        self.__node_curently_selected = None
        
    def set_mode_delete_node(self) -> None:
        self.__mode = "delete_node"
        self.__create_mode_button.config(bg="grey")
        self.__delete_edge_mode_button.config(bg="grey")
        self.__delete_node_mode_button.config(bg="green")
        n_cur = self.__node_curently_selected
        if n_cur:
            self.change_color_node(n_cur, "blue")
        self.__node_curently_selected = None
        
    def set_mode_delete_edge(self) -> None:
        self.__mode = "delete_edge"
        self.__create_mode_button.config(bg="grey")
        self.__delete_edge_mode_button.config(bg="green")
        self.__delete_node_mode_button.config(bg="grey")
        n_cur = self.__node_curently_selected
        if n_cur:
            self.change_color_node(n_cur, "blue")
        self.__node_curently_selected = None
        
    def draw_node(
        self,
        x: int,
        y: int,
        r: int,
        id: int
    ) -> None:
        self.__drawn_nodes[(x, y)] = self.__canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill="blue"
        )
        self.__written_ids[(x, y)] = self.__canvas.create_text(
            x,
            y,
            text=id,
            fill="white"
        )
        
    def create_node(
        self,
        x: int,
        y: int,
        r: int
    ) -> None:
        n = Node(x, y)
        self.__city_graph.add_node(n)
        self.draw_node(x, y, r, n.get_id())
        
    def delete_node(self, n_new: Node) -> None:
        g = self.__city_graph
        edges_from_n = g.find_edges_from_node(n_new)
        edges_to_n = g.find_edges_to_node(n_new)
        dr_e = self.__drawn_edges
        for e in edges_from_n:
            n_end = e.get_end()
            shape = dr_e[(
                n_new.get_x(),
                n_new.get_y(),
                n_end.get_x(),
                n_end.get_y()
            )]
            self.__canvas.delete(shape)
        for e in edges_to_n:
            n_start = e.get_start()
            shape = dr_e[(
                n_start.get_x(),
                n_start.get_y(),
                n_new.get_x(),
                n_new.get_y()
            )]
            self.__canvas.delete(shape)
        g.remove_node(n_new)
        dr_n = self.__drawn_nodes
        shape = dr_n[(
            n_new.get_x(),
            n_new.get_y()
        )]
        self.__canvas.delete(shape)
        wr_ids = self.__written_ids
        txt = wr_ids[(
            n_new.get_x(),
            n_new.get_y()
        )]
        self.__canvas.delete(txt)
        
    def change_color_node(self, n: Node, color: str) -> None:
        x = n.get_x()
        y = n.get_y()
        shape = self.__drawn_nodes[(x, y)]
        self.__canvas.itemconfig(shape, fill=color)
        
    def draw_edge(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        r: int
    ) -> None:
        v = (x2 - x1, y2 - y1)
        v_size: float = (v[0] ** 2 + v[1] ** 2) ** .5
        x1_tild = x1 + v[0] * r / v_size
        y1_tild = y1 + v[1] * r / v_size
        x2_tild = x2 - v[0] * r / v_size
        y2_tild = y2 - v[1] * r / v_size
        self.__drawn_edges[(x1, y1, x2, y2)] = self.__canvas.create_line(
            x1_tild, y1_tild, x2_tild, y2_tild, arrow=tk.LAST, fill="orange"
        )
    
    def create_edge(
        self,
        n_cur: Node,
        n_new: Node,
        r: int
    ) -> None:
        g = self.__city_graph
        if g.find_edge(n_cur, n_new) is None:
            g.add_edge(n_cur, n_new)
            self.draw_edge(
                n_cur.get_x(),
                n_cur.get_y(),
                n_new.get_x(),
                n_new.get_y(),
                r
            )
        
    def delete_edge(
        self,
        n_cur: Node,
        n_new: Node
    ) -> None:
        g = self.__city_graph
        e = g.find_edge(n_cur, n_new)
        if e:
            g.remove_edge(e)
            dr_e = self.__drawn_edges
            shape = dr_e[(n_cur.get_x(), n_cur.get_y(), n_new.get_x(), n_new.get_y())]
            self.__canvas.delete(shape)
            
    def select_node(self, event: tk.Event) -> None:
        if not self.__begin:
            x = event.x
            y = event.y
            r = 25
            
            n_new = self.new_node_selected(x, y, r)   # Récupération de l'éventuel noeud sélectionné par le clic de la souris
            n_cur = self.__node_curently_selected   # Récupération de l'éventuel noeud précédemment sélectionné   
            mode = self.__mode
             
            if n_new:   
                # Si l'emplacement cliqué correspond à un noeud existant : on le sélectionne
                if n_cur:
                    # Cas où un noeud était précédemment sélectionné
                    if n_new == n_cur:
                        # Si ce noeud est celui sur lequel on a cliqué : on le dé-selectionne
                        self.__node_curently_selected = None
                        self.change_color_node(n_cur, "blue")
                    else:
                        # Sinon on crée/supprime une arrête entre ces deux noeuds (de l'ancien vers le nouveau)
                        if mode == "create":
                            self.create_edge(n_cur, n_new, r)
                        elif mode == "delete_edge":
                            self.delete_edge(n_cur, n_new)
                        self.__node_curently_selected = None
                        self.change_color_node(n_cur, "blue")  
                else:
                    # Si aucun noeud n'était précédemment sélectionné : on marque comme précédemment séléctionné le noeud cliqué / on le supprime si on est en mode 'delete node'
                    if mode == 'delete_node':
                        self.delete_node(n_new)
                    else:
                        self.__node_curently_selected = n_new
                        self.change_color_node(n_new, "red")
                    
            elif not self.new_node_selected(x, y, 2 * r):
                # Si on a cliqué sur un emplacement vide du dessin : on y crée (en mode création) un nouveau noeud s'il ne touche aucun autre noeud
                if self.__mode == "create":
                    self.create_node(x, y, r)
                self.__node_curently_selected = None
                if n_cur:
                    # Si un autre noeud était pré-séléctionné, on le dé-selectionne
                    self.change_color_node(n_cur, "blue")
  
    def new_node_selected(
        self,
        x: int,
        y: int,
        r: int
    ) -> Node | None:
        nodes = self.__city_graph.get_nodes()
        for n in nodes:
            xi = n.get_x()
            yi = n.get_y()
            if (xi - x) ** 2 + (yi - y) ** 2 < r ** 2:
                return n
        return None 

class Simulation(Genetic, Colony, Visualisation):
    def __init__(self, genetic_params, colony_params, general_params, metric): #: callable[Ant, float]
        self.__city_graph = CityGraph()
        Visualisation.__init__(self, self.__city_graph, genetic_params, colony_params, general_params)
        
        self.__steps: int = 0
        while True:
            if self.get_begin():
                break
            
        self.__genetic_params = self.get_genetic_params()
        self.__colony_params = self.get_colony_params()
        self.__general_params = self.get_general_params()
        
        self.__N_pop = self.__general_params["N_pop"]
        self.__N_genetic_steps = self.__general_params["num_genetic_steps"]
        self.__N_colony_steps_each_generation = self.__general_params["num_colony_steps"]
        self.__metric = metric
        self.__population = random_population(self.__city_graph, self.__N_pop, self.__metric)
            
        Genetic.__init__(
            self,
            self.__city_graph,
            self.__population,
            self.__general_params["N_pop"],
            self.__genetic_params["rand_rate"],
            self.__genetic_params["mutation_rate"],
            self.__genetic_params["crossover_rate"],
            metric
        )
        Colony.__init__(
            self,
            self.__city_graph,
            self.__population,
            self.__general_params["N_pop"],
            self.__colony_params["evap_rate"],
            self.__colony_params["Q"],
            self.__colony_params["init_pheromone"],
            metric
        )
            
        print(self)
        self.launch()
        print(f"Edges after the simulation : {self.__city_graph.str_edges()}\n")

    def launch(self) -> None:
        # A chaque étape génétique, on lance un certain nombre d'étapes de colonies pour laisser le temps aux individus de démontrer leur adpatation
        N_genetic_steps = self.__N_genetic_steps
        N_colony_steps_each_generation = self.__N_colony_steps_each_generation
        
        for i in range(N_genetic_steps):
            for j in range(N_colony_steps_each_generation):
                self.colony_step()
                # TODO: màj le graphe à chaque étape
                # épaissir les arêtes selon la qté de phéromones...
                print(f"Population après l'étape {j} de colonie pour la génération {i} : {self.str_population()}\n")
                
            self.genetic_step()
          
    def str_population(self) -> str:
        txt_population = "["
        for ant in self.__population:
            txt_population += "\n"
            txt_population += str(ant)
        txt_population += "]"
        return txt_population
      
    def __str__(self):
        txt_population = self.str_population()
        return f""" 
            {self.__city_graph}
            \nGeneral params : {self.__general_params} \nGenetic params : {self.__genetic_params} \nColony params : {self.__colony_params}
            \nPopulation : {txt_population}
            \n
            """


s = Simulation(genetic_params, colony_params, general_params, metric)