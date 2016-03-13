import logging


def list_maps():
    return maps.keys()


def get_map(map_name):
    """ Return the actual map for the given name. """
    try:
        return maps[map_name].strip()  # No leading / trailing newlines
    except KeyError:
        logging.error('Could not find map name <{}> in maps: <{}>'
                      ''.format(map_name, list_maps()))
        return None


# Maps defined below:
maps = {
    'default': """
.........**.........
.@................@.
......********......
......********......
......********......
.@................@.
.........**.........
""",
    'hallway': """
...............**............**..........
.@.......**........**........**........@.
.........**............**................
""",
}
