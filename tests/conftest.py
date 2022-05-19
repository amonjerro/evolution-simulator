import pytest

from src import Being
from src import Coordinate
from src import NeuronFactory
from src import BoardSingleton

from config import CONFIG
from .gene_factory import GeneFactory


GENE_LENGTH = 4


@pytest.fixture
def gene_factory():
    return GeneFactory()

@pytest.fixture
def gene_array_1():
    gf = GeneFactory()
    return [
        gf.sensor_to_action(),
        gf.internal_to_action(),
        gf.sensor_to_internal(),
        gf.internal_to_internal()
    ]

@pytest.fixture
def gene_array_2():
    gf = GeneFactory()
    return [
        gf.sensor_to_action(sensor_offset=1),
        gf.internal_to_action(internal_offset=1),
        gf.sensor_to_internal(sensor_offset=1, internal_offset=1),
        gf.internal_to_internal(origin_offset=1, target_offset=1)
        ]

@pytest.fixture
def being_1(gene_array_1):
    gs = [gene.gene_string for gene in gene_array_1]
    b = Being(Coordinate(0,0), gene_length=GENE_LENGTH, genes=gs)
    b.genome.set_quick_access_arrays()
    b.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    return b


@pytest.fixture
def being_2(gene_array_2):
    gs = [gene.gene_string for gene in gene_array_2]
    b = Being(Coordinate(1,1), gene_length=GENE_LENGTH, genes=gs)
    b.genome.set_quick_access_arrays()
    b.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    return b


@pytest.fixture
def being_1_collision(gene_array_1):
    gs = [gene.gene_string for gene in gene_array_1]
    b = Being(Coordinate(0,0), gene_length=GENE_LENGTH, genes=gs)
    b.genome.set_quick_access_arrays()
    b.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    return b

@pytest.fixture
def four_space_board():
    board = BoardSingleton()
    board.config({'board-size':2})
    return board