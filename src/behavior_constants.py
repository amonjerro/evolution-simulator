import random
from enum import Enum
from src.board import Coordinate

class ActionEnum(Enum):
    MOVE_UP=1
    MOVE_RIGHT=2
    MOVE_DOWN=3
    MOVE_LEFT=4
    MOVE_RANDOM=5

class SensorEnum(Enum):
    SENSE_UP=1
    SENSE_RIGHT=2
    SENSE_DOWN=3
    SENSE_LEFT=4
    SENSE_NEIGHBOR_DENSITY=5
    SENSE_TOP_BORDER=6
    SENSE_RIGHT_BORDER=7
    SENSE_LOWER_BORDER=8
    SENSE_LEFT_BORDER=9

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