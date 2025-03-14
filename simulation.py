from genetic import Genetic
from colony import Colony
from ant import Ant
from city_graph import City_graph, Node
import tkinter as tk

class Visualisation:
    def __init__(self, city_graph : City_graph):
        self.__root = tk.Tk()
        self.__root.geometry("500x500")
        self.__root.title("Simulation TSP par colonie de fourmis et algorithmes génétiques")
        
        self.__canvas_frame = tk.Frame(self.__root)
        self.__canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__canvas = tk.Canvas(self.__canvas_frame, width=500, height=300)
        self.__canvas.pack(fill=tk.BOTH, expand=True)
        
        self.__drawn_nodes = {}
        self.__drawn_edges = {}
        self.__canvas.bind("<Button-1>", self.select_node)
        self.__node_curently_selected = None
        
        self.__city_graph = city_graph
        self.__begin = False
        
        self.__settings_frame = tk.Frame(self.__root, bg="brown")
        self.__settings_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.__begin_button = tk.Button(self.__settings_frame, text = 'begin', command = self.begin)
        self.__begin_button.pack()
        
        self.__step_label = tk.Label(self.__settings_frame, text=f"Etape : -")
        self.__step_label.pack()
        
        self.__root.mainloop()
        
    def begin(self):
        self.__begin = True
        
    def get_begin(self):
        return self.__begin
    
    def update_step(self, i):
        self.__step_label.config(text=f"Etape : {i}")
        
    def draw_node(self, x, y, r):
        self.__drawn_nodes[(x, y)] = self.__canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue")
        
    def add_node(self, x, y, r):
        g = self.__city_graph
        g.add_node(Node(x, y))
        self.draw_node(x, y, r)
        
    def change_color_node(self, n : Node, color):
        x = n.get_x()
        y = n.get_y()
        shape = self.__drawn_nodes[(x, y)]
        self.__canvas.itemconfig(shape, fill=color)
        
    def draw_edge(self, x1, y1, x2, y2):
        self.__drawn_edges[(x1, y1, x2, y2)]  = self.__canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="orange")
    
    def add_edge(self, n1 : Node, n2 : Node):
        self.draw_edge(n1.get_x(), n1.get_y(), n2.get_x(), n2.get_y())
        g = self.__city_graph
        g.add_edge(n1, n2)
            
    def select_node(self, event):
        if not(self.__begin):
            x = event.x
            y = event.y
            r = 25
            n_new = self.new_node_selected(x, y, r)
            n_cur = self.__node_curently_selected
            if n_new:
                if n_cur:
                    if n_new == n_cur:
                        self.__node_curently_selected = None
                        self.change_color_node(n_cur, "blue")
                    else:
                        self.add_edge(n_cur, n_new)  
                        self.__node_curently_selected = None
                        self.change_color_node(n_cur, "blue")
                else:
                    self.__node_curently_selected = n_new
                    self.change_color_node(n_new, "red")
            elif not(self.new_node_selected(x, y, 2*r)):
                self.add_node(x, y, r)
                self.__node_curently_selected = None
                if n_cur:
                    self.change_color_node(n_cur, "blue")
  
    def new_node_selected(self, x, y, r):
        nodes = self.__city_graph.get_nodes()
        for n in nodes:
            xi = n.get_x()
            yi = n.get_y()
            if (xi-x)**2 + (yi-y)**2 < r**2:
                return n
        return None 

class Simulation(Genetic, Colony, Visualisation):
    def __init__(self, city_graph : City_graph, num_steps, N_pop, metric, genetic_args, colony_args):
        Genetic.__init__(self, city_graph, N_pop, genetic_args["mut_rate"], genetic_args["cross_rate"], genetic_args["repr_rate"], metric)
        Colony.__init__(self, city_graph, N_pop, colony_args["evap_rate"], colony_args["Q"], metric)
        Visualisation.__init__(self, city_graph)
        
        self.__steps = 0
        while not(self.get_begin()):
            pass
        self.launch(num_steps)
        print("nb sommets :", city_graph.get_N_v(), "\n nb aretes :", city_graph.get_N_e())

    def get_steps(self):
        return self.__steps

    def step(self):
        # todo : étape de la simualation (utilisation des méthodes de génétique et de colonies de fourmis)
        #self.update_step(self.__steps)
        self.__steps += 1
    
    def launch(self, num_steps):
        for i in range(num_steps):
            self.step()



genetic_args = {
    "mut_rate" : 0.1,
    "cross_rate" : 0.1,
    "repr_rate" : 0.1
}

colony_args = {
    "evap_rate" : 0.1,
    "Q" : 5
}

city_graph = City_graph() 

#todo 
def metric(ant : Ant):
    return ant.get_L_path()

s = Simulation(city_graph, 5, 10, metric, genetic_args, colony_args)