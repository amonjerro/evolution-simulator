import pytest

from src import Being
from src import Coordinate
from src import Gene    
from src import NeuronFactory
from config import CONFIG


GENE_LENGTH = 4

@pytest.fixture
def gene_array_1():
    return [
        Gene(hex_string='010111'), #Sensor to Action 
        Gene(hex_string='110111'), #Internal to Action
        Gene(hex_string='011111'), #Sensor to Internal
        Gene(hex_string='111111'), #Internal to Internal
    ]

@pytest.fixture
def gene_array_2():
    return [ 
        Gene(hex_string='210111'), #Sensor to Action 
        Gene(hex_string='310111'), #Internal to Action
        Gene(hex_string='213111'), #Sensor to Internal
        Gene(hex_string='313111'), #Internal to Internal
        ]

@pytest.fixture
def being_1(gene_array_1):
    b = Being(Coordinate(1,1), gene_length=GENE_LENGTH, genes=gene_array_1)
    b.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    return b

@pytest.fixture
def being_2(gene_array_2):
    b = Being(Coordinate(1,2), gene_length=GENE_LENGTH, genes=gene_array_2)
    b.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    return b
