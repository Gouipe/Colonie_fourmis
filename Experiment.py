import random

from Ant import Ant
from Environment import Environment, OBSTACLE
import matplotlib.pyplot as plt

alpha_range = (0, 10)
beta_range = (0, 10)
rand_range = (0, 0.1)


class Experiment(object):
    def __init__(self, number_of_iterations, env=None) -> None:
        super().__init__()
        self.number_of_ants = 200

        if env is None:
            # create example environment of 11x11
            self.env = Environment(11, 11)
            # add food source at 0,0 with value = 10 (smell will be set automatically)
            self.env.add_food_source(0, 0, 10)
            # add obstacle at 3,4
            self.env.add_obstacle(3, 4)
            # add another food source
            self.env.add_food_source(9, 9, 50)
            # ...

        # set ranges to create ants with random parameters based on these ranges
        self.ranges = [alpha_range, beta_range, rand_range, (1, self.env.energy_death_thresh)]
        ants = self.create_new_population()
        self.env.init_ants(ants)

        self.noi = number_of_iterations

    def execute(self):

        # lists to monitor evolution of ant parameters
        alphas = []
        betas = []
        rands = []
        fitnesses = [] # tableau des moyennes d'aptitude 

        for i in range(self.noi):
            # update lists
            alphas.append(sum([ant.alpha/alpha_range[1] for ant in self.env.get_ants()])/len(self.env.get_ants()))
            betas.append(sum([ant.beta/beta_range[1] for ant in self.env.get_ants()]) / len(self.env.get_ants()))
            rands.append(sum([ant.rand/rand_range[1] for ant in self.env.get_ants()]) / len(self.env.get_ants()))

            # run one simulation
            for _ in range(self.env.energy_death_thresh * 2):
                self.env.update()

            # monitor ants fitness
            avg_fitness = 0
            if len(self.env.get_ants()) != 0:
                avg_fitness = sum([ant.fitness for ant in self.env.get_ants()])/len(self.env.get_ants())
            fitnesses.append(avg_fitness)

            print(self.env)
            # create new generation and replace the old one
            new_gen = self.produce_next_generation(self.env.get_ants(), self.number_of_ants)
            self.env.init_ants(new_gen)
            self.env.reset_pheromone()

        """ uncomment this to show graphs of parameter evolution """
        f = plt.figure(1)
        plt.plot(alphas, label="alpha")
        plt.plot(betas, label="beta")
        plt.plot(rands, label="rand")
        
        plt.ylim(0, 1)
        leg = plt.legend(loc='lower right')
        # f.show()
        g = plt.figure(2)
        plt.plot(fitnesses)
        plt.show()

    @staticmethod
    def _get_random_value(ran):
        return ran[0] + random.random() * ran[1]

    """
    creates a random new population.
    """
    def create_new_population(self):
        ants = []
        x = int(self.env.lines / 2)
        y = int(self.env.columns / 2)
        for _ in range(self.number_of_ants):
            [a, b, r, e] = [self._get_random_value(ran) for ran in self.ranges]
            ants.append(Ant(x, y, a, b, r, e))
        return ants

    # TODO implement
    def select(self, ants):
        return random.choices(ants, k=2)

    # TODO implement
    def cross(self, ant1, ant2):
        return ant1

    # TODO implement
    def mutate(self, ant):
        return ant

    """
    Creates a new generation based on previous generation;
    implement select, cross, mutate for this to work properly.
    """
    def produce_next_generation(self, ants, number_of_ants):
        new_gen = []
        if len(ants) < 2:
            # print("got here")
            return self.create_new_population()
        for _ in range(number_of_ants):
            [ant1, ant2] = self.select(ants)
            new_ant = self.cross(ant1, ant2)
            new_ant = self.mutate(new_ant)
            new_gen.append(new_ant)

        return new_gen
