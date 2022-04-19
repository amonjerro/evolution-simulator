import secrets
from src.board import Coordinate

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
            self.genes.append(secrets.token_hex(3))
    def genes_to_color(self):
        total = sum([int(gene, 16) for gene in self.genes])
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