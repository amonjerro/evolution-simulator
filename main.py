from config import CONFIG
from src import Simulation

if __name__ == '__main__':
    sim = Simulation(CONFIG)
    sim.populate_board()
    sim.run_simulation_generation()

    pop = sim.get_population()
    genome = pop.get_being_by_index(0).get_genome()
    genome.print_genome()