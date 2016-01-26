import random

# Move definitions
go_north = 'go north'
go_south = 'go south'
go_east = 'go east'
go_west = 'go west'
rotate_cw = 'rotate cw'
rotate_ccw = 'rotate ccw'
wait = 'wait'
shoot = 'shoot'

def make_move(state):
    """ Given a game state, decide on a move. """
    # TODO: Implement AI!
    return random.choice([
        go_north,
        go_south,
        go_east,
        go_west,
        rotate_cw,
        rotate_ccw,
        shoot,
    ])
