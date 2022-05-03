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
    
    def get_dimensions(self):
        return (self.x_dim, self.y_dim)
    
    def is_valid_move(self, coordinate):
        if self.x_dim <= coordinate.x or coordinate.x < 0:
            #Invalid move on the X-axis
            return False
        elif self.y_dim <= coordinate.y or coordinate.y < 0:
            #Invalid move on the Y-axis
            return False
        elif self.is_occupied(coordinate):
            return False
        return True

    def is_occupied(self, coordinate):
        # Check if another being exists in the target coordinate
        coordinate_contents = self.board[coordinate.y][coordinate.x]
        if coordinate_contents is None:
            return False
    def populate_space(self, being):
        if not self.is_occupied(being.get_position()):
            self.board[being.y][being.x] = being
            return True
        return False
    def depopulate_space(self, coordinate):
        self.board[coordinate.y][coordinate.x] = None
    def wipe(self):
        del self.board[:]
        for i in range(self.y_dim):
            self.board.append([None for j in range(self.x_dim)])