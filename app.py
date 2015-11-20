import json
import os

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import channel

import tokens
from models import User, Game, user_repo, game_repo


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))

    def validate_json_fields(self, fields, json_object):
        """ Return 422 is not all fields are present in a JSON object. """
        messages = []
        for field in fields:
            if field not in json_object:
                messages.append('Field [{}] is required<br />'.format(field))
        if messages:
            webapp2.abort(422, detail='\n'.join(messages))

    def authenticate(self):
        """ Return 401 if authorization fails. """
        username = self.request.headers.get('Username', None)
        access_token = self.request.headers.get('Access-Token', None)

        db_user = user_repo.find_by_username(username)
        if not username or not access_token or db_user.access_token != access_token:
            webapp2.abort(401, 'Authentication failed, please verify Username and Access-Token headers')


class IndexHandler(BaseHandler):
    def get(self):
        self.render_template('index.html', name=self.request.get('name'))


class RegistrationHandler(webapp2.RequestHandler):
    def post(self):
        """ Generates and returns an access token for a POSTed username. """
        json_object = json.loads(self.request.body)
        if not 'username' in json_object:
            webapp2.abort(422, detail='Field [username] is required')

        posted_username = json_object['username']
        existing_user = user_repo.find_by_username(posted_username)
        if existing_user is None:
            access_token = tokens.generate_unique_token()
            user = User(username=posted_username, access_token=access_token)
            key = user.put()
            content = {
                'message': 'Registration succeeded',
                'username': user.username,
                'access_token': user.access_token,
            }
        else:
            content = {
                'username': posted_username,
                'message': 'Registration failed: username already exists',
                'access_token': None,
            }
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


class CreateGameHandler(webapp2.RequestHandler):
    def post(self):
        self.authenticate()  # TODO: @authenticate

        json_object = json.loads(self.request.body)
        players = json_object['players']

        game = Game(players=players)
        key = game.put()
        content = {
            'id': key.id(),
            'players': game.players,
            'map': 'default',
            'created': game.created.isoformat(),
            'message': 'Game creation succeeded',
        }
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


class PlayGameHandler(BaseHandler):
    def get(self):
        self.authenticate()  # TODO: @authenticate

        game = game_repo.find_by_player(username)
        print('GAME ID {} FOR USERNAME {} FOUND'.format(game.key.id(), username))
        channel_token = channel.create_channel(username + '::' + str(game.key.id()))
        content = {
            'username': username,
            'message': 'Joined the game',
            'game_id': game.key.id(),
        }
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))

    def post(self):
        json_object = json.loads(self.request.body)

        required_fields = ['username', 'access_token']
        self.validate_json_fields(required_fields, json_object)

        username = json_object['username']
        access_token = json_object['access_token']

        existing_user = user_repo.find_by_username(username)

        game = game_repo.find_by_player(username)
        print(game.key.id())
        print('GAME ID {} FOR USERNAME {} FOUND'.format(game.key.id(), username))
        channel_token = channel.create_channel(username + '::' + str(game.key.id()))
        content = {
            'username': username,
            'message': 'Joined the game',
            'channel_token': channel_token,
        }
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


class PlayerConnectHandler(BaseHandler):
    print('Player connected')
    pass


class PlayerDisconnectHandler(BaseHandler):
    print('Player disconnected')
    pass


def play_game(game_id):
    for i in range(10):
        channel_key = 'mitch::' + game_id
        channel.send_message(channel_key , message)

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=IndexHandler, name='home', methods=['GET']),
    webapp2.Route('/register', handler=RegistrationHandler, name='registration', methods=['POST']),
    webapp2.Route('/games/create', handler=CreateGameHandler, name='games_create', methods=['POST']),
    webapp2.Route('/games/play', handler=PlayGameHandler, name='games_play', methods=['GET']),
    webapp2.Route('/games/move', handler=PlayGameHandler, name='games_move', methods=['POST']),
    webapp2.Route('/_ah/channel/connected/', handler=PlayerConnectHandler),
    webapp2.Route('/_ah/channel/disconnected/', handler=PlayerDisconnectHandler),
], debug=True)

