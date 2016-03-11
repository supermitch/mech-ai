import glob
import logging
import os

import maps

logging.info(maps.default.map)
logging.info(maps.hallway.map)

def list_maps():
    import pkgutil
    return [name for _, name, _ in pkgutil.iter_modules(['maps'])]

def get_map(map_name):
    map_module = getattr(maps, map_name)
    return getattr(map_module, 'map')
