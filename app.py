import json
import logging
import os

import webapp2
from webapp2_extras import jinja2

import tokens
from models import user_repo, game_repo
from game import Game, GAME_STATUS


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
        print(username, access_token)
        db_user = user_repo.find_by_username(username)
        if username is None or access_token is None or db_user is None or db_user.access_token != access_token:
            webapp2.abort(401, 'Authentication failed, please verify Username and Access-Token headers')
        return username


class IndexHandler(BaseHandler):
    def get(self):
        self.render_template('index.html', name=self.request.get('name'))


class RegistrationHandler(BaseHandler):
    def post(self):
        """ Generates and returns an access token for a POSTed username. """
        json_object = json.loads(self.request.body)
        self.validate_json_fields(['username'], json_object)

        posted_username = json_object['username']
        existing_user = user_repo.find_by_username(posted_username)
        if existing_user is None:
            user = user_repo.create(username=posted_username)
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


class CreateGameHandler(BaseHandler):
    def post(self):
        username = self.authenticate()  # TODO: @authenticate

        json_object = json.loads(self.request.body)
        # TODO: Players optional, allows for open game lobby or bots
        self.validate_json_fields(['players'], json_object)

        players = json_object['players']
        map = json_object.get('map', 'default')

        game = Game(players=players, map_name=map)
        game_model = game_repo.persist(game)

        content = {
            'id': game_model.key.id(),
            'name': game_model.name,
            'players': game_model.players,
            'map_name': game_model.map_name,
            'created': game_model.created.isoformat(),
            'message': 'Game creation succeeded',
        }
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


class PlayGameHandler(BaseHandler):
    def post(self):
        username = self.authenticate()  # TODO: @authenticate

        json_object = json.loads(self.request.body)
        self.validate_json_fields(['game_id', 'message'], json_object)

        game_id = json_object['game_id']
        game_model = game_repo.find_by_id(game_id)
        if not game_model:
            logging.info('Invalid message type [{}]. Must be "join" or "move".'.format(message))
            webapp2.abort(404, detail='Could not find game for game_id [{}]'.format(game_id))
        else:
            print('Game id [{}] found'.format(game_model.key.id()))

        message = json_object['message']
        if message not in ['join', 'move']:
            logging.info('Invalid message type [{}]. Must be "join" or "move".'.format(message))
            webapp2.abort(422, detail='Invalid message type [{}]. Must be "join" or "move".'.format(message))

        # TODO: Why not have the repo just returned a populated game?
        game = Game()  # New empty game
        game.load_from_model(game_model)  # Load from repo

        content = {  # Start building response content
            'game_id': game_model.key.id()
        }
        if game.status == GAME_STATUS.lobby:
            if message == 'join':  # Ignore all other messages
                game.queue.set_status(username, 'joined')

            if game.queue.is_complete:
                game.status == GAME_STATUS.playing
                content['message'] = 'Game started'
            else:
                content['message'] = 'Waiting for players {}'.format(', '.join(game.queue.not_joined))

        elif game.status == GAME_STATUS.playing:
            if game.queue.is_turn(username):
                content['message'] = 'Move successful'
                # And the player sent a move:
                    # update the game
            else:
                content['message'] = 'Not your turn.'
            pass

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=IndexHandler, name='home', methods=['GET']),
    webapp2.Route('/users/register', handler=RegistrationHandler, name='registration', methods=['POST']),
    webapp2.Route('/games/create', handler=CreateGameHandler, name='games_create', methods=['POST']),
    webapp2.Route('/games/play', handler=PlayGameHandler, name='games_play', methods=['POST']),
], debug=True)

