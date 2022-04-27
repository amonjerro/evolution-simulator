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
    def print_genome(self):
        print('===== Printing Genome =====')
        for gene in self.genes:
            origin, target, sensitivity = gene.decode(self.blueprints)
            print(f'Origin: {origin.name}')
            print(f'Target: {target.name}')
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


class Being:
    def __init__(self, starting_coordinates, gene_length, genes=None):
        self.x = starting_coordinates.x
        self.y = starting_coordinates.y
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


class Population:
    def __init__(self, config):
        self.population_size = config['population-size']
        self.being_list = []
    def get_population_size(self):
        return self.population_size
    def get_being_by_index(self, index):
        return self.being_list[index]
    def get_beings(self):
        return self.being_list
    def add_being(self, being):
        self.being_list.append(being)
    def wipe(self):
        del self.being_list[:]