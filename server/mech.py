

class Mech(object):
    """ Mech class """

    def __init__(self, name, pos, health, score, ammo):
        self.name = name
        self.pos = pos
        self.x, self.y = self.pos
        self.health = health
        self.score = score
        self.ammo = ammo

