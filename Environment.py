FREE = 0
OBSTACLE = -1
HOLE = -2


class Environment(object):
    def __init__(self, lines, columns, ants=None, energy_death_thresh=None) -> None:
        super().__init__()
        self.lines = lines
        self.columns = columns
        self.matrix = [[FREE for i in range(self.columns)] for j in range(self.lines)]  # cell state FREE/OBSTACLE
        self.values = [[0 for i in range(self.columns)] for j in range(self.lines)]  # food value in cell
        self.smell = [[0 for i in range(self.columns)] for j in range(self.lines)]  # smell of food in cell
        self.pheromone_f = [[0 for i in range(self.columns)] for j in range(self.lines)]  # pheromone p2 in cell
        self.pheromone_h = [[0 for i in range(self.columns)] for j in range(self.lines)]  # pheromone p1 in cell

        self.energy_death_thresh = energy_death_thresh
        if energy_death_thresh is None:
            self.energy_death_thresh = 2 * (columns + lines)  # default value for max energy

        if ants is None:
            ants = []
        self._ants = ants
        self.number_of_ants = len(ants)

    def init_ants(self, ants):
        self._ants = ants
        self.number_of_ants = len(ants)

    def reset_pheromone(self):
        self.pheromone_f = [[0 for i in range(self.columns)] for j in range(self.lines)]  # pheromone in node
        self.pheromone_h = [[0 for i in range(self.columns)] for j in range(self.lines)]  # pheromone in node

    def kill(self, ant):
        self._ants.remove(ant)

    def add_obstacle(self, x, y):
        self.matrix[x][y] = OBSTACLE

    def add_food_source(self, x, y, value):
        self.values[x][y] = value
        self.add_smell(x, y, value)

    def add_smell(self, x, y, value):
        if x >= self.lines or x < 0 or y >= self.columns or y < 0:
            return
        if value <= self.smell[x][y]:
            return
        self.smell[x][y] = value
        value = int(value/2)
        self.add_smell(x + 1, y, value)
        self.add_smell(x - 1, y, value)
        self.add_smell(x, y + 1, value)
        self.add_smell(x, y - 1, value)

    def evaporate(self):
        for i in range(self.lines):
            for j in range(self.columns):
                self.pheromone_f[i][j] *= 0.95
                self.pheromone_h[i][j] *= 0.95

    def update(self):
        for ant in self._ants:
            ant.move(self)
            # note: HOLE has been removed from project.
            if self.matrix[ant.x][ant.y] == HOLE or ant.energy <= 0:
                self.kill(ant)
        self.evaporate()

    def get_ants(self):
        return self._ants

    def num_ants(self, x, y):
        return len([ant for ant in self.get_ants() if ant.x == x and ant.y == y])

    """
    string of the environment's matrix to print state of cells
    """
    def __str__(self) -> str:
        s = "".join(["-"*19 for _ in range(self.columns)]) + "\n"
        for i in range(self.lines):
            for j in range(self.columns):
                s += "|" + "{:5.2f}".format(self.num_ants(i, j)) + "," + "{:5.2f}".format(self.pheromone_h[i][j]) +\
                     "," + "{:5.2f}".format(self.pheromone_f[i][j]) + "|"
            s += "\n" + "".join(["-"*19 for _ in range(self.columns)]) + "\n"

        return s


