import glob
import logging
import os

def get_map_dir():
    """ Helpfully return the path to the map folder. """
    root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, 'maps')

def read_map_file(map_name):
    """ Load map data from disk. """
    map_path = os.path.join(get_map_dir(), map_name + '.txt')

    if not os.path.isfile(map_path):
        logging.error('Map file [{}] does not exist'.format(map_path))
    else:
        try:
            with open(map_path, 'r') as f:
                return f.read()
        except IOError:
            logging.error('IOError exception reading map file [{}]'.format(map_path))

def list_maps():
    """ Return a list of maps in the map folder. """
    return glob.glob(os.path.join(get_map_dir(), '*.txt'))

