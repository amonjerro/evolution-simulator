import random

from src.board import Coordinate
from src.neuron import Gene

def pad_zeroes(value, min_length):
    zeroes = '0'*min_length
    return zeroes[:-len(value)]+value


class Genome:
    def __init__(self, genes, gene_length=0):
        self.blueprints = None
        if genes:
            self.genes = genes
        else:
            self.create_random(gene_length)

        self.sensors = []
        self.actions = []
        self.internals = []
        self._set_quick_access_arrays()
    
    def print_genome(self):
        print('===== Printing Genome =====')
        for gene in self.genes:
            origin, target, sensitivity = gene.decode(self.blueprints)
            print(f'Origin: {origin.name}, Activation: {origin.get_activation()}')
            print(f'Target: {target.name}, Activation: {target.get_activation()}')
            print(f'Connection Sensitivity: {sensitivity}')

    def create_random(self, gene_length):
        self.genes = []
        for i in range(gene_length):
            self.genes.append(Gene())

    def set_blueprints(self, blueprints):
        self.blueprints = blueprints

    def genes_to_color(self):
        total = sum([int(gene.gene_string, 16) for gene in self.genes])
        hexval = hex(int(total/len(self.genes)))[2:]
        return f'#{pad_zeroes(hexval, 6)}'
    
    def _set_quick_access_arrays(self):
        self.sensors = list(filter(lambda x: x.is_sensor(), self.genes))
        self.internals = list(filter(lambda x: x.is_internal(), self.genes))
        self.actions = list(filter(lambda x: x.is_action(), self.genes))


class Being:
    def __init__(self, starting_coordinates, gene_length, genes=None):
        self.x = starting_coordinates.x
        self.y = starting_coordinates.y
        self.excitability = random.uniform(0.5,1.5)
        self.genome = Genome(gene_length=gene_length, genes=genes)

    def update_position(self, new_coordinate):
        self.x = new_coordinate.x
        self.y = new_coordinate.y

    def get_position(self):
        return Coordinate(self.x, self.y)

    def get_genome(self):
        return self.genome

    def set_neuron_blueprints(self, blueprints):
        self.genome.set_blueprints(blueprints)

    def print_self(self):
        print('====Being Information=====')
        print(f'Location:({self.x},{self.y})')
        self.genome.print_genome()

    def act(self):
        actions = self.genome.actions
        position_update = self.get_position()
        for action in actions:
            c = action.enact(self.genome.blueprints, self.excitability)
            position_update.add(c)
        return position_update

    def activate_senses(self):
        senses = self.genome.sensors
        for sense in senses:
            sense.feed_forward(self.get_position(), self.genome.blueprints, self.excitability)

    def process_internals(self):
        internals = self.genome.internals
        for internal in internals:
            internal.feed_forward(None, self.genome.blueprints, self.excitability)


class Population:
    def __init__(self, config):
        self.population_size = config['population-size']
        self.being_list = []
    def get_population_size(self):
        return self.population_size
    def inspect_being(self, index):
        being = self.being_list[index]
        being.print_self()
        return self.being_list[index]
    def get_beings(self):
        return self.being_list
    def execute_senses(self):
        for being in self.being_list:
            being.activate_senses()
    def process_internal_signals(self):
        for being in self.being_list:
            being.process_internals()
    def add_being(self, being):
        self.being_list.append(being)
    def wipe(self):
        del self.being_list[:]