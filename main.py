from config import CONFIG
from src import Simulation
from src import Board
from src import ImageManager

if __name__ == '__main__':
    sim = Simulation(Board(CONFIG), ImageManager(CONFIG), CONFIG)
    sim.populate_board()
    sim.run_simulation_generation()