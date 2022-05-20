from config import CONFIG
from src import Simulation
from src import Rect
from src import ImageManagerSingleton
from src.reports import ReportSingleton

if __name__ == '__main__':
    sim = Simulation(CONFIG)
    sim.set_selection_criteria(Rect(0,0, CONFIG['board-size']/3,CONFIG['board-size']))
    sim.populate_board()
    for i in range(CONFIG['max-generations']):
        print('New Gen')
        sim.run_simulation_generation()
    ImageManagerSingleton().display_genome(sim.get_population().get_beings()[0])
    ReportSingleton().plot_death_rate()
    ReportSingleton().plot_diversity()