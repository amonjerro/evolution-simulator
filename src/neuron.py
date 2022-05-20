import secrets
import math
import networkx as nx

from src.errors import UndefinedNeuronError
from src.behavior_constants import ACTION_FUNCTIONS, ActionEnum, no_op
from src.behavior_constants import SENSOR_FUNCTIONS, SensorEnum
from src.behavior_constants import NeuronEnum

class Neuron:
    def __init__(self):
        self.function = None
        self.activation_value = 0
        self.name = ''
        self.type = None
    def set_activation(self, value):
        self.activation_value = value
    def get_activation(self):
        return self.activation_value
    def set_function(self, func):
        self.function = func
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
        

class Sensor(Neuron):
    def __init__(self):
        self.type = NeuronEnum.SENSOR
    def sense(self, params):
        if self.function:
            self.set_activation(self.function(params))
        else:
            raise UndefinedNeuronError('This sensor neuron does not have a sensory function defined')

class Action(Neuron):
    def __init__(self):
        self.type = NeuronEnum.ACTION
        
    def set_threshhold(self, value):
        self.threshold = value
    def _meets_threshold(self, modifier):
        activation_value = math.tanh(self.get_activation()*modifier) 
        return  activation_value > self.threshold
    def act(self, modifier):
        if self.function:
            if self._meets_threshold(modifier):
                return self.function()
            else:
                return no_op()
        else:
            raise UndefinedNeuronError('This action neuron does not have an action function defined')

class Internal(Neuron):
    def __init__(self):
        self.type = NeuronEnum.INTERNAL
    pass

class NeuronFactory:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NeuronFactory, cls).__new__(cls)
        return cls.instance
    def config(self, config):
        self.sensor = Sensor
        self.internal = Internal
        self.action = Action
        self.internal_neuron_limit = config['internal-neurons']
        self.action_threshold = config['action-threshold']
    def make_neurons_for_being(self):
        blueprint = {
            NeuronEnum.SENSOR:[],
            NeuronEnum.INTERNAL:[],
            NeuronEnum.ACTION:[]
        }

        for aEnumElement in ActionEnum:
            action = Action()
            action.set_function(ACTION_FUNCTIONS[aEnumElement])
            action.set_name(aEnumElement.name)
            action.set_activation(0)
            action.set_threshhold(self.action_threshold)
            blueprint[NeuronEnum.ACTION].append(action)
        
        for sEnumElement in SensorEnum:
            sensor = Sensor()
            sensor.set_function(SENSOR_FUNCTIONS[sEnumElement])
            sensor.set_name(sEnumElement.name)
            sensor.set_activation(0)
            blueprint[NeuronEnum.SENSOR].append(sensor)
        
        for n in range(self.internal_neuron_limit):
            internal = Internal()
            internal.set_name(f'INTERNAL {n}')
            internal.set_activation(0)
            blueprint[NeuronEnum.INTERNAL].append(internal)

        return blueprint

    def make_neuron_graph(self):
        DG = nx.DiGraph()
        for sEnumElement in SensorEnum:
            DG.add_node(sEnumElement.name)
        for n in range(self.internal_neuron_limit):
            DG.add_node(f'INTERNAL {n}')
        for aEnumElement in ActionEnum:
            DG.add_node(aEnumElement.name)
        return DG


class Gene:
    # A gene is a connection between two neurons
    def __init__(self, hex_string=None):
        self.SENSOR_INDEX = 1
        self.SPEC_SENSOR_INDEX = 0
        self.INTERNAL_INDEX = 1
        self.ACTION_INDEX = 3
        self.SPEC_ACTION_INDEX = 2
        if hex_string:
            self.gene_string = hex_string
        else:
            self.gene_string = secrets.token_hex(3)

    def _get_neuron_from_blueprint(self, blueprint, key, rounds):
        neuron_type_length = len(blueprint[key])
        return blueprint[key][rounds%neuron_type_length]

    def is_sensor(self):
        return int(self.gene_string[self.SENSOR_INDEX],16) % 2 == 0
    
    def is_internal(self):
        return int(self.gene_string[self.INTERNAL_INDEX],16) % 2 == 1
        
    def is_action(self):
        return int(self.gene_string[self.ACTION_INDEX],16)%2==0

    def feed_forward(self, params, blueprint, excitability):
        origin, target, sensitivity = self.decode(blueprint)

        if origin.type == NeuronEnum.SENSOR:
            origin.sense(params)

        activation_score = origin.get_activation()*sensitivity*excitability

        target.set_activation(target.get_activation()+activation_score)
        origin.set_activation(0)
    
    def enact(self, blueprint, excitability):
        origin, action, _ = self.decode(blueprint)
        act_results = action.act(excitability)
        action.set_activation(0)
        return act_results

    def decode(self, blueprint):
        #The hexstring that contains all the information to describe the gene
        origin = None
        target = None

        origin_neuron_type = int(self.gene_string[self.SENSOR_INDEX], 16)
        origin_rounds = int(self.gene_string[self.SPEC_SENSOR_INDEX], 16)
        target_neuron_type = int(self.gene_string[self.ACTION_INDEX], 16)
        target_rounds = int(self.gene_string[self.SPEC_ACTION_INDEX], 16)
        connection_sensitivity = int(self.gene_string[-2:],16) / 128

        origin_key = ''
        if origin_neuron_type % 2 == 0:
            #Origin is a Sensor
            origin_key = NeuronEnum.SENSOR
        else:
            origin_key = NeuronEnum.INTERNAL
        origin = self._get_neuron_from_blueprint(blueprint, origin_key, origin_rounds)
        
        target_key = ''
        if target_neuron_type % 2 == 0:
            #Target is an action
            target_key = NeuronEnum.ACTION
        else:
            target_key = NeuronEnum.INTERNAL
        target = self._get_neuron_from_blueprint(blueprint, target_key, target_rounds)

        return origin, target, connection_sensitivity

    

