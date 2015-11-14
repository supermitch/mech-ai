from google.appengine.ext import ndb


class User(ndb.Model):
    """ Models a user of the system. """
    username = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)


class Game(ndb.Model):
    """ Game """
    id = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    users = ndb.StringProperty()


class UserRepository(object):
    def find_by_username(self, username):
        return User.query(User.username==username).get()

    def find_by_access_token(self, access_token):
        return User.query(User.access_token==access_token).get()


class GameRepository(object):
    pass

user_repo = UserRepository()
game_repo = GameRepository()
