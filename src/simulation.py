import random
from collections import Counter
from src.imager import ImageManagerSingleton
from src.being import Being, PopulationSingleton
from src.board import Coordinate, BoardSingleton
from src.neuron import NeuronFactory
from src.Reports import ReportSingleton, performance_check

from src.selection_criteria import box_filter, circle_filter
from src.Utils import Rect, Circle
from src.reproduction import REPRODUCTION_FUNCTION_MAP

class Simulation:
    def __init__(self, config):
        #Config singletons and other basic classes
        self.board = BoardSingleton()
        self.board.config(config)
        
        self.imager = ImageManagerSingleton()
        self.imager.config(config)

        self.population = PopulationSingleton()
        self.population.config(config)

        self.reports = ReportSingleton()
        self.reports.config(config)

        self.neuronFactory = NeuronFactory()
        self.neuronFactory.config(config)
        
        self.gene_length = config['gene-length']
        self.max_steps = config['max-steps']
        self.max_generations = config['max-generations']
        self.reproduction_function = REPRODUCTION_FUNCTION_MAP[config['reproduction_function']]
        self.current_generation = 0

    def get_population(self):
        return self.population
    
    def set_selection_criteria(self, shape):
        self.criteria_shape = shape
        if isinstance(shape, Rect):
            self.criteria_function = box_filter
            self.imager.draw_selection = self.imager.draw_box_filter 
        elif isinstance(shape, Circle):
            self.criteria_function = circle_filter
            self.imager.draw_selection = self.imager.draw_circle_filter

    def check_diversity(self):
        beings = self.population.get_beings()
        counter = Counter()
        for being in beings:
            diversity_string = being.genome.genes_to_color()[1:5]
            counter[diversity_string] += 1

        return len(counter)

    @performance_check("pop_board", "Populate the board")
    def populate_board(self, beings=None):
        dimensions = self.board.get_dimensions()
        for i in range(self.population.get_population_size()):
            populated = False
            while not populated:
                starting_coordinate = Coordinate(
                        random.randint(1,dimensions[0]-1), 
                        random.randint(1, dimensions[1]-1)
                        )
                if beings is not None and len(beings)>0:
                    being_a, being_b = random.sample(beings, 2)
                    new_gene_strings = self.reproduction_function(being_a, being_b)
                    b = Being(starting_coordinates=starting_coordinate, 
                                gene_length=self.gene_length, 
                                genes=new_gene_strings)
                else:
                    b = Being(starting_coordinates=starting_coordinate, 
                                gene_length=self.gene_length)
               
                b.genome.set_quick_access_arrays()
                b.set_neuron_blueprints(self.neuronFactory.make_neurons_for_being())
                
                if self.population.being_is_valid(b):
                    populated = self.board.populate_space(b)
          
            self.population.add_being(b)

    @performance_check('sim_step', 'Running a simulation step')
    def run_simulation_generation(self):

        def _run_simulation_step(self):
            #For every being, sense & feedforward
            self.population.execute_senses()
            self.population.process_internal_signals()

            #For every being, stage the actions they want to perform
            beings = self.population.get_beings()
            for being in beings:
                tentative_new_coordinate = being.act()
                if self.board.is_valid_move(tentative_new_coordinate):
                    self.board.collision_map_add(tentative_new_coordinate, being)
                else:
                    self.board.collision_map_add(being.get_position(), being)

            for position in self.board.collision_map:
                self.board.resolve_occupation(position)

        ## Function start
        self.imager.render_simulation_step(
            self.current_generation, 
            0, 
            self.population.get_beings()
        )

        #Run all steps
        for step in range(self.max_steps):
            _run_simulation_step(self)
            self.imager.render_simulation_step(
                self.current_generation,
                step+1, 
                self.population.get_beings()
            )
            self.board.collision_map_wipe()
        self.imager.draw_selection(self.criteria_shape)
        self.imager.make_gif_from_gen(self.current_generation)

        #Apply selection criteria
        survivors = self.criteria_function(self.criteria_shape)
        self.population.wipe()
        #Wipe the board
        self.board.board_wipe()

        #Gen Report
        diversity = self.check_diversity()
        deaths = self.population.get_population_size() - len(survivors)
        self.reports.add_generation_data(deaths, diversity)

        #Create the new individuals
        self.populate_board(survivors)
        self.current_generation += 1
