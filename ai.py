import random


# Define possible actions
GoNorth = 'Go North'
GoSouth = 'Go South'
GoEast = 'Go East'
GoWest = 'Go West'

TurnClockwise = 'Turn cw'
TurnCounterClockwise = 'Turn ccw'

Wait = 'Wait'


def make_move(state):
    """ Given a game state, decide on a move. """
    print(state)
    return random.choice([GoNorth, GoSouth, GoEast, GoWest])
