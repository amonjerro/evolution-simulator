from src.board import Coordinate
from src.neuron import Gene

def pad_zeroes(value, min_length):
    zeroes = '0'*min_length
    return zeroes[:-len(value)]+value


class Genome:
    def __init__(self, genes, gene_length=0):
        if genes:
            self.genes = genes
        else:
            self.create_random(gene_length)
    def create_random(self, gene_length):
        self.genes = []
        for i in range(gene_length):
            self.genes.append(Gene())
    def genes_to_color(self):
        total = sum([int(gene.hex_string, 16) for gene in self.genes])
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


class Population:
    def __init__(self, config):
        self.population_size = config['population-size']
        self.being_list = []
    def get_population_size(self):
        return self.population_size
    def add_being(self, being):
        self.being_list.append(being)
    def wipe(self):
        del self.being_list[:]