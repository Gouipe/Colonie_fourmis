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
        else:
            self.env = env
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
        energy = [] # tableau de moyenne d'energie max
        survived = [] # tableau de nombre de fourmis survivantes
        fitnesses = [] # tableau des moyennes d'aptitude 
        total_food = [] # tableau de nourriture totale ramenée

        for i in range(self.noi):
            # update lists
            alphas.append(sum([ant.alpha/alpha_range[1] for ant in self.env.get_ants()])/len(self.env.get_ants()))
            betas.append(sum([ant.beta/beta_range[1] for ant in self.env.get_ants()]) / len(self.env.get_ants()))
            rands.append(sum([ant.rand/rand_range[1] for ant in self.env.get_ants()]) / len(self.env.get_ants()))
            energy.append(sum([ant.max_energy/self.env.energy_death_thresh for ant in self.env.get_ants()])/ len(self.env.get_ants())) # moyenne energie au depart
            # run one simulation
            for _ in range(self.env.energy_death_thresh * 2):
                self.env.update()

            # monitor ants fitness
            avg_fitness = 0
            current_total_food = 0
            if len(self.env.get_ants()) != 0:
                for ant in self.env.get_ants():
                    current_total_food += ant.fitness
                avg_fitness = current_total_food/len(self.env.get_ants())
            fitnesses.append(avg_fitness)
            survived.append(len(self.env._ants))
            total_food.append(current_total_food)
            # print(self.env)

            # create new generation and replace the old one
            new_gen = self.produce_next_generation(self.env.get_ants(), self.number_of_ants)
            self.env.init_ants(new_gen)
            self.env.reset_pheromone()

        """ uncomment this to show graphs of parameter evolution """
        # Parametres
        f = plt.figure(1)
        plt.plot(alphas, label="alpha")
        plt.plot(betas, label="beta")
        plt.plot(rands, label="rand")
        plt.ylim(0, 1)
        leg = plt.legend(loc='lower right')
        # f.show()

        # Aptitude
        g = plt.figure(2)
        plt.plot(fitnesses, label="moy_aptitude")
        leg = plt.legend(loc='lower right')

        # # Autres
        # h= plt.figure(3)
        # # plt.plot(survived, label="survived")
        # plt.plot(total_food, label="nourriute totale ramenée")
        # # plt.plot(energy, label="energy at beginning")
        # leg = plt.legend(loc='lower right')

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
    def select(self, ants, weight=None):
        # return random.choices(ants, k=2)

        # Sélection par proportionnalité à l'aptitude
        # Sélection de 2 fourmis. La probabilité qu'une fourmi soit selectionnée est proportionnelle à son aptitude
        if weight != None and sum(weight) > 0: 
            return random.choices(ants, weight, k=2)
        else:
            return random.choices(ants, k=2)

        # Sélection par rang


    # TODO implement
    def cross(self, ant1, ant2):
        # return ant1
        x = int(self.env.lines / 2)
        y = int(self.env.columns / 2)
        # Nouvelle fourmi possédant alpha et rand de la première fourmi, et possédant beta et max_energy de la deuxième fourmi
        return Ant(x, y, ant1.alpha, ant2.beta, ant1.rand, ant2.max_energy)

    # TODO implement
    def mutate(self, ant):
        # return ant

        #Chaque paramètre a 0.5% de chances d'être modifié au hasard
        if random.random() < 0.005:
            ant.alpha = self._get_random_value(self.ranges[0]) 
        if random.random() < 0.005:
            ant.beta = self._get_random_value(self.ranges[1]) 
        if random.random() < 0.005:
            ant.rand = self._get_random_value(self.ranges[2])
        if random.random() < 0.005:
            ant.max_energy = self._get_random_value(self.ranges[3])
            ant.energy = ant.max_energy
        return ant

    """
    Creates a new generation based on previous generation;
    implement select, cross, mutate for this to work properly.
    """
    def produce_next_generation(self, ants, number_of_ants):
        # return self.create_new_population()
        new_gen = []
        if len(ants) < 2:
            # print("got here")
            return self.create_new_population()

        # Liste des poids/aptitudes à utiliser dans la sélection plus bas
        aptitudeWeight = list(map(lambda x : x.fitness, ants))   

        # ELITISME (on garde les meilleurs chromosomes avant de suivre la démarche classique de sélection)
        orderedAnts = sorted(ants, key=lambda x : x.fitness, reverse=True) # ants ordoné par aptitude
        nbElite = len(ants) if len(ants) < 10 else 10 # nb d'elite qu'on garde
        x = int(self.env.lines / 2) # coordonnées de départ 
        y = int(self.env.columns / 2)  
        for i in range(number_of_ants): 
            # Pour les nbElite premières fois, on prend les meilleures chromosomes sans les changer
            if i < nbElite :
                elite = orderedAnts[i]
                new_gen.append(Ant(x, y, elite.alpha, elite.beta, elite.rand, elite.max_energy))
            # Ensuite sélection classique
            else:    
                #Sélection par proportionnalité à l'aptitude
                [ant1, ant2] = self.select(ants, aptitudeWeight)
                #Sélection par rang
                #[ant1, ant2] = self.select(sorted(ants, key=lambda x : x.fitness))
                new_ant = self.cross(ant1, ant2)
                new_ant = self.mutate(new_ant)
                new_gen.append(new_ant)
       
        # # NON ELITISME
        # for _ in range(number_of_ants): 
        #     [ant1, ant2] = self.select(ants, aptitudeWeight)
        #     new_ant = self.cross(ant1, ant2)
        #     new_ant = self.mutate(new_ant)
        #     new_gen.append(new_ant)

        return new_gen
