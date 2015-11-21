import tokens

from google.appengine.ext import ndb


class UserModel(ndb.Model):
    """ Models a user of the system. """
    username = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)

class UserRepo(object):
    def create(self, username):
        access_token = tokens.generate_unique_token()
        user = UserModel(username=username, access_token=access_token)
        return user.put()

    def find_by_username(self, username):
        return UserModel.query(UserModel.username==username).get()

    def find_by_access_token(self, access_token):
        return UserModel.query(UserModel.access_token==access_token).get()

class GameModel(ndb.Model):
    """ Game """
    name = ndb.StringProperty()
    players = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty()
    map = ndb.StringProperty()
    state = ndb.JsonProperty()

class GameRepo(object):
    def create(players, map='default'):
        game = GameModel(players=players, map=map, status='Waiting', state='{}')
        return game.put()

    def find_by_id(self, id):
        return GameModel.query(GameModel.id==id).get()

    def find_by_player(self, username):
        return GameModel.query(GameModel.players==username).get()


user_repo = UserRepo()
game_repo = GameRepo()

