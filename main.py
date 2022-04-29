from config import CONFIG
from src import Simulation

if __name__ == '__main__':
    sim = Simulation(CONFIG)
    sim.populate_board()
    sim.run_simulation_generation()