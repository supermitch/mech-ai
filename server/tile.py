import logging


class Tile(object):
    """ An object representing a 'tile' on the map. """
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self.pos = (x, y)
        try:
            self.kind = {
                '.': 'open',
                '*': 'block',
                '@': 'spawn_point',
            }[char]
        except KeyError:
            self.kind = 'open'
            logging.error('Unknown character <{}> at ({}, {}) in map file'.format(char, x, y))

        if self.kind in ('open', 'spawn_point'):
            self.walkable = True
        else:
            self.walkable = False

