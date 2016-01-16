

class Mech(object):
    """ Mech class. """

    def __init__(self, name, pos, health, score, ammo):
        self.name = name
        self.pos = pos
        self.x, self.y = self.pos
        self.health = health
        self.score = score
        self.ammo = ammo


class Enemy(Mech):
    """ Enemy mech class. """

    def __init__(self, name, pos, health, score, ammo):
        super(Enemy, self).__init__(name, pos, health, score, ammo)


class Player(Mech):
    """ Player mech class. """

    def __init__(self, name, pos, health, score, ammo):
        super(Player, self).__init__(name, pos, health, score, ammo)
