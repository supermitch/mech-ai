import random


# define possible actions
go_north = 'go north'
go_south = 'go south'
go_east = 'go east'
go_west = 'go west'

rotate_cw = 'rotate cw'
rotate_ccw = 'rotate ccw'

wait = 'wait'


def make_move(state):
    """ Given a game state, decide on a move. """
    print('AI making move for state: {}'.format(state))
    return random.choice([go_north, go_south, go_east, go_west, rotate_cw, rotate_ccw])
