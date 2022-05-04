import pytest

from src import Being
from src import Coordinate
from src import NeuronFactory

from tests.conftest import GENE_LENGTH
from tests.conftest import CONFIG

def test_internal_arrays(being_1, being_2):
    being_1_genome = being_1.get_genome()
    being_2_genome = being_2.get_genome()

    # Action Strings
    being_1_action_strings = [a.gene_string for a in being_1_genome.actions]
    being_2_action_strings = [a.gene_string for a in being_2_genome.actions]

    assert len(being_1_action_strings) == 2
    assert len(being_2_action_strings) == 2

    # Sensor Strings
    being_1_sensor_strings = [a.gene_string for a in being_1_genome.sensors]
    being_2_sensor_strings = [a.gene_string for a in being_2_genome.sensors]

    assert len(being_1_sensor_strings) == 2
    assert len(being_2_sensor_strings) == 2

    # Internal Strings
    being_1_internal_strings = [a.gene_string for a in being_1_genome.internals]
    being_2_internal_strings = [a.gene_string for a in being_2_genome.internals]

    assert len(being_1_internal_strings) == 2
    assert len(being_2_internal_strings) == 2

def test_mutate_sensor_to_internal(gene_array_1):
    first_gene_string = list(gene_array_1[0].gene_string)
    first_gene_string[0] = '1'
    gene_array_1[0].gene_string = ''.join(first_gene_string)

    assert gene_array_1[0].gene_string == '110111'
    new_being = Being(Coordinate(3,1), gene_length=GENE_LENGTH, genes=gene_array_1)
    new_being.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    sensor_array = [a.gene_string for a in new_being.get_genome().sensors]
    expected_array = ['011111']
    assert expected_array == sensor_array

    internal_array = [a.gene_string for a in new_being.get_genome().internals]
    expected_array = ['110111','110111','111111']
    assert internal_array == expected_array

def test_mutate_internal_to_sensor(gene_array_1):
    first_gene_string = list(gene_array_1[3].gene_string)
    first_gene_string[0] = '0'
    gene_array_1[3].gene_string = ''.join(first_gene_string)

    assert gene_array_1[3].gene_string == '011111'
    new_being = Being(Coordinate(3,1), gene_length=GENE_LENGTH, genes=gene_array_1)
    new_being.set_neuron_blueprints(NeuronFactory(CONFIG).make_neurons_for_being())
    sensor_array = [a.gene_string for a in new_being.get_genome().sensors]
    expected_array = ['010111','011111','011111']
    assert expected_array == sensor_array

    internal_array = [a.gene_string for a in new_being.get_genome().internals]
    expected_array = ['110111']
    assert internal_array == expected_array