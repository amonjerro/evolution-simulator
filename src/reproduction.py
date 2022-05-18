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

def gene_mixing(being_a, being_b, is_random=True):
    being_a_gene_strings = [gene.gene_string for gene in being_a.get_genome().genes]
    being_b_gene_strings = [gene.gene_string for gene in being_b.get_genome().genes]
    half_string_index = len(being_b_gene_strings[0]) // 2
    resulting_gene_strings = []
    if is_random:
        #To Do
        pass
    else:        
        for i in range(len(being_a_gene_strings)):   
            gene_string_a = being_a_gene_strings[i]
            gene_string_b = being_b_gene_strings[i]
            
            new_string = gene_string_a[:half_string_index] + gene_string_b[half_string_index:]
            resulting_gene_strings.append(new_string)
    return resulting_gene_strings

REPRODUCTION_FUNCTION_MAP = {
    'sexual_reproduction':sexual_reproduction,
    'gene_mixing':gene_mixing
} 