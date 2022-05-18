import pytest

from src import Being
from src import Coordinate
from src import NeuronFactory
from src import reproduction

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

def test_sexual_reproduction(being_1, being_2):
    # Test Deterministic Reproduction
    being_1_genes = being_1.get_genome().genes
    being_1_gene_strings = [gene.gene_string for gene in being_1_genes]
    being_2_genes = being_2.get_genome().genes
    being_2_gene_strings = [gene.gene_string for gene in being_2_genes]

    gene_length = len(being_1_genes)
    haploid_length = gene_length // 2
    new_gene_strings = reproduction.sexual_reproduction(being_1, being_2, is_random=False)
    assert new_gene_strings == being_1_gene_strings[:haploid_length] + being_2_gene_strings[haploid_length:]