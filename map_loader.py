import os

def read_map_file(map_name):
    """ Load map data from disk. """
    root = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(root, 'maps', map_name + '.txt')

    print('Loading map file [{}]'.format(map_name))
    if not os.path.isfile(map_path):
        print('Map file [{}] does not exist'.format(map_path))
    else:
        try:
            with open(map_path, 'r') as f:
                return f.read()
        except IOError:
            print('IOError exception reading map file [{}]'.format(map_path))

