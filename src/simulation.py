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

    def get_population(self):
        return self.population

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

    def run_simulation_step(self):
        #For every being, perform their actions

        #Render the new board state
        pass

    def run_simulation_generation(self):
        #Run all steps
        for step in range(self.max_steps):
            self.run_simulation_step()
            beings = self.population.get_beings()
            self.imager.render_simulation_step(step, beings)

        #Apply selection criteria

        #Create the new individuals

        #Wipe the board
        self.board.wipe()
        self.population.wipe()

        #Populate the board again
        self.populate_board()