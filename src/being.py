import random
from src.Reports import performance


from src.board import Coordinate
from src.neuron import Gene
from src.Utils import pad_zeroes
from src.behavior_constants import NeuronEnum, SensorInformationStruct
from src.Reports.performance import performance_check

class Genome:
    def __init__(self, genes, gene_length=0):
        self.blueprints = None
        if genes:
            self.genes = [Gene(string) for string in genes]
        else:
            self.create_random(gene_length)

        self.sensors = []
        self.actions = []
        self.internals = []
    
    def __str__(self):
        return str(list(map(str,self.genes)))

    def create_random(self, gene_length):
        self.genes = []
        for i in range(gene_length):
            self.genes.append(Gene())

    def set_blueprints(self, blueprints):
        self.blueprints = blueprints

    @performance_check('gene_color', 'Address gene coloring')
    def genes_to_color(self):        
        sensor_strings = [sensor.gene_string for sensor in self.sensors]
        action_strings = [action.gene_string for action in self.actions]
        salient_excitation = -999
        salient_gene = ''
        for string in action_strings+sensor_strings:
            string_excitation = int(string[:-2], 16)
            if string_excitation > salient_excitation:
                salient_excitation = string_excitation
                salient_gene = string

        new_string = f'#{salient_gene}' 
        return new_string
    
    @performance_check('indexing', 'Index the genes for a being')
    def set_quick_access_arrays(self):
        for gene in self.genes:
            if gene.is_sensor():
                self.sensors.append(gene)
            elif gene.is_internal():
                self.internals.append(gene)
            if gene.is_action():
                self.actions.append(gene)
    
    @performance_check('dead_bois', "Detecting dead genes", 'pop_board')
    def clear_dead_sensors(self):
        dead_genes_found = False
        
        # Detect dead internals
        available_internals = []
        dead_sensors = []
        for internal in self.internals:
            if internal.is_action():
                available_internals.append(internal.get_internal(self.blueprints, internal.gene_string[internal.SPEC_SENSOR_INDEX]))
        for i in range(len(self.sensors)):
            sense = self.sensors[i]
            if sense.leads_to_internal() and sense.get_internal(self.blueprints, sense.gene_string[sense.SPEC_ACTION_INDEX]) not in available_internals:
                sense.set_as_dead()
                dead_sensors.append(i)
                dead_genes_found = True
        
        for i in range(len(dead_sensors), 0, -1):
            self.sensors.pop(dead_sensors[i-1])

class Being:
    def __init__(self, starting_coordinates, gene_length, genes=None):
        self.x = starting_coordinates.x
        self.y = starting_coordinates.y
        self.age = 0
        self.lastMoveDirection = Coordinate(0,0)
        self.excitability = random.uniform(0.5,1.5)
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

    def print_self(self):
        print('====Being Information=====')
        print(f'Location:({self.x},{self.y})')
        self.genome.print_genome()

    @performance_check('act', 'Beings acting', 'sim_step')
    def act(self):
        position_update = self.get_position()
        for action in self.genome.actions:
            c = action.enact(self.genome.blueprints, self.excitability)
            position_update.add(c)
        return position_update

    def activate_senses(self):
        sensorInfo = SensorInformationStruct(self)
        for sense in self.genome.sensors:
            sense.feed_forward(sensorInfo, self.genome.blueprints, self.excitability)

    def process_internals(self):
        for internal in self.genome.internals:
            internal.feed_forward(None, self.genome.blueprints, self.excitability)


class PopulationSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PopulationSingleton, cls).__new__(cls)
        return cls.instance
    
    def config(self, config):
        self.population_size = config['population-size']
        self.being_list = []
    
    def get_population_size(self):
        return self.population_size
    
    def being_is_valid(self, being):
        genome = being.get_genome()
        return len(genome.sensors) > 0 and len(genome.actions) > 0
    
    def inspect_being(self, index):
        being = self.being_list[index]
        being.print_self()
        return self.being_list[index]
    
    def get_beings(self):
        return self.being_list
    
    @performance_check('sense', "Obtain sensor information", "sim_step")
    def execute_senses(self):
        [being.activate_senses() for being in self.being_list]
    
    @performance_check('internals', "Process all internal signals", "sim_step")
    def process_internal_signals(self):
        for being in self.being_list:
            being.process_internals()
    
    def add_being(self, being):
        self.being_list.append(being)
    
    def wipe(self):
        del self.being_list[:]