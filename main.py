from config import CONFIG
from src import Simulation
from src import Rect
from src import ImageManagerSingleton
from src.reports import ReportSingleton

if __name__ == '__main__':
    print('Initializing')
    sim = Simulation(CONFIG)
    sim.set_selection_criteria(Rect(0,0, CONFIG['board-size']/3,CONFIG['board-size']))
    sim.populate_board()

    print('Running the simulation')
    for i in range(CONFIG['max-generations']):
        print(f'Running generation {i}', end='\r')
        sim.run_simulation_generation()
    print()
    
    print('Preparing Reports')
    ImageManagerSingleton().display_genome(sim.get_population().get_beings()[0], 0)
    ImageManagerSingleton().display_genome(sim.get_population().get_beings()[10], 10)
    ImageManagerSingleton().display_genome(sim.get_population().get_beings()[20], 20)
    ImageManagerSingleton().display_genome(sim.get_population().get_beings()[30], 30)
    ReportSingleton().plot_death_rate()
    ReportSingleton().plot_diversity()