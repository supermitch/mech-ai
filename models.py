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
        user.put()
        return user

    def find_by_username(self, username):
        return UserModel.query(UserModel.username==username).get()

    def find_by_access_token(self, access_token):
        return UserModel.query(UserModel.access_token==access_token).get()


class GameModel(ndb.Model):
    """ Game """
    name = ndb.StringProperty()
    players = ndb.StringProperty(repeated=True)
    status = ndb.StringProperty()
    map = ndb.StringProperty()
    state = ndb.JsonProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

class GameRepo(object):
    def create(self, players, map='default'):
        game = GameModel(name='Arena', players=players, map=map, status='Waiting', state='{}')
        game.put()
        return game

    def find_by_id(self, id):
        return ndb.Key(GameModel, str(id)).get()
        #return GameModel.get_by_id(id)

    def find_by_player(self, username):
        return GameModel.query(GameModel.players==username).get()


user_repo = UserRepo()
game_repo = GameRepo()

