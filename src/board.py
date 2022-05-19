class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y
 
    def __str__(self):
        return str((self.x,self.y))
 
    def unpack(self):
        return (self.x, self.y)
 
    def add(self, other):
        self.x += other.x
        self.y += other.y
    
    def compare(self, other):
        return self.x == other.x and self.y == other.y

class BoardSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BoardSingleton, cls).__new__(cls)
        return cls.instance
    
    def config(self, config):
        self.board = []
        for i in range(config['board-size']):
            self.board.append([None for j in range(config['board-size'])])
        self.y_dim = len(self.board)
        self.x_dim = len(self.board[0])
        self.collision_map = {}
    
    def get_dimensions(self):
        return (self.x_dim, self.y_dim)

    def collision_map_add(self, new_position, being):
        x, y = new_position.unpack()
        if f'{x},{y}' in self.collision_map.keys():
            self.collision_map[f'{x},{y}'].append(being)
        else:
            self.collision_map[f'{x},{y}'] = [being]
    
    def is_valid_move(self, coordinate):
        if self.x_dim <= coordinate.x or coordinate.x < 0:
            #Invalid move on the X-axis
            return False
        elif self.y_dim <= coordinate.y or coordinate.y < 0:
            #Invalid move on the Y-axis
            return False
        return True

    def resolve_occupation(self, position_key):
        x,y = map(lambda x: int(x), position_key.split(','))
        position_coord = Coordinate(x,y)
        candidates = self.collision_map[position_key]
        no_opped = None
        winner = None

        if len(candidates) == 1:
            winner = candidates[0]
        else:
            #Decide a winner
            max_excitement = 0
            for candidate in candidates:
                #Check for a no_opped
                if candidate.get_position().compare(position_coord):
                    no_opped = candidate
                    continue
                if candidate.excitability > max_excitement:
                    winner = candidate
                    max_excitement = candidate.excitability
        
        old_coordinate = winner.get_position()
        winner.update_position(position_coord)
        if no_opped:
            #Conditional no_opped logic
            no_opped.update_position(old_coordinate)
            self.populate_space(winner)
            self.populate_space(no_opped)
        else:
            self.depopulate_space(old_coordinate)
            self.populate_space(winner)

    def is_occupied(self, coordinate):
        # Check if another being exists in the target coordinate
        coordinate_contents = self.board[coordinate.y][coordinate.x]
        return coordinate_contents is None

    def populate_space(self, being):
        if not self.is_occupied(being.get_position()):
            self.board[being.y][being.x] = being
            return True
        return False

    def depopulate_space(self, coordinate):
        self.board[coordinate.y][coordinate.x] = None

    def collision_map_wipe(self):
        self.collision_map.clear()

    def board_wipe(self):
        del self.board[:]
        self.collision_map.clear()
        for i in range(self.y_dim):
            self.board.append([None for j in range(self.x_dim)])