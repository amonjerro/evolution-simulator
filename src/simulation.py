import random
from src.imager import ImageManagerSingleton
from src.being import Being, PopulationSingleton
from src.board import Coordinate, BoardSingleton
from src.neuron import NeuronFactory

from src.selection_criteria import box_filter, circle_filter
from src.utils import Rect, Circle
from src.reproduction import sexual_reproduction

class Simulation:
    def __init__(self, config):
        #Config singletons and other basic classes
        self.board = BoardSingleton()
        self.board.config(config)
        
        self.imager = ImageManagerSingleton()
        self.imager.config(config)

        self.population = PopulationSingleton()
        self.population.config(config)

        self.neuronFactory = NeuronFactory(config)
        self.gene_length = config['gene-length']
        self.max_steps = config['max-steps']
        self.max_generations = config['max-generations']
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
        # Calculates a diversity metric for the population
        # Stores it every generation ran
        pass

    def populate_board(self, beings=None):
        dimensions = self.board.get_dimensions()
        for i in range(self.population.get_population_size()):
            populated = False
            while not populated:
                starting_coordinate = Coordinate(
                        random.randint(1,dimensions[0]-1), 
                        random.randint(1, dimensions[1]-1)
                        )
                if beings is not None:
                    being_a, being_b = random.sample(beings, 2)
                    new_being_genes = sexual_reproduction(being_a, being_b)
                    b = Being(starting_coordinate, self.gene_length, genes=new_being_genes)
                else:
                    b = Being(starting_coordinate, self.gene_length)
                b.set_neuron_blueprints(self.neuronFactory.make_neurons_for_being())
                populated = self.board.populate_space(b)
            self.population.add_being(b)


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
                    #Update the being's coordinates
                    old_coordinate = being.get_position()
                    being.update_position(tentative_new_coordinate)
                    #Populate the space
                    self.board.populate_space(being)
                    #Depopulate the old space
                    self.board.depopulate_space(old_coordinate)

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
        self.imager.draw_selection(self.criteria_shape)
        self.imager.make_gif_from_gen(self.current_generation)

        #Gen Report
        self.check_diversity()

        #Apply selection criteria
        survivors = self.criteria_function(self.criteria_shape)
        self.population.wipe()
        #Wipe the board
        self.board.wipe()

        #Create the new individuals
        self.populate_board(survivors)
        self.current_generation += 1