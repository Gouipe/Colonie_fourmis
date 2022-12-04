from Experiment import Experiment
from Environment import Environment

# Création d'un environnement 7*7
env7_7 = Environment(7,7)
env7_7.add_food_source(0,0,10)
env7_7.add_obstacle(2,2)
env7_7.add_obstacle(2,3)
env7_7.add_obstacle(2,4)
env7_7.add_obstacle(3,4)
env7_7.add_obstacle(3,2)
env7_7.add_obstacle(4,3)
env7_7.add_obstacle(4,4)


# Main
if __name__ == '__main__':
    exp = Experiment(30)
    exp.execute()

