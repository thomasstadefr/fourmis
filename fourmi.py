class Fourmi:
    def __init__(self, pos_init, metric):
        self.__pos = pos_init
        self.__visited = [pos_init]
        self.__metric = metric
        self.__score = self.__metric(self) # todo

    def get_score(self):
        return self.__score

    def step(self):
        # todo
        self.__score = self.__metric(self)