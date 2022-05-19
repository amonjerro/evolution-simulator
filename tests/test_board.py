def test_board_size(four_space_board):
    x_size, y_size = four_space_board.get_dimensions()
    assert x_size == 2
    assert y_size == 2

def test_populate_being(four_space_board, being_1, being_2, being_1_collision):
    four_space_board.populate_space(being_1)
    being_1_position = being_1.get_position()
    assert four_space_board.is_occupied(being_1_position)
    
    four_space_board.populate_space(being_2)
    being_2_position = being_2.get_position()
    assert four_space_board.is_occupied(being_2_position)

    collision_populated = four_space_board.populate_space(being_1_collision)
    assert not collision_populated
