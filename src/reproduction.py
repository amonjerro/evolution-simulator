import random
from config import CONFIG


# Mutations
def random_mutation(string):
    if random.random() < CONFIG['mutation-chance']:
        index = random.randint(0,5)
        hex_components = list(string)

        # This implementation means there is a 1/16 chance a mutation does nothing.
        value = random.randint(0,15)

        hex_components[index] = hex(value)[2:]
        string = ''.join(hex_components)
    return string

def flip_bit(string, index):
    hex_list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    ls_string = list(string)
    original_value = int(string[index], 16)
    new_value = 1-original_value
    ls_string[index] = hex_list[new_value]
    return ''.join(ls_string)

# Reproduction Functions
def sexual_reproduction(being_a, being_b, is_random=True):
    resulting_gene_strings = []
    if is_random:
        haploid_length = len(being_a.get_genome().genes) // 2
        a_genes = random.sample(being_a.get_genome().genes, haploid_length)
        b_genes = random.sample(being_b.get_genome().genes, haploid_length)
        resulting_gene_strings = [ g.gene_string for g in a_genes+b_genes ]
        if CONFIG['mutation-enabled']:
            resulting_gene_strings = [ random_mutation(s) for s in resulting_gene_strings ]
    else:
        gene_length = len(being_a.get_genome().genes)
        if gene_length%2 == 0:
            haploid_length = gene_length // 2
            genes_from_a = being_a.get_genome().genes[:haploid_length]
            genes_from_b = being_b.get_genome().genes[haploid_length:]
            resulting_gene_strings = [ g.gene_string for g in genes_from_a+genes_from_b ]        
    return resulting_gene_strings
