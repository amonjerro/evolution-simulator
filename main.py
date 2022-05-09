from config import CONFIG
from src import Simulation
from src import Rect
from src.reports import ReportSingleton

if __name__ == '__main__':
    sim = Simulation(CONFIG)
    sim.set_selection_criteria(Rect(0,0, CONFIG['board-size']/3,CONFIG['board-size']))
    sim.populate_board()
    for i in range(CONFIG['max-generations']):
        print('New Gen')
        sim.run_simulation_generation()
    ReportSingleton().plot_death_rate()
    ReportSingleton().plot_diversity()