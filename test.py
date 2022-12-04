import random
from Experiment import Experiment
from Ant import Ant

# Création d'un objet Experiment et d'un tableau d'ants
a1 = Ant(0,0)
a2 = Ant(0,0, 3, 4, 0.6, 40)
a3 = Ant(0,0)
a4 = Ant(0,0)
a5 = Ant(0,0)
a1.fitness = 10
a2.fitness = 12
a3.fitness = 20
a4.fitness = 100
a5.fitness = 101
ants = [a1, a2, a3, a4, a5]
exp = Experiment(3)

# Test select
# for i in range(10):
#     (ch1,ch2) = exp.select(ants)

# # Test cross
# ant = exp.cross(a1,a2)
# pass

# # Test mutate
# for i in range(200):
#     exp.mutate(a1)