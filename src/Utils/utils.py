class Rect:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.x1 = start_x
        self.x2 = end_x
        self.y1 = start_y
        self.y2 = end_y

class Circle:
    def __init__(self, center_x, center_y, radius):
        x = center_x
        y = center_y
        r = radius

def pad_zeroes(value, min_length):
    zeroes = '0'*min_length
    return zeroes[:-len(value)]+value