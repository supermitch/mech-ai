import json
import requests

USERNAME = 'mitch'
ACCESS_TOKEN = 'ffs76cby'

host = 'http://mech-ai.appspot.com'
host = 'http://127.0.0.1:8080'


def register_user(username):
    """ Register a new username. """
    print('Attempting to register username: {} ...'.format(username))
    path = '/users/register'
    url = host + path
    data = {'username': username}
    r = requests.post(url, data=json.dumps(data))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e))
        return None

    output = r.json()
    print('\t' + output['message'])
    username, access_token = output['username'], output['access_token']
    if access_token is not None:
        print('\tUsername: {}'.format(username))
        print('\tAccess token: {}'.format(access_token))

    return access_token


def create_game():
    """ Create a new game. """
    print('Attempting to create game...')
    path = '/games/create'
    url = host + path
    headers = {
        'username': USERNAME,
        'access_token': ACCESS_TOKEN
    }
    data = json.dumps({
        'players': ['zora', 'chris', 'mitch'],
        'duration': 1000,
    })
    r = requests.post(url, headers=headers, data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e))
        return None

    output = r.json()
    print('\t' + output['message'])
    game_id, players = output['id'], output['players']
    if game_id is not None:
        print('\tGame ID: {}'.format(game_id))
        print('\tPlayers: {}'.format(', '.join(players)))
    return game_id


def play_game(game_id):
    """ Get a game ID for an existing game, if you are a listed player. """
    path = '/games/play'
    url = host + path
    headers = {
        'username': USERNAME,
        'access_token': ACCESS_TOKEN
    }
    data = json.dumps({'game_id': game_id})
    r = requests.post(url, headers=headers, data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e))
        return None
    print(r.url)
    output = r.json()
    print('\t' + output['message'])
    game_id = output['id']
    if game_id is not None:
        print('\tGame ID: {}'.format(game_id))
    return game_id


def main():
    # register_user('mitch')
    game_id = create_game()
    # play_game(game_id)


if __name__ == '__main__':
    main()

