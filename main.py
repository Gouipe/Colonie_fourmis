from Experiment import Experiment
from Environment import Environment



# Main
if __name__ == '__main__':
    # Création d'un environnement 7*7
    env7_7 = Environment(7,7)
    env7_7.add_food_source(0,0,10)
    env7_7.add_obstacle(1,2)
    env7_7.add_obstacle(4,2)
    env7_7.add_obstacle(5,2)

    exp = Experiment(20)
    exp.execute()

