from src import Gene

class GeneFactory:
    def __init__(self):
        g = Gene()
        self.INTERNAL_INDEX = g.INTERNAL_INDEX
        self.SENSOR_INDEX = g.SENSOR_INDEX
        self.ACTION_INDEX = g.ACTION_INDEX
        self.SPEC_ACTION_INDEX = g.SPEC_ACTION_INDEX
        self.SPEC_SENSOR_INDEX = g.SPEC_SENSOR_INDEX

    def sensor_to_action(self, excitation=11, sensor_offset=0, action_offset=0):
        initial_value = list(f'0000{excitation}')
        initial_value[self.SENSOR_INDEX] = str(sensor_offset*2)
        initial_value[self.SPEC_SENSOR_INDEX] = str(1)
        initial_value[self.ACTION_INDEX] = str(action_offset*2)
        initial_value[self.SPEC_ACTION_INDEX] = str(1)
        return Gene(''.join(initial_value))
    
    def internal_to_action(self, excitation=11, internal_offset=0, action_offset=0):
        initial_value = list(f'0000{excitation}')
        initial_value[self.INTERNAL_INDEX] = str(internal_offset*2+1)
        initial_value[self.SPEC_SENSOR_INDEX] = str(1)
        initial_value[self.ACTION_INDEX] = str(action_offset*2)
        initial_value[self.SPEC_ACTION_INDEX] = str(1)
        return Gene(''.join(initial_value))
    
    def sensor_to_internal(self, excitation=11, sensor_offset=0, internal_offset=0):
        initial_value = list(f'0000{excitation}')
        initial_value[self.SENSOR_INDEX] = str(sensor_offset*2)
        initial_value[self.SPEC_SENSOR_INDEX] = str(1)
        initial_value[self.ACTION_INDEX] = str(internal_offset*2+1)
        initial_value[self.SPEC_ACTION_INDEX] = str(1)
        return Gene(''.join(initial_value))

    def internal_to_internal(self, excitation=11, origin_offset=0, target_offset=0):
        initial_value = list(f'0000{excitation}')
        initial_value[self.INTERNAL_INDEX] = str(origin_offset*2+1)
        initial_value[self.SPEC_SENSOR_INDEX] = str(1)
        initial_value[self.ACTION_INDEX] = str(target_offset*2+1)
        initial_value[self.SPEC_ACTION_INDEX] = str(1)
        return Gene(''.join(initial_value))