import json
import logging
import os

import webapp2
from webapp2_extras import jinja2
from webapp2_extras.routes import RedirectRoute, PathPrefixRoute

import tokens
import map_loader
from models import user_repo, game_repo
from game import Game, GAME_STATUS


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))

    def validate_json_fields(self, fields, json_object):
        """ Return 422 if not all fields are present in a JSON object. """
        messages = ['Field <{}> is required<br />'.format(field) for field in fields if field not in json_object]
        if messages:
            webapp2.abort(422, detail='\n'.join(messages))

    def authenticate(self):
        """ Return 401 if authorization fails. """
        username = self.request.headers.get('Username', None)
        access_token = self.request.headers.get('Access-Token', None)
        logging.debug('Authenticating username <{}> token <{}>'.format(username, access_token))
        db_user = user_repo.get_by_username(username)
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
        existing_user = user_repo.get_by_username(posted_username)
        if not existing_user:
            user = user_repo.create(username=posted_username)
            content = {
                'username': user.username,
                'access_token': user.access_token,
                'message': 'Registration succeeded',
            }
        else:
            content = {
                'username': None,
                'access_token': None,
                'message': 'Registration failed: username <{}> already exists'.format(posted_username),
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
        name = json_object.get('name', 'Mech AI')
        rounds = json_object.get('rounds', 17)
        map_name = json_object.get('map', 'Default')

        game = Game(players=players, map_name=map_name, name=name, rounds=rounds)
        game.transactions.append({
            'move': None,
            'message': (True, 'Initial state'),
            'state': game.state.jsonable,
        })
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


def handle_client_message(username, game, json_object):
    """ Return response content given a game and a client's message. """
    # TODO: Where should this live?
    message = json_object['message']
    logging.debug('Received message <{}>'.format(message))
    content = {'game_id': json_object['game_id']}  # Return a dictionary
    if message == 'join':
        if game.status == GAME_STATUS.lobby:
            logging.debug('Game in lobby')
            game.queue.set_status(username, 'joined')
            logging.debug('Statuses: {}'.format(game.queue.statuses))

            if game.queue.is_complete:
                game.status = GAME_STATUS.playing
                logging.debug('Game queue is complete')
                content['message'] = 'Game started'
            else:
                logging.debug('Game gueue is incomplete')
                content['message'] = 'Waiting for players {}'.format(', '.join(game.queue.not_joined))
        elif game.status == GAME_STATUS.playing:
            logging.debug('Game in progess')
            content['message'] = 'Game started'  # Stop joining
        elif game.status == GAME_STATUS.complete:
            logging.debug('Game is complete!')
            content['message'] = 'Game complete'
        else:
            logging.error('Unknown game status: {}'.format(game.status))

    elif message == 'status':
        if game.status == GAME_STATUS.lobby:
            logging.debug('Game gueue is incomplete')
            content['message'] = 'Waiting for players {}'.format(', '.join(game.queue.not_joined))
        elif game.status == GAME_STATUS.playing:
            if game.queue.is_turn(username):
                logging.debug('It is your turn, {}'.format(username))
                content['message'] = 'Your turn'  # Tell them to make a move
            else:
                logging.debug('It is not your turn')
                content['message'] = 'Not your turn'
            content['state'] = game.state.json  # Return state either way
        elif game.status == GAME_STATUS.complete:
            logging.debug('Game is complete!')
            content['message'] = 'Game complete'
        else:
            logging.error('Unknown game status: {}'.format(game.status))

    elif message == 'move':
        if game.status == GAME_STATUS.lobby:
            logging.debug('Game gueue is incomplete')
            content['message'] = 'Waiting for players {}'.format(', '.join(game.queue.not_joined))

        elif game.status == GAME_STATUS.playing:
            if game.queue.is_turn(username):
                logging.debug('Received move <{}> from player <{}>'.format(json_object['move'], username))
                success, reason = game.update(username, json_object['move'])
                if success:
                    content['message'] = 'Move successful'
                else:
                    content['message'] = 'Move rejected: {}'.format(reason)

                game.transactions.append({
                    'move': json_object['move'],
                    'message': (success, reason),
                    'state': game.state.jsonable,
                })
            else:
                logging.debug('It is not your turn')
                content['message'] = 'Not your turn'
            content['state'] = game.state.json  # Return state either way
        elif game.status == GAME_STATUS.complete:
            logging.debug('Game is complete!')
            content['message'] = 'Game complete'
        else:
            logging.error('Unknown game status: {}'.format(game.status))

    else:
        content['message'] = 'Unknown message content <{}>'.format(message)
        logging.error('Unknown message content <{}>'.format(message))

    logging.debug('Persisting game...')
    game_repo.persist(game)  # Store state to disk

    return content


class PlayGameHandler(BaseHandler):
    def post(self):
        username = self.authenticate()

        json_object = json.loads(self.request.body)
        self.validate_json_fields(['game_id', 'message'], json_object)

        logging.debug('Extracting game from model...')
        game_id = json_object['game_id']
        game = game_repo.extract_game(game_id)
        if not game:
            error_message = 'Could not find game for game_id <{}>'.format(game_id)
            logging.warn(error_message)
            webapp2.abort(404, detail=error_message)
        else:
            logging.debug('Game id <{}> found'.format(game_id))

        message = json_object['message']
        if message not in ('status', 'join', 'move'):
            logging.warn('Invalid message type <{}>'.format(message))
            webapp2.abort(422, detail='Invalid message type <{}>'.format(message))

        content = handle_client_message(username, game, json_object)

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


class FindGameHandler(BaseHandler):
    def get(self):
        username = self.authenticate()  # TODO: @authenticate decorator

        game_model = game_repo.find_lobby_by_username(username)
        if game_model:
            content = {
                'id': game_model.key.id(),
                'name': game_model.name,
                'players': game_model.players,
                'map_name': game_model.map_name,
                'created': game_model.created.isoformat(),
                'message': 'Game found',
            }
            logging.debug('Found game: {}'.format(content))
        else:
            error_message = 'Could not find game for username [{}]'.format(username)
            logging.info(error_message)
            webapp2.abort(404, detail=error_message)

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


def list_game_by_username_and_id(username, id):
    """
    Return game results as a dictionary, for given query params.

    Common functionality to list games by username & id. Both can be None.
    """
    results = game_repo.find_by_username_and_id(username, id)
    results = results if results else []
    return {
        'results': [{
            'id': game_model.key.id(),
            'name': game_model.name,
            'players': game_model.players,
            'map_name': game_model.map_name,
            'status': game_model.status,
            'created': game_model.created.isoformat(),
            'transactions': json.loads(game_model.transactions),
        } for game_model in results]
    }


class ListGameHandler(BaseHandler):
    """ Handler for API to list games. """
    def get(self, id=None):
        username = self.request.get('user')
        results = list_game_by_username_and_id(username, id)
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(results))


class ListGamePageHandler(BaseHandler):
    """ Handler for template to list games. """
    def get(self, id=None):
        username = self.request.get('user')
        print('username {}'.format(username))
        results = list_game_by_username_and_id(username, id)['results']  # Extract inner contents
        context = {
            'games': results,
            'username': username,
            'id': id,
        }
        self.render_template('games.html', **context)


def list_users_by_username(username):
    """
    Return user results as a dictionary, for given query params.

    Common functionality to list users by username & id. Both can be None.
    """
    results = user_repo.find_by_username(username)
    results = results if results else []
    return {
        'results': [{
            'username': user_model.username,
            'access_token': user_model.access_token,
            'created': user_model.created,
        } for user_model in results]
    }


class ListUserHandler(BaseHandler):
    """ Handler for API to list users. """
    def get(self):
        username = self.request.get('user')
        results = list_users_by_username(username)
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(results))


class ListUserPageHandler(BaseHandler):
    """ Handler for template to list users. """
    def get(self, username=None):
        results = list_users_by_username(username)['results']  # Extract inner contents
        context = {
            'users': results,
            'username': username,
        }
        self.render_template('users.html', **context)


class ListMapsHandler(BaseHandler):
    """ Handler for template to list users. """
    def get(self):
        context = {'maps': map_loader.list_maps()}
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(context))


app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=IndexHandler, name='home', methods=['GET']),
    PathPrefixRoute('/games', [
        RedirectRoute('/', handler=ListGamePageHandler, name='games_list_page', methods=['GET'], strict_slash=True),
        webapp2.Route('/<id:[0-9]+$>', handler=ListGamePageHandler, name='game_show_page', methods=['GET']),
    ]),
    PathPrefixRoute('/users', [
        RedirectRoute('/', handler=ListUserPageHandler, name='users_list_page', methods=['GET'], strict_slash=True),
        webapp2.Route('/<username>', handler=ListUserPageHandler, name='users_show_page', methods=['GET']),
    ]),
    PathPrefixRoute('/api/v1/games', [
        RedirectRoute('/', handler=ListGameHandler, name='games_list_api', methods=['GET'], strict_slash=True),
        webapp2.Route('/create', handler=CreateGameHandler, name='games_create_api', methods=['POST']),
        webapp2.Route('/play', handler=PlayGameHandler, name='games_play_api', methods=['POST']),
        webapp2.Route('/find', handler=FindGameHandler, name='games_find_api', methods=['GET']),
        webapp2.Route('/<id:[0-9]+$>', handler=ListGameHandler, name='game_show_api', methods=['GET']),
    ]),
    PathPrefixRoute('/api/v1/users', [
        RedirectRoute('/', handler=ListUserHandler, name='users_list_api', methods=['GET'], strict_slash=True),
        webapp2.Route('/register', handler=RegistrationHandler, name='user_registration_api', methods=['POST']),
    ]),
    PathPrefixRoute('/api/v1/maps', [
        RedirectRoute('/', handler=ListMapsHandler, name='maps_list_api', methods=['GET'], strict_slash=True),
    ]),
], debug=True)
