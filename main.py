from config import CONFIG
from src import Simulation
from src import Rect

if __name__ == '__main__':
    sim = Simulation(CONFIG)
    sim.set_selection_criteria(Rect(10,10, 90,70))
    sim.populate_board()
    for i in range(CONFIG['max-generations']):
        print(i)
        sim.run_simulation_generation()
    