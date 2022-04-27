import random

from config import CONFIG
from enum import Enum
from src.board import Coordinate

WORLD_SIZE = CONFIG['board-size']


class ActionEnum(Enum):
    MOVE_UP=1
    MOVE_RIGHT=2
    MOVE_DOWN=3
    MOVE_LEFT=4
    MOVE_RANDOM=5

class SensorEnum(Enum):
    SENSE_TOP_BORDER=1
    SENSE_RIGHT_BORDER=2
    SENSE_LOWER_BORDER=3
    SENSE_LEFT_BORDER=4
    # SENSE_UP=1
    # SENSE_RIGHT=2
    # SENSE_DOWN=3
    # SENSE_LEFT=4
    # SENSE_NEIGHBOR_DENSITY=5


## SENSORS ##

#Normalize the position of the being in relation to the world.
#Sensor range: [0-1]
def sense_left_border(coordinate):
    return (WORLD_SIZE-coordinate.x)/WORLD_SIZE

def sense_right_border(coordinate):
    return coordinate.x/WORLD_SIZE

def sense_top_border(coordinate):
    return (WORLD_SIZE-coordinate.y)/WORLD_SIZE

def sense_lower_border(coordinate):
    return coordinate.y/WORLD_SIZE

SENSOR_FUNCTIONS={
    SensorEnum.SENSE_TOP_BORDER:sense_top_border,
    SensorEnum.SENSE_LOWER_BORDER:sense_lower_border,
    SensorEnum.SENSE_RIGHT_BORDER:sense_right_border,
    SensorEnum.SENSE_LEFT_BORDER:sense_left_border
}

## ACTIONS ##

def move_up(coordinate):
    x,y = coordinate.unpack()
    return Coordinate(x,y-1)

def move_down(coordinate):
    x,y = coordinate.unpack()
    return Coordinate(x,y+1)

def move_left(coordinate):
    x,y = coordinate.unpack()
    return Coordinate(x-1,y)

def move_right(coordinate):
    x,y = coordinate.unpack()
    return Coordinate(x+1,y)

def move_random(coordinate):
    x,y = coordinate.unpack()
    new_y = y
    if random.randint(0,1) == 1:
        #Move Y
        if random.randint(0,1) == 1:
            # Move Up
            new_y = y - 1
        else:
            # Move Down
            new_y = y + 1
    
    new_x = x
    
    if random.randint(0,1) == 1:
        # Move X
        if random.randint(0,1) == 1:
            # Move Left
            new_x = x - 1
        else:
            # Move Right
            new_x = x + 1
    return Coordinate(new_x, new_y)


ACTION_FUNCTIONS={
    ActionEnum.MOVE_UP:move_up,
    ActionEnum.MOVE_DOWN:move_down,
    ActionEnum.MOVE_LEFT:move_left,
    ActionEnum.MOVE_RIGHT:move_right,
    ActionEnum.MOVE_RANDOM:move_random
}