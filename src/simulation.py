import random
from src.imager import ImageManager
from src.being import Being, Population
from src.board import Coordinate, Board
from src.neuron import NeuronFactory


class Simulation:
    def __init__(self, config):
        self.board = Board(config)
        self.imager = ImageManager(config)
        self.population = Population(config)
        self.neuronFactory = NeuronFactory(config)
        self.gene_length = config['gene-length']
        self.max_steps = config['max-steps']
        self.max_generations = config['max-generations']
        self.current_generation = 0

    def get_population(self):
        return self.population

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
                    b = Being(starting_coordinate,self.gene_length, genes=beings[i].genome.genes[:])
                else:
                    b = Being(starting_coordinate,self.gene_length)
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
        
        self.imager.gen_to_gif(self.current_generation)

        #Gen Report
        self.check_diversity()

        #Apply selection criteria

        #Create the new individuals

        #Wipe the board
        # self.board.wipe()
        # self.population.wipe()

        #Populate the board again
        # self.populate_board()
        self.current_generation += 1