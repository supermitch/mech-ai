from google.appengine.ext import ndb


class User(ndb.Model):
    """ Models a user of the system. """
    username = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)

class UserRepository(object):
    def find_by_username(self, username):
        return User.query(User.username==username).get()

    def find_by_access_token(self, access_token):
        return User.query(User.access_token==access_token).get()

user_repo = UserRepository()


class Game(ndb.Model):
    """ Game """
    name = ndb.StringProperty()
    players = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

class GameRepository(object):
    def find_by_id(self, id):
        return Game.query(Game.id==id).get()

    def find_by_player(self, username):
        return Game.query(Game.players==username).get()

game_repo = GameRepository()
