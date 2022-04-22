import secrets

from src.errors import UndefinedNeuronError
from src.behavior_constants import ACTION_FUNCTIONS

class Neuron:
    def __init__(self):
        self.activated = False

class Sensor(Neuron):
    def __init__(self):
        self.function = None
    def set_function(self, sensor_func):
        self.function = sensor_func
    def sense(self, params):
        if self.function:
            self.function(params)
        else:
            raise UndefinedNeuronError('This sensor neuron does not have a sensory function defined')

class Action(Neuron):
    def __init__(self):
        self.function = None
    def set_function(self, action_func):
        self.function = action_func
    def act(self):
        if self.function:
            self.function()
        else:
            raise UndefinedNeuronError('This action neuron does not have an action functoin defined')

class Internal(Neuron):
    pass

class NeuronFactory:
    def __init__(self):
        self.sensor = Sensor
        self.internal = Internal
        self.action = Action
    def make_neuron(self, genetic_info):
        #Implement a switch case to see the kind of neuron that gets created from this genetic info
        pass

class Gene:
    # A gene is a connection between two neurons
    def __init__(self, hex_string=None):
        if hex_string:
            self.gene_string = hex_string
        else:
            self.gene_string = secrets.token_hex(3)
    

