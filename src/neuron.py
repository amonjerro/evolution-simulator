import secrets

from src.errors import UndefinedNeuronError
from src.behavior_constants import ACTION_FUNCTIONS, ActionEnum
from src.behavior_constants import SENSOR_FUNCTIONS, SensorEnum

SENSOR_KEY = 'sensors'
INTERNAL_KEY = 'internal'
ACTIONS_KEY = 'actions'

class Neuron:
    def __init__(self):
        self.activated = False
        self.function = None
        self.name = ''
    def set_function(self, func):
        self.function = func
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
        

class Sensor(Neuron):
    def sense(self, params):
        if self.function:
            self.function(params)
        else:
            raise UndefinedNeuronError('This sensor neuron does not have a sensory function defined')

class Action(Neuron):
    def act(self):
        if self.function:
            self.function()
        else:
            raise UndefinedNeuronError('This action neuron does not have an action function defined')

class Internal(Neuron):
    pass

class NeuronFactory:
    def __init__(self, config):
        self.sensor = Sensor
        self.internal = Internal
        self.action = Action
        self.internal_neuron_limit = config['internal-neurons']
        self.genetic_blueprint = None
    def make_neurons_for_being(self):
        if self.genetic_blueprint is None:
            self.genetic_blueprint = {
                SENSOR_KEY:[],
                INTERNAL_KEY:[],
                ACTIONS_KEY:[]
            }

            for aEnumElement in ActionEnum:
                action = Action()
                action.set_function(ACTION_FUNCTIONS[aEnumElement])
                action.set_name(aEnumElement.name)
                self.genetic_blueprint[ACTIONS_KEY].append(action)
            
            for sEnumElement in SensorEnum:
                sensor = Sensor()
                sensor.set_function(SENSOR_FUNCTIONS[sEnumElement])
                sensor.set_name(sEnumElement.name)
                self.genetic_blueprint[SENSOR_KEY].append(sensor)
            
            for n in range(self.internal_neuron_limit):
                # Will probably need to expand this somehow
                internal = Internal()
                internal.set_name(f'INTERNAL {n}')
                self.genetic_blueprint[INTERNAL_KEY].append(internal)

        return self.genetic_blueprint

class Gene:
    # A gene is a connection between two neurons
    def __init__(self, hex_string=None):
        if hex_string:
            self.gene_string = hex_string
        else:
            self.gene_string = secrets.token_hex(3)
    def _get_neuron_from_blueprint(self, blueprint, key, rounds):
        neuron_type_length = len(blueprint[key])
        return blueprint[key][rounds%neuron_type_length]
    def decode(self, blueprint):
        origin = None
        target = None

        origin_neuron_type = int(self.gene_string[0],16)
        origin_rounds = int(self.gene_string[1],16)
        target_neuron_type = int(self.gene_string[2],16)
        target_rounds = int(self.gene_string[3], 16)
        connection_sensitivity = int(self.gene_string[-2:],16)

        origin_key = ''
        if origin_neuron_type % 2 == 0:
            #Origin is a Sensor
            origin_key = SENSOR_KEY
        else:
            origin_key = INTERNAL_KEY
        origin = self._get_neuron_from_blueprint(blueprint, origin_key, origin_rounds)
        
        target_key = ''
        if target_neuron_type % 2 == 0:
            #Target is an action
            target_key = ACTIONS_KEY
        else:
            target_key = INTERNAL_KEY
        target = self._get_neuron_from_blueprint(blueprint, target_key, target_rounds)

        return origin, target, connection_sensitivity

    

