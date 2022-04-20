class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return str((self.x,self.y))

class Board:
    def __init__(self, config):
        self.board = []
        for i in range(config['board-size']):
            self.board.append([None for j in range(config['board-size'])])
        self.y_dim = len(self.board)
        self.x_dim = len(self.board[0])
    def get_dimensions(self):
        return (self.x_dim, self.y_dim)
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
    def wipe(self):
        del self.board[:]
        for i in range(self.y_dim):
            self.board.append([None for j in range(self.x_dim)])