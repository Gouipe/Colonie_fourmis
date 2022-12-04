import random

from Environment import Environment, OBSTACLE

EXPLORE = 1
RETURN = 2

class Ant(object):
    def __init__(self, x, y, alpha=1, beta=1, rand=0.2, energy=20, dx=0, dy=0) -> None:
        super().__init__()
        self.alpha = alpha  # exploit society information
        self.beta = beta  # exploit environment information
        self.rand = rand  # explore
        self.max_energy = energy
        self.energy = energy

        self.origin = (x, y)
        self.x = x
        self.y = y  # start at origin

        self.mode = EXPLORE
        self.carried_value = 0  # carried value is 0 initially
        self.fitness = 0  # fitness 0 initially, quantité de nourriture rapportée
        self.movement = [(x, y)]

    # TODO: Implement, now it moves randomly
    def choose_cell(self, cells):
        # Choix d'une cellule au hasard avec une probabilité self.rand
        cell_result = random.choice(cells)
        if(random.random() < self.rand):
            return cell_result

        # Mode exploration
        somme_cells = 0
        cells_probability = [] 
        if(self.mode == EXPLORE):
            for cell in cells:
                phero = cell[3]
                smell = cell[2]
                somme_cells += pow(phero, self.alpha) * pow(smell, self.beta)

            #Si aucune odeur ou pheromone dans les cellules voisines, on renvoie une cellule au hasard
            if somme_cells == 0:
                return cell_result
                
            for cell in cells:         
                phero = cell[3]
                smell = cell[2]
                #Calcul de la probabilité de la cellule courante
                current_cell_probability= (pow(phero, self.alpha) * pow(smell, self.beta))/somme_cells
                # current_cell_probability est parfois un complex, et cela pose probleme par la suite dans le random.choices
                if isinstance(current_cell_probability, complex):
                    return cell_result
                #La somme des elements de cells_probability vaudra 1 à la fin de la boucle
                cells_probability.append(current_cell_probability)

        #Mode retour
        else:
            for cell in cells:
                phero = cell[4]
                somme_cells += pow(phero, self.alpha)

            if somme_cells == 0:
                return cell_result

            for cell in cells:
                phero = cell[4]
                current_cell_probability = pow(phero, self.alpha)/somme_cells
                # current_cell_probability est parfois un complex, et cela pose probleme par la suite dans le random.choices
                if isinstance(current_cell_probability, complex):
                    return cell_result
                cells_probability.append(current_cell_probability)
        
        #On choisit une cellule selon les poids de probabilité calculés auparavant
        cell_result = random.choices(cells, weights=cells_probability, k=1)[0]
        return cell_result

    def move(self, env: Environment):
        cells = []

        # get neighboring cells
        for i in range(self.x - 1, self.x + 2):
            if i < 0 or i >= env.lines:
                continue
            for j in range(self.y - 1, self.y + 2):
                if j < 0 or j >= env.columns:
                    continue
                if env.matrix[i][j] != OBSTACLE and (self.x != i or self.y != j):
                    cells.append([i, j, env.smell[i][j], env.pheromone_f[i][j], env.pheromone_h[i][j]])

        # implement this
        cell = self.choose_cell(cells)

        # add pheromone based on energy consumed
        energy_consumed = self.max_energy - self.energy
        if self.mode == EXPLORE:
            env.pheromone_h[self.x][self.y] += 10/(1+energy_consumed)
        else:
            env.pheromone_f[self.x][self.y] += self.carried_value/(1+energy_consumed)

        # move ant
        self.x = cell[0]
        self.y = cell[1]
        self.movement.append((self.x, self.y))
        self.energy -= 1

        # case ant reached a new food source
        if self.carried_value < env.values[self.x][self.y]:
            self.carried_value = env.values[self.x][self.y]
            self.mode = RETURN
            self.energy = self.max_energy

        # case ant back to nest
        if self.x == self.origin[0] and self.y == self.origin[1]:  # back to origin, update fitness
            self.energy = self.max_energy  # reinit energy
            self.mode = EXPLORE
            if self.carried_value > 0:
                self.fitness += self.carried_value
                self.carried_value = 0
    
    def copy(self):
        return Ant(self.origin[0], self.origin[1], self.alpha, self.beta, self.rand)

    def __str__(self) -> str:
        s = str([self.alpha, self.beta, self.rand, self.max_energy])
        return s
