import os

def load_map_file(self, name):
    """ Load map data from disk. """
    root = os.path.dirname(os.path.abspath(__file__))
    map_name = os.path.join(root, 'maps', name, '.txt')

    print('Loading map file [{}]'.format(map_name))
    if not os.path.isfile(map_name):
        print('Could not load map file [{}]'.format(map_name))
    else:
        try:
            with open(map_name, 'r') as f:
                return f.read()
        except IOError:
            print('IOError exception reading map file [{}]'.format(map_name))


