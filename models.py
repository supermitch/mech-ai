import tokens

from google.appengine.ext import ndb

from game import Game
from queue import Queue
from state import State


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
    map_name = ndb.StringProperty()
    state = ndb.JsonProperty()
    queue = ndb.JsonProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

class GameRepo(object):
    """ Abstraction of the GameModel storage in NDB. """

    def persist(self, game):
        """ Store a game in the repo. """
        print('Persisting: {}'.format(game.queue.json))
        game = GameModel(
            name=game.name,
            players=game.players,
            map_name=game.map_name,
            status=game.status,
            state=game.state.json,  # jsonify object
            queue=game.queue.json,  # jsonify object
            created=game.created,
        )
        game.put()
        return game

    def extract_game(self, game_id):
        """ Populate an return a Game from an NDB game entry. """
        model = self.find_by_id(game_id)
        game = Game()
        attrs = ['name', 'players', 'status', 'created', 'map_name']
        for attr in attrs:
            setattr(game, attr, getattr(model, attr))

        game.state = State()
        game.state.load_from_json(model.state)
        print('Model.state {}'.format(model.state))
        print('game.state: {}'.format(game.state))

        game.queue = Queue()
        print('Model.queue {}'.format(model.queue))
        print('game.queue: {}'.format(game.queue))
        game.queue.load_from_json(model.queue)
        return game

    def find_by_id(self, game_id):
        #return ndb.Key(GameModel, game_id).get()
        try:
            game_id = int(game_id)
        except (ValueError, TypeError):
            return None
        return GameModel.get_by_id(game_id)

    def find_by_player(self, username):
        return GameModel.query(GameModel.players==username).get()


user_repo = UserRepo()
game_repo = GameRepo()

