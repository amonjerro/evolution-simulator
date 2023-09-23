import random

from src.board import Coordinate
from src.neuron import Gene
from src.Utils import pad_zeroes
from src.behavior_constants import NeuronEnum, SensorInformationStruct

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

    def genes_to_color(self):
        sensor_index = self.genes[0].SPEC_SENSOR_INDEX
        action_index = self.genes[0].SPEC_ACTION_INDEX
        sensor_length = len(self.blueprints[NeuronEnum.SENSOR])
        action_length = len(self.blueprints[NeuronEnum.ACTION])
        
        sensor_strings = [sensor.gene_string for sensor in self.sensors]
        action_strings = [action.gene_string for action in self.actions]
        
        moduloed_sensors = sum([int(s[sensor_index],16) for s in sensor_strings]) % sensor_length
        moduloed_actions = sum([int(a[action_index],16) for a in action_strings]) % action_length
        average_excitation = sum([int(gene.gene_string[-2:],16) for gene in self.genes])/len(self.genes)
        average_excitation -= 64
        if average_excitation < 0:
            average_excitation = 0 

        sensor_val = hex(moduloed_sensors)[2:]
        action_val = hex(moduloed_actions)[2:]
        excitation_val = pad_zeroes(hex(int(average_excitation))[2:],2)
        new_string = f'#{sensor_val}0{action_val}0{excitation_val}' 
        return new_string
    
    def set_quick_access_arrays(self):
        for gene in self.genes:
            if gene.is_sensor():
                self.sensors.append(gene)
            elif gene.is_internal():
                self.internals.append(gene)
            
            if gene.is_action():
                self.actions.append(gene)


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

    def act(self):
        actions = self.genome.actions
        position_update = self.get_position()
        for action in actions:
            c = action.enact(self.genome.blueprints, self.excitability)
            position_update.add(c)
        return position_update

    def activate_senses(self):
        senses = self.genome.sensors
        for sense in senses:
            sensorInfo = SensorInformationStruct(self)
            sense.feed_forward(sensorInfo, self.genome.blueprints, self.excitability)

    def process_internals(self):
        internals = self.genome.internals
        for internal in internals:
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
    
    def execute_senses(self):
        for being in self.being_list:
            being.activate_senses()
    
    def process_internal_signals(self):
        for being in self.being_list:
            being.process_internals()
    
    def add_being(self, being):
        self.being_list.append(being)
    
    def wipe(self):
        del self.being_list[:]