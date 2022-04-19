import random
from src.being import Being
from src.board import Coordinate


class Simulation:
    def __init__(self, board, imager, config):
        self.board = board
        self.population_size = config['population-size']
        self.gene_length = config['gene-length']
        self.max_steps = config['max-steps']
        self.max_generations = config['max-generations']
        self.imager = imager

    def populate_board(self, beings=None):
        dimensions = self.board.get_dimensions()
        for i in range(self.population_size):
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
                populated = self.board.populate_space(b)

    def run_simulation_step(self):
        #For every being, perform their actions

        #Render the new board state
        pass

    def run_simulation_generation(self):
        #Run all steps
        for step in range(self.max_steps):
            self.run_simulation_step()
            beings = self.board.get_beings()
            self.imager.render_simulation_step(step, beings)

        #Apply selection criteria

        #Create the new individuals

        #Wipe the board
        self.board.wipe()

        #Populate the board again
        self.populate_board()