class Ant:
    def __init__(self, pos_init, metric):
        self.__pos = pos_init
        self.__visited = [pos_init]
        self.__metric = metric
        self.__score = self.__metric(self)

    def get_score(self):
        return self.__score
    
    def update_score(self):
        self.__score = self.__metric(self)

    def next_city(self):
        # todo : choose next city to visit

    def step(self):
        # todo
        self.update_score()
        
