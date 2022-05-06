import random
from config import CONFIG

def mutate(string):
    if random.random() < CONFIG['mutation-chance']:
        index = random.randint(0,5)
        hex_components = list(string)

        # This implementation means there is a 1/16 chance a mutation does nothing.
        value = random.randint(0,15)

        hex_components[index] = hex(value)[2:]
        string = ''.join(hex_components)
    return string

def sexual_reproduction(being_a, being_b):
    haploid_length = len(being_a.get_genome().genes) // 2
    a_genes = random.sample(being_a.get_genome().genes, haploid_length)
    b_genes = random.sample(being_b.get_genome().genes, haploid_length)
    resulting_gene_strings = [ g.gene_string for g in a_genes+b_genes]
    if CONFIG['mutation-enabled']:
        resulting_gene_strings = [ mutate(s) for s in resulting_gene_strings ]
    return resulting_gene_strings
